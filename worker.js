// JS스포츠 — Cloudflare Worker
// 정적 파일(ASSETS)을 그대로 내보내되, 관리자(/admin)에서 고친 내용(D1 settings)을 HTMLRewriter 로 덮어쓴다.
// HTML 의 편집 지점은 tools/cms-tag.js 가 붙인 data-cms 키로 찾는다.
// 그 밖에: 방문 기록(/api/t), 상담 신청(/api/inquiry), 관리자 API(/api/admin/*), 업로드 사진(/media/*), 기구 라인업 데이터(/js/lexco-data.js).

const SELF_HOSTS = new Set(['js-sports.kr', 'www.js-sports.kr', 'js-sports.hsk9867.workers.dev', 'hsk9867.github.io', 'localhost', '127.0.0.1']);
const PRIMARY_HOST = 'js-sports.kr';        // 검색에 잡혀야 하는 주소. 그 밖의 주소(workers.dev)는 noindex
const COOKIE = 'js_admin';
const VID_COOKIE = 'js_vid';
const VID_RE = /^[a-f0-9]{16}$/;
const VID_DAYS = 400;
const SESSION_DAYS = 30;
const SETTINGS_TTL = 30 * 1000;
const KST_OFFSET = 9 * 3600;
// 홈페이지 기본 전화번호. 관리자 설정에서 바꾸면 모든 전화 버튼(tel:)과 글자 속 번호가 함께 바뀐다.
const PHONES = { 'site.phone': '16889634', 'site.mobile': '01092298051' };

let settingsCache = { at: 0, map: null };

// ---------- 공통 ----------

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const safeImg = (v) => (typeof v === 'string' && /^(\/media\/[a-f0-9]{16}\.(jpg|png|webp)|img\/[\w./-]+|https:\/\/\S+)$/i.test(v.trim()) ? v.trim() : '');
const fmtPhone = (d) => (/^1\d{3}\d{4}$/.test(d) ? d.replace(/^(\d{4})(\d{4})$/, '$1-$2') : /^010\d{8}$/.test(d) ? d.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3') : /^0\d{1,2}\d{3,4}\d{4}$/.test(d) ? d.replace(/^(0\d{1,2})(\d{3,4})(\d{4})$/, '$1-$2-$3') : d);

// 관리자가 고친 글(안쪽 HTML)에서 허용하는 것: 줄바꿈과 글자 서식 태그, class / 간단한 style 만
const RICH_TAGS = new Set(['br', 'b', 'strong', 'em', 'i', 'small', 'span', 'mark', 'sup', 'sub', 'u']);
function sanitizeRich(html) {
  let out = '';
  const re = /<(\/?)([a-zA-Z0-9]+)([^>]*)>/g;
  let last = 0, m;
  const stack = [];
  const text = (s) => s.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/&(?!(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);)/g, '&amp;');
  while ((m = re.exec(html))) {
    out += text(html.slice(last, m.index));
    last = re.lastIndex;
    const close = !!m[1], tag = m[2].toLowerCase();
    if (!RICH_TAGS.has(tag)) continue;
    if (tag === 'br') { if (!close) out += '<br>'; continue; }
    if (close) {
      const i = stack.lastIndexOf(tag);
      if (i < 0) continue;
      while (stack.length > i) out += `</${stack.pop()}>`;
      continue;
    }
    let attrs = '';
    const cls = m[3].match(/\bclass\s*=\s*"([\w\s-]{0,80})"/);
    if (cls) attrs += ` class="${cls[1]}"`;
    const st = m[3].match(/\bstyle\s*=\s*"([^"]{0,120})"/);
    if (st && /^[\w\s:;().,%#-]*$/.test(st[1]) && !/url|expression|@/i.test(st[1])) attrs += ` style="${st[1]}"`;
    out += `<${tag}${attrs}>`;
    stack.push(tag);
  }
  out += text(html.slice(last));
  while (stack.length) out += `</${stack.pop()}>`;
  return out;
}

function json(data, status = 200, extra = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra },
  });
}
function kst(ts) {
  const d = new Date((ts + KST_OFFSET) * 1000);
  return { day: d.toISOString().slice(0, 10), hour: d.getUTCHours() };
}
async function sha256hex(s) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
function b64url(buf) {
  return btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function b64urlDecode(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/');
  while (s.length % 4) s += '=';
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
function getCookie(request, name) {
  const c = request.headers.get('cookie') || '';
  const m = c.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}
function sameOrigin(request, url) {
  const o = request.headers.get('origin');
  if (!o) return true;
  try { return new URL(o).host === url.host; } catch { return false; }
}
function parseJson(v, fallback) {
  try { return v ? JSON.parse(v) : fallback; } catch { return fallback; }
}
const randHex = (n) => [...crypto.getRandomValues(new Uint8Array(n))].map((b) => b.toString(16).padStart(2, '0')).join('');

// ---------- 설정 ----------

async function loadSettings(env, force) {
  if (!env.DB) return new Map();
  if (!force && settingsCache.map && Date.now() - settingsCache.at < SETTINGS_TTL) return settingsCache.map;
  try {
    const { results } = await env.DB.prepare('SELECT key, value FROM settings').all();
    const map = new Map(results.map((r) => [r.key, r.value]));
    settingsCache = { at: Date.now(), map };
    return map;
  } catch (e) {
    return settingsCache.map || new Map();
  }
}

// ---------- 인증 ----------

async function hmacKey(secret) {
  const raw = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(secret + '|js-sports-admin|v1'));
  return crypto.subtle.importKey('raw', raw, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign', 'verify']);
}
async function makeToken(secret) {
  const exp = String(Math.floor(Date.now() / 1000) + SESSION_DAYS * 86400);
  const sig = await crypto.subtle.sign('HMAC', await hmacKey(secret), new TextEncoder().encode(exp));
  return exp + '.' + b64url(sig);
}
async function verifyToken(secret, token) {
  if (!secret || !token) return false;
  const i = token.indexOf('.');
  if (i < 0) return false;
  const exp = token.slice(0, i), sig = token.slice(i + 1);
  if (!/^\d+$/.test(exp) || Number(exp) < Date.now() / 1000) return false;
  try { return await crypto.subtle.verify('HMAC', await hmacKey(secret), b64urlDecode(sig), new TextEncoder().encode(exp)); }
  catch { return false; }
}
async function isAdmin(request, env) {
  const t = getCookie(request, COOKIE);
  return t ? verifyToken(env.ADMIN_PASSWORD, t) : false;
}
function cookieHeader(value, url, maxAge) {
  const secure = url.protocol === 'https:' ? '; Secure' : '';
  return `${COOKIE}=${value}; Path=/; HttpOnly; SameSite=Strict; Max-Age=${maxAge}${secure}`;
}

// ---------- HTML 변환 ----------

function transformHtml(res, s, { origin, track, setVid, secure, page }) {
  const rw = new HTMLRewriter();
  if (s.size) {
    rw.on('[data-cms]', {
      element(el) {
        const key = el.getAttribute('data-cms');
        const v = s.get(key);
        if (v == null) return;
        const fmt = el.getAttribute('data-cms-fmt') || 'rich';
        if (fmt === 'img') {
          const src = safeImg(v);
          if (src) { el.setAttribute('src', src); el.removeAttribute('srcset'); el.removeAttribute('sizes'); }
        } else if (fmt === 'bg') {
          const src = safeImg(v);
          if (src) {
            const st = el.getAttribute('style') || '';
            el.setAttribute('style', st.replace(/background-image\s*:\s*url\([^)]*\)/i, `background-image:url(${src})`));
          }
        } else if (fmt === 'count') {
          const n = String(v).replace(/[^\d.]/g, '');
          if (n) el.setAttribute('data-count', n);
        } else if (fmt === 'icontext') {
          // 아이콘(svg)은 두고 글자만: 아래 text 핸들러가 처리
        } else if (el.getAttribute('data-cms-attr')) {
          el.setAttribute(el.getAttribute('data-cms-attr'), String(v));
        } else if (fmt === 'plain') {
          el.setInnerContent(String(v));
        } else {
          el.setInnerContent(sanitizeRich(String(v)), { html: true });
        }
      },
    });
    // 아이콘이 붙은 버튼 글자 (키마다 따로 등록: 그 요소 안의 글자 조각만 바꾼다)
    for (const [key, v] of s) {
      if (!/:x\d+$/.test(key)) continue;
      let done = false;
      rw.on(`[data-cms="${key}"]`, {
        element() { done = false; },
        text(t) {
          if (done) return;
          if (!t.lastInTextNode) { t.remove(); return; }
          t.replace(esc(v) + ' ', { html: true });
          done = true;
        },
      });
    }
    // 검색 제목·설명을 바꾸면 공유 미리보기(og)도 같이
    const title = s.get(page + ':title'), desc = s.get(page + ':desc');
    if (title) rw.on('meta[property="og:title"]', { element(el) { el.setAttribute('content', title); } });
    if (desc) rw.on('meta[property="og:description"]', { element(el) { el.setAttribute('content', desc); } });

    // 전화번호 바꾸기: tel: 링크 + 글자 속 번호(하이픈 표기)
    const swaps = [];
    for (const [k, def] of Object.entries(PHONES)) {
      const nv = (s.get(k) || '').replace(/[^\d]/g, '');
      if (nv && nv !== def) swaps.push([def, nv]);
    }
    if (swaps.length) {
      for (const [def, nv] of swaps) rw.on(`a[href="tel:${def}"]`, { element(el) { el.setAttribute('href', 'tel:' + nv); } });
      const swapStr = (str) => { let o = str; for (const [def, nv] of swaps) o = o.split(fmtPhone(def)).join(fmtPhone(nv)); return o; };
      rw.on('meta[name="description"], meta[property="og:description"]', { element(el) { const c = el.getAttribute('content'); if (c) el.setAttribute('content', swapStr(c)); } });
      let buf = '';
      rw.onDocument({
        text(t) {
          if (t.removed) { if (t.lastInTextNode) buf = ''; return; }   // 다른 핸들러(관리자 수정 글)가 이미 바꾼 조각은 그대로
          buf += t.text;
          if (!t.lastInTextNode) { t.remove(); return; }
          let out = buf;
          for (const [def, nv] of swaps) out = out.split(fmtPhone(def)).join(fmtPhone(nv));
          buf = '';
          t.replace(out, { html: true });
        },
      });
    }
  }
  for (const sel of ['meta[property="og:image"]', 'meta[name="twitter:image"]']) rw.on(sel, {
    element(el) {
      const c = el.getAttribute('content') || '';
      if (c && !/^https?:\/\//.test(c)) el.setAttribute('content', origin + '/' + c.replace(/^\//, ''));
    },
  });
  if (track) rw.on('head', { element(el) { el.append('<script src="/js/t.js" defer></script>', { html: true }); } });
  const out = rw.transform(res);
  const h = new Headers(out.headers);
  h.delete('etag');
  h.delete('content-length');
  h.set('cache-control', 'no-cache');
  if (new URL(origin).hostname !== PRIMARY_HOST) h.set('x-robots-tag', 'noindex');
  if (setVid) h.append('set-cookie', `${VID_COOKIE}=${setVid}; Path=/; Max-Age=${VID_DAYS * 86400}; HttpOnly; SameSite=Lax${secure ? '; Secure' : ''}`);
  return new Response(out.body, { status: out.status, headers: h });
}

// ---------- 방문 추적 ----------

const BOT_RE = /bot|crawl|spider|slurp|yeti|daumoa|kakaotalk-scrap|facebookexternalhit|headless|lighthouse|pagespeed|preview|monitor|python|curl\/|wget|httpclient|go-http|java\/|okhttp|scrapy|phantom|puppeteer|playwright|gptbot|claudebot|perplexitybot|bytespider|petalbot|semrush|ahrefs|mj12|dataforseo|screaming/i;

function parseUA(ua) {
  const device = /iPad|Tablet|SM-T\d/i.test(ua) ? '태블릿' : /Mobi|Android|iPhone/i.test(ua) ? '모바일' : 'PC';
  const os = /Windows/i.test(ua) ? 'Windows' : /iPhone|iPad|iPod/i.test(ua) ? 'iOS' : /Android/i.test(ua) ? 'Android' : /Mac OS/i.test(ua) ? 'macOS' : /CrOS/.test(ua) ? 'ChromeOS' : /Linux/i.test(ua) ? 'Linux' : '기타';
  const browser = /KAKAOTALK/i.test(ua) ? '카카오톡 인앱' : /Instagram/i.test(ua) ? '인스타그램 인앱' : /NAVER\(inapp/i.test(ua) ? '네이버 앱' : /FBAN|FBAV/.test(ua) ? '페이스북 인앱' : /Whale\//.test(ua) ? '웨일' : /SamsungBrowser/.test(ua) ? '삼성 인터넷' : /Edg\//.test(ua) ? 'Edge' : /OPR\//.test(ua) ? 'Opera' : /Firefox\//.test(ua) ? 'Firefox' : /Chrome\/|CriOS/.test(ua) ? 'Chrome' : /Safari\//.test(ua) ? 'Safari' : '기타';
  return { device, os, browser };
}
const SOURCE_RULES = [
  [/(^|\.)search\.naver\.com$/, '네이버 검색'], [/(^|\.)map\.naver\.com$/, '네이버 지도'], [/(^|\.)place\.naver\.com$/, '네이버 플레이스'],
  [/(^|\.)blog\.naver\.com$/, '네이버 블로그'], [/(^|\.)cafe\.naver\.com$/, '네이버 카페'], [/(^|\.)(naver\.com|naver\.me)$/, '네이버'],
  [/gemini\.google\.com$/, 'Gemini'], [/(^|\.)google\./, '구글'], [/(^|\.)daum\.net$/, '다음'], [/(^|\.)bing\.com$/, 'Bing'],
  [/(^|\.)kakao\.com$/, '카카오톡'], [/(^|\.)daangn\.com$/, '당근'], [/instagram\.com$/, '인스타그램'], [/(^|\.)(facebook\.com|fb\.com|fb\.me)$/, '페이스북'],
  [/(^|\.)(youtube\.com|youtu\.be)$/, '유튜브'], [/(chatgpt\.com|openai\.com)$/, 'ChatGPT'], [/perplexity\.ai$/, 'Perplexity'],
  [/(^|\.)(g2b\.go\.kr|pps\.go\.kr)$/, '나라장터·조달청'], [/(^|\.)(zum\.com|nate\.com|yahoo\.|duckduckgo\.com)/, '기타 검색'],
];
const UTM_NAMES = { naver: '네이버', google: '구글', kakao: '카카오톡', kakaotalk: '카카오톡', instagram: '인스타그램', facebook: '페이스북', youtube: '유튜브', blog: '블로그', sms: '문자', email: '이메일', qr: 'QR코드', flyer: '전단지', catalog: '카탈로그', proposal: '제안서', banner: '현수막', car: '차량 광고' };
function classifySource(refHost, utmSource, ua) {
  if (utmSource) return UTM_NAMES[utmSource.toLowerCase()] || utmSource.slice(0, 40);
  const h = (refHost || '').toLowerCase();
  if (!h) {
    if (/KAKAOTALK/i.test(ua)) return '카카오톡';
    if (/Instagram/i.test(ua)) return '인스타그램';
    if (/NAVER\(inapp/i.test(ua)) return '네이버 앱';
    return '직접 유입';
  }
  for (const [re, name] of SOURCE_RULES) if (re.test(h)) return name;
  return '기타 사이트';
}

async function handleTrack(request, env, ctx, url) {
  if (request.method !== 'POST') return new Response(null, { status: 405 });
  if (!env.DB) return new Response(null, { status: 204 });
  if (!sameOrigin(request, url)) return new Response(null, { status: 403 });
  const ua = request.headers.get('user-agent') || '';
  if (!ua || BOT_RE.test(ua)) return new Response(null, { status: 204 });
  if (await isAdmin(request, env)) return new Response(null, { status: 204 });
  const ip = request.headers.get('cf-connecting-ip') || '0';
  if (env.TRACK_LIMIT) {
    const { success } = await env.TRACK_LIMIT.limit({ key: ip });
    if (!success) return new Response(null, { status: 204 });
  }
  let b;
  try {
    const text = await request.text();
    if (text.length > 4096) return new Response(null, { status: 204 });
    b = JSON.parse(text);
  } catch { return new Response(null, { status: 204 }); }
  if (!b || typeof b !== 'object') return new Response(null, { status: 204 });
  let path = typeof b.p === 'string' ? b.p.split('?')[0].split('#')[0] : '';
  if (!path.startsWith('/') || path.length > 200 || path.startsWith('/admin')) return new Response(null, { status: 204 });
  if (path.length > 1 && path.endsWith('/')) path = path.slice(0, -1);
  if (path === '/index.html' || path === '/index') path = '/';
  path = path.replace(/\.html$/, '');
  const type = b.e ? 'event' : 'view';
  const name = b.e ? String(b.e).slice(0, 40) : null;
  let refHost = null, refUrl = null;
  if (typeof b.r === 'string' && b.r) {
    try {
      const r = new URL(b.r);
      if (!SELF_HOSTS.has(r.hostname.toLowerCase()) && r.hostname.toLowerCase() !== url.hostname.toLowerCase()) {
        refHost = r.hostname.toLowerCase().replace(/^www\./, '');
        refUrl = (r.origin + r.pathname + r.search).slice(0, 500);
      }
    } catch {}
  }
  let utmSource = null, medium = null, campaign = null;
  if (typeof b.q === 'string' && b.q) {
    const q = new URLSearchParams(b.q);
    utmSource = (q.get('utm_source') || '').slice(0, 60) || null;
    medium = (q.get('utm_medium') || '').slice(0, 60) || null;
    campaign = (q.get('utm_campaign') || '').slice(0, 80) || null;
  }
  const source = classifySource(refHost, utmSource, ua);
  const { device, os, browser } = parseUA(ua);
  const cf = request.cf || {};
  const ts = Math.floor(Date.now() / 1000);
  const { day, hour } = kst(ts);
  const cv = getCookie(request, VID_COOKIE);
  const vid = VID_RE.test(cv || '') ? cv : (await sha256hex(day + '|' + ip + '|' + ua)).slice(0, 16);
  const stmt = env.DB.prepare(
    'INSERT INTO hits (ts, day, hour, type, name, path, ref_host, ref_url, source, medium, campaign, device, browser, os, country, city, vid, screen, lang) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
  ).bind(ts, day, hour, type, name, path, refHost, refUrl, source, medium, campaign, device, browser, os, cf.country || null, cf.city ? String(cf.city).slice(0, 60) : null, vid,
    typeof b.s === 'string' ? b.s.slice(0, 20) : null, typeof b.l === 'string' ? b.l.slice(0, 10) : null);
  ctx.waitUntil(stmt.run().catch(() => {}));
  return new Response(null, { status: 204, headers: { 'cache-control': 'no-store' } });
}

// ---------- 상담 신청 ----------

async function handleInquiry(request, env, url) {
  if (request.method !== 'POST') return json({ error: 'method' }, 405);
  if (!env.DB) return json({ error: '접수 서버가 준비되지 않았습니다.' }, 503);
  if (!sameOrigin(request, url)) return json({ error: '잘못된 요청입니다.' }, 403);
  const ip = request.headers.get('cf-connecting-ip') || '0';
  if (env.FORM_LIMIT) {
    const { success } = await env.FORM_LIMIT.limit({ key: ip });
    if (!success) return json({ error: '잠시 후 다시 시도해 주세요.' }, 429);
  }
  let b;
  try { b = await request.json(); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
  if (b && b.hp) return json({ ok: true });   // 허니팟: 사람에게 안 보이는 칸을 채우면 스팸
  const s = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
  const name = s(b.name, 60), tel = s(b.tel, 40), type = s(b.type, 60), msg = s(b.msg, 3000);
  if (!name || !tel) return json({ error: '이름과 연락처를 입력해 주세요.' }, 400);
  if (!/\d{2,}/.test(tel)) return json({ error: '연락처를 확인해 주세요.' }, 400);
  const ts = Math.floor(Date.now() / 1000);
  await env.DB.prepare('INSERT INTO inquiries (ts, day_kst, name, tel, type, msg, page, ua, status) VALUES (?,?,?,?,?,?,?,?,?)')
    .bind(ts, kst(ts).day, name, tel, type === '시설 유형 선택' ? '' : type, msg, s(b.page, 100), (request.headers.get('user-agent') || '').slice(0, 200), 'new').run();
  return json({ ok: true });
}

// ---------- 통계 ----------

function dayStr(d) { return d.toISOString().slice(0, 10); }
function validDay(s) { return typeof s === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(s) && !isNaN(Date.parse(s + 'T00:00:00Z')); }
function shiftDay(s, n) { const d = new Date(s + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return dayStr(d); }

async function handleStats(env, url) {
  const todayKst = kst(Math.floor(Date.now() / 1000)).day;
  let from = url.searchParams.get('from'), to = url.searchParams.get('to');
  if (!validDay(to)) to = todayKst;
  if (!validDay(from)) from = shiftDay(to, -6);
  if (from > to) [from, to] = [to, from];
  let days = Math.round((Date.parse(to) - Date.parse(from)) / 86400000) + 1;
  if (days > 400) { from = shiftDay(to, -399); days = 400; }
  const pFrom = shiftDay(from, -days), pTo = shiftDay(from, -1);
  const now = Math.floor(Date.now() / 1000);
  const D = env.DB;
  const q = (sql, ...args) => D.prepare(sql).bind(...args);
  const rows = await D.batch([
    q(`SELECT COUNT(*) pv, COUNT(DISTINCT vid) uv, COUNT(DISTINCT day || vid) visits FROM hits WHERE type='view' AND day BETWEEN ? AND ?`, from, to),
    q(`SELECT COUNT(*) pv, COUNT(DISTINCT vid) uv, COUNT(DISTINCT day || vid) visits FROM hits WHERE type='view' AND day BETWEEN ? AND ?`, pFrom, pTo),
    q(`SELECT COUNT(*) c, COUNT(DISTINCT vid) u FROM hits WHERE type='event' AND day BETWEEN ? AND ?`, from, to),
    q(`SELECT COUNT(*) c, COUNT(DISTINCT vid) u FROM hits WHERE type='event' AND day BETWEEN ? AND ?`, pFrom, pTo),
    q(`SELECT day, SUM(type='view') pv, COUNT(DISTINCT CASE WHEN type='view' THEN vid END) uv, SUM(type='event') ev FROM hits WHERE day BETWEEN ? AND ? GROUP BY day ORDER BY day`, from, to),
    q(`SELECT hour, SUM(type='view') pv, COUNT(DISTINCT CASE WHEN type='view' THEN vid END) uv FROM hits WHERE day BETWEEN ? AND ? GROUP BY hour ORDER BY hour`, from, to),
    q(`SELECT source, COUNT(*) pv, COUNT(DISTINCT vid) uv FROM hits WHERE type='view' AND day BETWEEN ? AND ? GROUP BY source ORDER BY uv DESC, pv DESC`, from, to),
    q(`SELECT ref_host, ref_url, COUNT(*) pv, COUNT(DISTINCT vid) uv FROM hits WHERE type='view' AND ref_host IS NOT NULL AND day BETWEEN ? AND ? GROUP BY ref_url ORDER BY uv DESC, pv DESC LIMIT 30`, from, to),
    q(`SELECT path, COUNT(*) pv, COUNT(DISTINCT vid) uv FROM hits WHERE type='view' AND day BETWEEN ? AND ? GROUP BY path ORDER BY pv DESC`, from, to),
    q(`SELECT device k, COUNT(DISTINCT vid) uv, COUNT(*) pv FROM hits WHERE type='view' AND day BETWEEN ? AND ? GROUP BY device ORDER BY uv DESC`, from, to),
    q(`SELECT name, COUNT(*) c, COUNT(DISTINCT vid) u FROM hits WHERE type='event' AND day BETWEEN ? AND ? GROUP BY name ORDER BY c DESC`, from, to),
    q(`SELECT COUNT(DISTINCT vid) n FROM hits WHERE ts > ?`, now - 1800),
    q(`SELECT ts, type, name, path, source, ref_host, device, browser, country, city FROM hits ORDER BY ts DESC LIMIT 40`),
    q(`SELECT COUNT(*) n FROM (SELECT vid, MIN(day) d0 FROM hits WHERE type='view' GROUP BY vid) WHERE d0 BETWEEN ? AND ?`, from, to),
    q(`SELECT COUNT(*) n FROM (SELECT vid, MIN(day) d0 FROM hits WHERE type='view' GROUP BY vid) WHERE d0 BETWEEN ? AND ?`, pFrom, pTo),
    q(`SELECT browser k, COUNT(DISTINCT vid) uv, COUNT(*) pv FROM hits WHERE type='view' AND day BETWEEN ? AND ? GROUP BY browser ORDER BY uv DESC`, from, to),
    q(`SELECT os k, COUNT(DISTINCT vid) uv, COUNT(*) pv FROM hits WHERE type='view' AND day BETWEEN ? AND ? GROUP BY os ORDER BY uv DESC`, from, to),
    q(`SELECT city k, COUNT(DISTINCT vid) uv, COUNT(*) pv FROM hits WHERE type='view' AND city IS NOT NULL AND day BETWEEN ? AND ? GROUP BY city ORDER BY uv DESC`, from, to),
    q(`SELECT COUNT(*) n FROM inquiries WHERE day_kst BETWEEN ? AND ?`, from, to),
  ]);
  const r = rows.map((x) => x.results || []);
  const dims = {};
  [['device', 9], ['browser', 15], ['os', 16], ['city', 17]].forEach(([dim, i]) => { dims[dim] = r[i].map((row) => ({ k: row.k || '알 수 없음', uv: row.uv, pv: row.pv })); });
  return json({
    range: { from, to, days, prevFrom: pFrom, prevTo: pTo, today: todayKst },
    totals: { ...r[0][0], events: r[2][0].c, eventUsers: r[2][0].u, newUsers: r[13][0].n, inquiries: r[18][0].n },
    prev: { ...r[1][0], events: r[3][0].c, eventUsers: r[3][0].u, newUsers: r[14][0].n },
    daily: r[4], hourly: r[5], sources: r[6], referrers: r[7], pages: r[8],
    dims, events: r[10], live: r[11][0].n, recent: r[12],
  });
}

async function handleExport(env, url) {
  let from = url.searchParams.get('from'), to = url.searchParams.get('to');
  const today = kst(Math.floor(Date.now() / 1000)).day;
  if (!validDay(to)) to = today;
  if (!validDay(from)) from = shiftDay(to, -29);
  const { results } = await env.DB.prepare(
    'SELECT ts, day, hour, type, name, path, ref_host, ref_url, source, medium, campaign, device, browser, os, country, city, vid, screen, lang FROM hits WHERE day BETWEEN ? AND ? ORDER BY ts LIMIT 50000'
  ).bind(from, to).all();
  const cols = ['ts', 'day', 'hour', 'type', 'name', 'path', 'ref_host', 'ref_url', 'source', 'medium', 'campaign', 'device', 'browser', 'os', 'country', 'city', 'vid', 'screen', 'lang'];
  const cell = (v) => { if (v == null) return ''; const s = String(v); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  const out = [cols.join(',')];
  for (const row of results) out.push(cols.map((c) => cell(row[c])).join(','));
  return new Response('﻿' + out.join('\r\n'), {
    headers: { 'content-type': 'text/csv; charset=utf-8', 'content-disposition': `attachment; filename="js-sports-visits-${from}_${to}.csv"`, 'cache-control': 'no-store' },
  });
}

// ---------- 사진 업로드 (D1 에 base64 로 보관) ----------

const MEDIA_TYPES = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp' };
const MAX_MEDIA_B64 = 1900000;

async function handleMediaUpload(request, env) {
  let body;
  try { body = await request.json(); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
  const ext = MEDIA_TYPES[body && body.type];
  const data = body && typeof body.data === 'string' ? body.data : '';
  if (!ext) return json({ error: 'JPG·PNG·WEBP 사진만 올릴 수 있습니다.' }, 400);
  if (!data || !/^[A-Za-z0-9+/=]+$/.test(data)) return json({ error: '사진 데이터가 올바르지 않습니다.' }, 400);
  if (data.length > MAX_MEDIA_B64) return json({ error: '사진이 너무 큽니다.' }, 413);
  const id = randHex(8) + '.' + ext;
  await env.DB.prepare('INSERT INTO media (id, type, data, size, created_at) VALUES (?,?,?,?,?)')
    .bind(id, body.type, data, Math.floor(data.length * 0.75), Math.floor(Date.now() / 1000)).run();
  return json({ ok: true, url: '/media/' + id });
}
async function serveMedia(request, env, ctx, url) {
  const id = url.pathname.slice('/media/'.length);
  if (!/^[a-f0-9]{16}\.(jpg|png|webp)$/.test(id) || !env.DB) return new Response('not found', { status: 404 });
  const cache = caches.default;
  const hit = await cache.match(request);
  if (hit) return hit;
  const row = await env.DB.prepare('SELECT type, data FROM media WHERE id=?').bind(id).first();
  if (!row) return new Response('not found', { status: 404 });
  const res = new Response(b64urlDecode(row.data), { headers: { 'content-type': row.type, 'cache-control': 'public, max-age=31536000, immutable' } });
  ctx.waitUntil(cache.put(request, res.clone()));
  return res;
}

// ---------- 기구 라인업 데이터 ----------
// 관리자에서 라인업을 고치면 settings 'lexco' (JSON 배열) 로 저장되고, /js/lexco-data.js 를 그것으로 대신 내보낸다.

function cleanLexco(arr) {
  if (!Array.isArray(arr)) return null;
  const s = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
  return arr.slice(0, 300).map((p) => ({
    model: s(p.model, 30), series: p.series === 'free' ? 'free' : 'master', en: s(p.en, 80), ko: s(p.ko, 60),
    size: s(p.size, 120), weight: s(p.weight, 60), block: s(p.block, 60),
    features: (Array.isArray(p.features) ? p.features : []).map((f) => s(f, 120)).filter(Boolean).slice(0, 12),
    file: safeImg(p.file) || (/^[\w.-]+\.(jpg|png|webp)$/i.test(p.file || '') ? p.file : ''),
  })).filter((p) => p.model && p.ko);
}

// ---------- 관리자 API ----------

const KEY_RE = /^[a-z0-9][a-z0-9_.:-]{0,79}$/i;
const MAX_VALUE = 200000;

async function handleAdminApi(request, env, ctx, url) {
  const p = url.pathname.slice('/api/admin/'.length);
  const method = request.method;
  if (p === 'login' && method === 'POST') {
    if (!sameOrigin(request, url)) return json({ error: '잘못된 요청입니다.' }, 403);
    if (!env.ADMIN_PASSWORD) return json({ error: '관리자 비밀번호(ADMIN_PASSWORD)가 아직 설정되지 않았습니다.' }, 503);
    if (env.LOGIN_LIMIT) {
      const { success } = await env.LOGIN_LIMIT.limit({ key: request.headers.get('cf-connecting-ip') || 'x' });
      if (!success) return json({ error: '시도 횟수가 많습니다. 1분 뒤 다시 시도해 주세요.' }, 429);
    }
    let body;
    try { body = await request.json(); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
    const pw = typeof body.password === 'string' ? body.password : '';
    const ok = pw && (await sha256hex('pw|' + pw)) === (await sha256hex('pw|' + env.ADMIN_PASSWORD));
    if (!ok) return json({ error: '비밀번호가 맞지 않습니다.' }, 401);
    return json({ ok: true }, 200, { 'set-cookie': cookieHeader(await makeToken(env.ADMIN_PASSWORD), url, SESSION_DAYS * 86400) });
  }
  if (p === 'logout' && method === 'POST') return json({ ok: true }, 200, { 'set-cookie': cookieHeader('', url, 0) });
  if (!(await isAdmin(request, env))) return json({ error: 'unauthorized' }, 401);
  if (method !== 'GET' && !sameOrigin(request, url)) return json({ error: 'forbidden' }, 403);

  if (p === 'me') return json({ ok: true, db: !!env.DB, host: url.host });
  if (!env.DB) return json({ error: 'D1 데이터베이스(DB)가 연결되지 않았습니다.' }, 503);

  if (p === 'content' && method === 'GET') {
    const s = await loadSettings(env, true);
    return json({ settings: Object.fromEntries(s) });
  }
  if (p === 'content' && (method === 'PUT' || method === 'POST')) {
    let body;
    try { body = await request.json(); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
    const set = body && body.set && typeof body.set === 'object' ? body.set : {};
    const del = Array.isArray(body && body.del) ? body.del : [];
    const now = Math.floor(Date.now() / 1000);
    const stmts = [];
    for (let [k, v] of Object.entries(set)) {
      if (!KEY_RE.test(k)) return json({ error: '잘못된 항목 이름: ' + k }, 400);
      if (typeof v !== 'string') return json({ error: '값은 문자열이어야 합니다: ' + k }, 400);
      if (v.length > MAX_VALUE) return json({ error: '값이 너무 깁니다: ' + k }, 400);
      if (k === 'lexco') { const c = cleanLexco(parseJson(v, null)); if (!c) return json({ error: '라인업 형식이 올바르지 않습니다.' }, 400); v = JSON.stringify(c); }
      stmts.push(env.DB.prepare('INSERT INTO settings (key, value, updated_at) VALUES (?,?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at').bind(k, v, now));
    }
    for (const k of del) {
      if (!KEY_RE.test(k)) return json({ error: '잘못된 항목 이름: ' + k }, 400);
      stmts.push(env.DB.prepare('DELETE FROM settings WHERE key=?').bind(k));
    }
    if (stmts.length) await env.DB.batch(stmts);
    settingsCache = { at: 0, map: null };
    return json({ ok: true, set: Object.keys(set).length, del: del.length });
  }
  if (p === 'inquiries' && method === 'GET') {
    const { results } = await env.DB.prepare('SELECT id, ts, name, tel, type, msg, page, status, memo FROM inquiries ORDER BY ts DESC LIMIT 500').all();
    return json({ items: results });
  }
  if (p === 'inquiries' && method === 'PUT') {
    let b;
    try { b = await request.json(); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
    const id = Number(b && b.id);
    if (!id) return json({ error: 'id' }, 400);
    if (b.delete) { await env.DB.prepare('DELETE FROM inquiries WHERE id=?').bind(id).run(); return json({ ok: true }); }
    const status = ['new', 'done'].includes(b.status) ? b.status : null;
    const memo = typeof b.memo === 'string' ? b.memo.slice(0, 2000) : null;
    await env.DB.prepare('UPDATE inquiries SET status=COALESCE(?, status), memo=COALESCE(?, memo) WHERE id=?').bind(status, memo, id).run();
    return json({ ok: true });
  }
  if (p === 'media' && method === 'POST') return handleMediaUpload(request, env);
  if (p === 'stats' && method === 'GET') return handleStats(env, url);
  if (p === 'export' && method === 'GET') return handleExport(env, url);
  return json({ error: 'not found' }, 404);
}

// ---------- 진입점 ----------

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const p = url.pathname;
    if (url.hostname.startsWith('www.')) return Response.redirect('https://' + url.hostname.slice(4) + p + url.search, 301);
    if (url.protocol === 'http:' && /\.(com|kr|net)$/.test(url.hostname)) return Response.redirect('https://' + url.hostname + p + url.search, 301);

    if (p === '/api/t') return handleTrack(request, env, ctx, url);
    if (p === '/api/inquiry') {
      try { return await handleInquiry(request, env, url); }
      catch (e) { return json({ error: '접수 중 오류가 났습니다. 전화로 문의해 주세요.' }, 500); }
    }
    if (p.startsWith('/api/admin/')) {
      try { return await handleAdminApi(request, env, ctx, url); }
      catch (e) { return json({ error: '서버 오류: ' + String((e && e.message) || e) }, 500); }
    }
    if (p.startsWith('/media/')) return serveMedia(request, env, ctx, url);
    if (p === '/admin.html') return Response.redirect(url.origin + '/admin', 301);
    if (p === '/admin' || p === '/admin/') {
      const res = await env.ASSETS.fetch(new Request(url.origin + '/admin', request));
      const h = new Headers(res.headers);
      h.set('cache-control', 'no-store');
      h.set('x-robots-tag', 'noindex, nofollow');
      return new Response(res.body, { status: res.status, headers: h });
    }
    if (p === '/js/lexco-data.js') {
      const s = await loadSettings(env);
      const v = s.get('lexco');
      if (v) return new Response('window.LEXCO = ' + v.replace(/</g, '\\u003c') + ';\n', { headers: { 'content-type': 'text/javascript; charset=utf-8', 'cache-control': 'no-cache' } });
    }

    const admin = request.headers.get('cookie') ? await isAdmin(request, env) : false;
    const raw = admin && (request.headers.get('x-cms-raw') === '1' || url.searchParams.get('cms') === 'raw');

    let req = request;
    const accept = request.headers.get('accept') || '';
    if (accept.includes('text/html') || raw) {
      const h = new Headers(request.headers);
      h.delete('if-none-match');
      h.delete('if-modified-since');
      req = new Request(request, { headers: h });
    }
    const res = await env.ASSETS.fetch(req);
    const ct = res.headers.get('content-type') || '';
    if (res.status === 200 && ct.includes('text/html')) {
      const s = raw ? new Map() : await loadSettings(env);
      let setVid = null;
      if (!admin && !VID_RE.test(getCookie(request, VID_COOKIE) || '')) setVid = randHex(8);
      const page = (p.replace(/^\//, '').replace(/\.html$/, '').replace(/\/$/, '') || 'index');
      return transformHtml(res, s, { origin: url.origin, track: !admin, setVid, secure: url.protocol === 'https:', page });
    }
    return res;
  },
};
