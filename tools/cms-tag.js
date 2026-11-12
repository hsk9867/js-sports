// 관리자 편집용 data-cms 키를 HTML 에 붙인다. (원본 서식은 그대로 두고 시작 태그에 속성만 끼워 넣음)
// 사용: node tools/cms-tag.js            (parse5 필요: npm i parse5@7 를 임시 폴더에 설치 후 NODE_PATH 지정)
//
// 이미 붙은 키는 절대 바꾸지 않는다. 새로 생긴 요소에만 (같은 접두어의 최대 번호 + 1) 을 준다.
// → 나중에 HTML 을 고쳐도 관리자에서 저장해 둔 내용이 엉뚱한 곳으로 옮겨 가지 않는다.
//
// 키 규칙
//   <페이지>:t<n>  글자 (fmt 없음 = rich: 안쪽 HTML, 굵게·줄바꿈 유지)
//   <페이지>:x<n>  아이콘이 같이 있는 버튼 글자 (fmt=icontext: 글자만 바꾸고 아이콘은 둠)
//   <페이지>:c<n>  숫자 카운터 (fmt=count: data-count 값)
//   <페이지>:i<n>  사진 (fmt=img: src)
//   <페이지>:b<n>  배경 사진 (fmt=bg: style 의 url())
//   <페이지>:title / <페이지>:desc   검색 제목 · 설명
//   hd:… / ft:…   머리말(메뉴) · 꼬리말 — 모든 페이지 공통
const fs = require('fs');
const path = require('path');
const { parse } = require('parse5');

const ROOT = path.resolve(__dirname, '..');
const PAGES = ['index', 'about', 'business', 'service', 'rental', 'operation', 'portfolio', 'contact'];
const INLINE = new Set(['b', 'strong', 'em', 'i', 'small', 'span', 'mark', 'sup', 'sub', 'u', 'br']);
const SKIP = new Set(['script', 'style', 'noscript', 'svg', 'select', 'option', 'textarea', 'input', 'template', 'iframe', 'video', 'canvas']);

const attr = (n, k) => { const a = (n.attrs || []).find((x) => x.name === k); return a ? a.value : null; };
const kids = (n) => n.childNodes || [];
const isText = (n) => n.nodeName === '#text';
const hasText = (n) => isText(n) ? n.value.trim() !== '' : kids(n).some(hasText);
const hasCounter = (n) => attr(n, 'data-count') != null || kids(n).some((c) => c.tagName && hasCounter(c));

// 글자만 안쪽에 있고(인라인 서식 허용) 블록·아이콘·카운터가 없는 요소
function isRich(n) {
  if (!n.tagName || SKIP.has(n.tagName)) return false;
  if (!hasText(n) || hasCounter(n)) return false;
  const ok = (c) => isText(c) || c.nodeName === '#comment' || (c.tagName && INLINE.has(c.tagName) && kids(c).every(ok));
  return kids(n).every(ok);
}
// 글자 하나 + svg 아이콘(들)만 있는 버튼·링크
function isIconText(n) {
  if (!n.tagName || SKIP.has(n.tagName)) return false;
  const ch = kids(n).filter((c) => !(isText(c) && !c.value.trim()) && c.nodeName !== '#comment');
  const texts = ch.filter(isText), svgs = ch.filter((c) => c.tagName === 'svg');
  return texts.length === 1 && svgs.length >= 1 && texts.length + svgs.length === ch.length;
}

function tagPage(page) {
  const file = path.join(ROOT, page + '.html');
  const src = fs.readFileSync(file, 'utf8');
  const doc = parse(src, { sourceCodeLocationInfo: true });
  const inserts = [];   // [offset, text]
  const max = {};       // 접두어별 최대 번호
  const pending = [];   // 새 키가 필요한 요소 [node, prefix, kind, extra]

  const existing = (n) => attr(n, 'data-cms');
  const note = (k) => { const m = k.match(/^(.*:[a-z])(\d+)$/); if (m) max[m[1]] = Math.max(max[m[1]] || 0, Number(m[2])); };

  function want(n, prefix, kind, extra) {
    const k = existing(n);
    if (k) { note(k); return; }
    pending.push([n, prefix, kind, extra]);
  }

  function walk(n, scope) {
    if (!n.tagName) { kids(n).forEach((c) => walk(c, scope)); return; }
    if (SKIP.has(n.tagName)) return;
    if (n.tagName === 'header') scope = 'hd';
    if (n.tagName === 'footer') scope = 'ft';
    const prefix = scope || page;

    if (n.tagName === 'title') { if (!existing(n)) inserts.push([n.sourceCodeLocation.startTag.endOffset - 1, ` data-cms="${page}:title" data-cms-fmt="plain"`]); return; }
    if (n.tagName === 'meta' && attr(n, 'name') === 'description') { if (!existing(n)) inserts.push([n.sourceCodeLocation.startTag.endOffset - (src[n.sourceCodeLocation.startTag.endOffset - 2] === '/' ? 2 : 1), ` data-cms="${page}:desc" data-cms-attr="content"`]); return; }
    if (n.tagName === 'img') { want(n, prefix + ':i', 'img'); return; }
    const st = attr(n, 'style') || '';
    if (/background-image\s*:\s*url\(/i.test(st)) want(n, prefix + ':b', 'bg');
    if (attr(n, 'data-count') != null) { want(n, prefix + ':c', 'count'); return; }
    if (isRich(n)) { want(n, prefix + ':t', 'rich'); return; }
    if (isIconText(n)) { want(n, prefix + ':x', 'icontext'); return; }
    kids(n).forEach((c) => walk(c, scope));
  }
  walk(doc, null);

  for (const [n, prefix, kind] of pending) {
    const no = (max[prefix] = (max[prefix] || 0) + 1);
    const fmt = kind === 'rich' ? '' : ` data-cms-fmt="${kind}"`;
    const loc = n.sourceCodeLocation.startTag;
    const end = loc.endOffset - (src[loc.endOffset - 2] === '/' ? 2 : 1);
    inserts.push([end, ` data-cms="${prefix}${no}"${fmt}`]);
  }
  if (!inserts.length) return { page, added: 0 };
  inserts.sort((a, b) => b[0] - a[0]);
  let out = src;
  for (const [off, text] of inserts) out = out.slice(0, off) + text + out.slice(off);
  fs.writeFileSync(file, out);
  return { page, added: inserts.length };
}

const res = PAGES.map(tagPage);
console.log(res.map((r) => `${r.page} +${r.added}`).join('  '));
