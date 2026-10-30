# -*- coding: utf-8 -*-
"""사업분야 페이지 정의 — build_sub.py 가 import 해서 PAGES 에 추가"""

def nav(items):
    return ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)

MARQUEE = '''
<div class="marquee" aria-hidden="true"><div class="track">
  <span>TOTAL SPORTS SERVICE</span><i></i><span>운동기구 납품 · A/S</span><i></i><span>시설 정기점검</span><i></i><span>기구 렌탈 · 리스</span><i></i><span>위탁운영 · 컨설팅 · 인테리어</span><i></i>
  <span>TOTAL SPORTS SERVICE</span><i></i><span>운동기구 납품 · A/S</span><i></i><span>시설 정기점검</span><i></i><span>기구 렌탈 · 리스</span><i></i><span>위탁운영 · 컨설팅 · 인테리어</span><i></i>
</div></div>
'''

def area(id_, no, en, title_html, lead_html, items, img, link, link_txt, flip=False, dark=False):
    lis = ''.join(f'<li><span class="split-w">{t}</span></li>' for t in items)
    cls = 'area' + (' flip' if flip else '') + (' dark' if dark else '')
    return f'''
<section class="{cls}" id="{id_}">
  <div class="wrap">
    <div class="area-txt">
      <div class="area-no"><span class="outline">{no}</span><em>{en}</em></div>
      <h2 class="split">{title_html}</h2>
      <p class="lead split-w">{lead_html}</p>
      <ul class="area-list">{lis}</ul>
      <a href="{link}" class="btn {'btn-ghost' if dark else 'btn-dark'} rv">{link_txt} <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
    </div>
    <div class="area-pic rv"><img src="{img}" alt="{en}"><span class="tag">{no}</span></div>
  </div>
</section>'''

BODY = '''
<section class="intro">
  <div class="wrap">
    <p class="kicker split-w">JS SPORTS BUSINESS</p>
    <h2 class="split big">운동시설에 필요한 <b class="hl">모든 것</b>을<br>한 곳에서 <b class="hl">컨설팅</b>합니다</h2>
    <p class="split-w lead">납품과 A/S, 정기점검, 렌탈·리스, 위탁운영과 인테리어까지. 개인 피트니스 센터부터 기업체·아파트·학교·관공서까지 다양한 현장에서 토탈 스포츠 서비스를 제공합니다.</p>
    <ul class="jump">
      <li><a href="#supply"><b>01</b>운동기구 납품 · A/S</a></li>
      <li><a href="#inspect"><b>02</b>시설 정기점검</a></li>
      <li><a href="#rental"><b>03</b>기구 렌탈 · 리스</a></li>
      <li><a href="#consult"><b>04</b>위탁운영 · 컨설팅 · 인테리어</a></li>
    </ul>
  </div>
</section>
''' + MARQUEE + area(
    'supply', '01', 'SUPPLY & A/S',
    '조달청 등록 기구를<br><b class="hl">직접 납품</b>하고<br><b class="hl">직접 수리</b>합니다',
    '전문 엔지니어 구성으로 단순한 헬스용품점과 달리 매장 다이렉트 A/S가 가능합니다. 타 업체에서 수리 불가한 국산 기구와 수입 기구까지 완벽하게 수리하는 기술력을 보유하고 있습니다.',
    ['조달청 · 나라장터 등록 기구 취급, 등록 업체', '700평대 창고형 매장에서 전시 · 시연 후 구매', '국산 · 수입 브랜드 구분 없는 원스톱 A/S', 'A/S 접수 후 1~2일 내 신속 방문'],
    'img/install-1.jpg', 'portfolio.html', '납품 실적 보기'
) + area(
    'inspect', '02', 'INSPECTION',
    '월 1~2회 방문,<br><b class="hl">안전사고</b>를<br>미리 막습니다',
    '위탁운영으로 전문인력이 상주하지 않는 체육시설도 연간 계약으로 정기점검을 받을 수 있습니다. A타입(점검 수수료형)과 B타입(A/S 전액 책임형) 중 선택하세요.',
    ['유산소기구 전장류 · 벨트 · 오일 점검', '웨이트기구 와이어 · 롤러 · 패드 · 베어링 점검', '매 방문 시 점검차트 작성 및 보고', '점검기간 외 A/S도 1~2일 내 방문'],
    'img/cardio-2.jpg', 'service.html', '정기점검 프로그램 보기', flip=True, dark=True
) + area(
    'rental', '03', 'RENTAL & LEASE',
    '<b class="hl">목돈 ZERO</b>,<br>클럽용 기구를<br>부담 없이 렌탈',
    '노후된 기구로 인한 안전사고와 잦은 유상 A/S로 고민하고 계시다면, 최소한의 비용으로 운동기구를 렌탈하세요. 런닝머신 1대부터 피트니스센터 인테리어까지 컨설팅해 드립니다.',
    ['초기비용 없이 고가의 클럽용 제품 이용', '계약기간 내 정기점검과 A/S 무료', '렌탈 종료 시 소유권 이전 또는 반납 선택', '장기렌탈 시 바닥공사 · 기초 인테리어 무상'],
    'img/rental-co-1.jpg', 'rental.html', '렌탈 프로그램 보기'
) + area(
    'consult', '04', 'OPERATION & INTERIOR',
    '운영부터 시공까지,<br><b class="hl">한 팀</b>이<br>책임집니다',
    '체육시설 위탁운영, 전문강사진 및 인력파견, 헬스장 건축 · 시공 · 견적과 CAD 계획까지. 시설관리팀 · 영업 컨설팅팀 · 인테리어팀이 하나의 현장을 함께 만듭니다.',
    ['체육시설 위탁운영 및 지점 운영 관리', '아파트 · 관공서 전문강사 및 인력파견', '헬스장 건축 / 시공 / 견적, CAD 계획', '인테리어 견적 및 컨설팅'],
    'img/facility.jpg', 'about.html#process', '팀 프로세스 보기', flip=True, dark=True
) + MARQUEE + '''
<section class="section numbers">
  <div class="wrap">
    <div class="stats stats4 rv">
      <div class="stat"><b><span data-count="700">0</span><small>평</small></b><span>창고형 매장<br>전시·시연 가능</span></div>
      <div class="stat"><b><span data-count="2012">0</span></b><span>설립 이후<br>충남 대표 전문업체</span></div>
      <div class="stat"><b><span data-count="1">0</span>~<span data-count="2">0</span><small>일</small></b><span>A/S 접수 후<br>신속 방문</span></div>
      <div class="stat"><b class="pop">전국</b><span>충남 · 서울경기<br>전국 관리대행</span></div>
    </div>
  </div>
</section>
'''

PAGE = dict(
    title='사업분야', desc='JS스포츠 사업분야 - 운동기구 납품·A/S, 시설 정기점검, 기구 렌탈·리스, 체육시설 위탁운영·컨설팅·인테리어',
    on='business', visual='img/hero-2.jpg', crumb='사업분야', h1='사업분야',
    sub='납품 · A/S · 정기점검 · 렌탈 · 위탁운영 · 인테리어, 토탈 스포츠 서비스',
    subnav=nav([('supply', '운동기구 납품 · A/S'), ('inspect', '시설 정기점검'), ('rental', '기구 렌탈 · 리스'), ('consult', '위탁운영 · 컨설팅 · 인테리어')]),
    body=BODY,
)
