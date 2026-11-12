// 렌탈 기구 라인업 (LEXCO): 탭 필터 + 카드 그리드 + 사양 모달
(function () {
  var data = window.LEXCO || [];
  var grid = document.getElementById('lxGrid');
  var tabs = document.getElementById('lxTabs');
  if (!grid || !data.length) return;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var IMG = 'img/lexco/';
  var mmOnly = function (s) { return s.replace(/\s*\(.*\)\s*$/, ''); };      // 인치 표기는 모달에서만
  var kgOnly = function (s) { return s.replace(/\s*\(.*\)\s*$/, ''); };

  var render = function (series) {
    grid.innerHTML = data.filter(function (p) { return series === 'all' || p.series === series; }).map(function (p) {
      return '<button type="button" class="lx-card" data-model="' + esc(p.model) + '" aria-label="' + esc(p.ko) + ' 사양 보기">' +
        '<span class="lx-pic"><img src="' + IMG + p.file + '" alt="' + esc(p.ko + ' ' + p.en) + '" loading="lazy"></span>' +
        '<span class="lx-txt"><span class="lx-model">' + esc(p.model) + '</span>' +
        '<span class="lx-ko">' + esc(p.ko) + '</span><span class="lx-en">' + esc(p.en) + '</span>' +
        '<span class="lx-spec">' + esc(kgOnly(p.weight)) + (p.block ? ' · 블록 ' + esc(kgOnly(p.block)) : '') + '</span></span></button>';
    }).join('');
  };
  render('master');

  tabs.addEventListener('click', function (e) {
    var t = e.target.closest('button'); if (!t) return;
    [].forEach.call(tabs.children, function (b) { var on = b === t; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
    render(t.dataset.series);
  });

  // 모달
  var md = document.createElement('div');
  md.className = 'lx-modal'; md.setAttribute('aria-hidden', 'true');
  md.innerHTML = '<div class="lx-bg" data-close></div><div class="lx-box" role="dialog" aria-modal="true" aria-labelledby="lxName">' +
    '<button class="lx-x" data-close aria-label="닫기">×</button><div class="lx-mpic"><img id="lxImg" alt=""></div>' +
    '<div class="lx-mbody"><p class="lx-mseries" id="lxSeries"></p><h3 id="lxName"></h3><p class="lx-men" id="lxEn"></p>' +
    '<dl class="lx-dl" id="lxDl"></dl><h4>특징</h4><ul class="lx-feat" id="lxFeat"></ul>' +
    '<p class="lx-note">제원 및 디자인은 품질향상을 위하여 예고 없이 변경될 수 있습니다.</p>' +
    '<a class="btn btn-red" href="contact.html">렌탈 · 납품 상담</a></div></div>';
  document.body.appendChild(md);
  var last = null;
  var open = function (model) {
    var p = data.find(function (x) { return x.model === model; }); if (!p) return;
    last = document.activeElement;
    md.querySelector('#lxImg').src = IMG + p.file; md.querySelector('#lxImg').alt = p.ko;
    md.querySelector('#lxSeries').textContent = (p.series === 'master' ? 'LEXCO MASTER · 웨이트 머신' : 'LEXCO FREE WEIGHT · 프리웨이트') + ' · ' + p.model;
    md.querySelector('#lxName').textContent = p.ko;
    md.querySelector('#lxEn').textContent = p.en;
    md.querySelector('#lxDl').innerHTML = '<div><dt>제품 크기</dt><dd>' + esc(mmOnly(p.size)) + '</dd></div><div><dt>제품 중량</dt><dd>' + esc(p.weight) + '</dd></div>' +
      (p.block ? '<div><dt>블록 중량</dt><dd>' + esc(p.block) + '</dd></div>' : '');
    md.querySelector('#lxFeat').innerHTML = p.features.map(function (f) { return '<li>' + esc(f) + '</li>'; }).join('');
    md.classList.add('open'); md.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    md.querySelector('.lx-x').focus();
  };
  var close = function () {
    md.classList.remove('open'); md.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (last) last.focus();
  };
  grid.addEventListener('click', function (e) { var c = e.target.closest('.lx-card'); if (c) open(c.dataset.model); });
  md.addEventListener('click', function (e) { if (e.target.hasAttribute('data-close')) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && md.classList.contains('open')) close(); });
})();
