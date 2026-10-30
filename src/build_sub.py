# -*- coding: utf-8 -*-
"""Generates sub pages with shared header/footer. Run: python src/build_sub.py (from js-sports root)"""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | JS스포츠</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="progress"></div>
<header class="header sub">
  <div class="wrap">
    <a href="index.html" class="logo" aria-label="JS스포츠 홈"><img class="lg-light" src="img/logo-light.png" alt="JS SPORTS"><img class="lg-dark" src="img/logo-dark.png" alt="JS SPORTS"></a>
    <nav class="gnb">
      <a href="about.html"{on_about}>회사소개</a>
      <a href="index.html#biz">사업분야</a>
      <a href="service.html"{on_service}>시설점검</a>
      <a href="rental.html"{on_rental}>기구렌탈</a>
      <a href="portfolio.html"{on_portfolio}>실적현황</a>
      <a href="contact.html"{on_contact}>상담문의</a>
    </nav>
    <div class="hd-right">
      <a href="tel:16889634" class="hd-tel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>1688-9634</a>
      <a href="contact.html" class="hd-btn">상담신청</a>
      <button class="ham" aria-label="전체메뉴"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="fullmenu">
  <div class="wrap">
    <div class="bigs">
      <a href="about.html"><span>01</span>회사소개</a>
      <a href="index.html#biz"><span>02</span>사업분야</a>
      <a href="service.html"><span>03</span>시설 정기점검</a>
      <a href="rental.html"><span>04</span>기구 렌탈</a>
      <a href="portfolio.html"><span>05</span>실적현황</a>
      <a href="contact.html"><span>06</span>상담문의</a>
    </div>
    <div class="info">
      <span class="lab">CONSULTING</span>
      <strong><a href="tel:16889634">1688-9634</a></strong>
    </div>
  </div>
</div>
<div style="height:80px"></div>
<section class="subvisual">
  <div class="bg" style="background-image:url({visual})"></div>
  <div class="wrap">
    <ul class="crumb"><li>HOME</li><li>{crumb}</li></ul>
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
</section>
<div class="subnav"><div class="wrap"><ul>{subnav}</ul></div></div>
'''

FOOT = '''
<section class="cta">
  <div class="wrap">
    <div>
      <h2>운동시설, 고민하지 말고 전화하세요</h2>
      <p>전문인력이 직접 방문하여 공간에 맞는 컨설팅과 견적을 상담해 드립니다.</p>
    </div>
    <a href="tel:16889634" class="tel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg><span>1688-9634<small style="display:block;margin-top:10px">컨설팅상담 · 평일 09:00 – 18:00</small></span></a>
  </div>
</section>
<footer class="footer">
  <div class="wrap">
    <div class="legal">
      <ul><li><a href="#">개인정보처리방침</a></li><li><a href="#">이메일주소 무단수집거부</a></li><li><a href="contact.html">찾아오시는 길</a></li></ul>
      <span>www.js-sports.kr</span>
    </div>
    <div class="grid">
      <div>
        <a href="index.html" class="logo"><img class="lg-dark" src="img/logo-dark.png" alt="JS SPORTS"></a>
        <p class="copy"><b>JS스포츠</b> · 대표 송종수 · 설립 2012. 03. 20<br>COPYRIGHT © JS SPORTS. ALL RIGHTS RESERVED.</p>
      </div>
      <div class="cols">
        <div><h4>회사소개</h4><ul><li><a href="about.html#greeting">인사말</a></li><li><a href="about.html#overview">회사개요</a></li><li><a href="about.html#warehouse">700평 창고</a></li><li><a href="about.html#process">팀 프로세스</a></li></ul></div>
        <div><h4>시설점검</h4><ul><li><a href="service.html#program">정기점검 프로그램</a></li><li><a href="service.html#cardio">유산소 기구관리</a></li><li><a href="service.html#weight">웨이트 기구관리</a></li><li><a href="service.html#sheet">점검표 관리</a></li></ul></div>
        <div><h4>기구렌탈</h4><ul><li><a href="rental.html#program">렌탈 프로그램</a></li><li><a href="rental.html#case-apt">사례 · 아파트</a></li><li><a href="rental.html#case-corp">사례 · 회사</a></li></ul></div>
        <div><h4>실적 · 문의</h4><ul><li><a href="portfolio.html">실적현황</a></li><li><a href="portfolio.html#photos">납품 사진</a></li><li><a href="contact.html">상담문의</a></li></ul></div>
      </div>
      <div class="addr">
        <b>1688-9634</b>
        충남 아산시 배방읍 고불로 690-7<br>
        FAX 041-534-0126 · H.P <a href="tel:01092298051">010-9229-8051</a>
      </div>
    </div>
  </div>
</footer>
<button class="totop" aria-label="맨 위로"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<script src="js/main.js"></script>
</body>
</html>
'''

def nav(items):
    return ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)

PAGES = {}

# ---------------- ABOUT ----------------
PAGES['about.html'] = dict(
    title='회사소개', desc='충남 유일 토탈 스포츠 서비스 전문기업 JS스포츠 인사말, 회사개요, 700평 창고, 팀 프로세스',
    on='about', visual='img/hero-2.jpg', crumb='회사소개', h1='회사소개',
    sub='체육시설 위탁운영부터 인력파견, 헬스기구 납품과 렌탈·리스, 인테리어까지 모두 컨설팅하는 충남 유일 전문업체',
    subnav=nav([('greeting','인사말'),('overview','회사개요'),('warehouse','700평 창고'),('process','팀 프로세스')]),
    body='''
<section class="section" id="greeting">
  <div class="wrap greet">
    <div class="pic rv"><img src="img/grip.jpg" alt="JS스포츠"><div class="badge"><small>SINCE 2012</small>신뢰받는 기업<br>고객만족도 1위</div></div>
    <div class="rv d1">
      <span class="eyebrow">Greeting</span>
      <h2>신뢰받는 기업, 고객만족도 1위<br><em>JS스포츠</em>입니다</h2>
      <div class="body">
        <p>안녕하십니까? JS스포츠 대표 송종수입니다.</p>
        <p>저희 JS스포츠는 운동기구 납품 및 A/S, 헬스기구 리스·렌탈, 위탁운영, 전문강사진 및 인력 파견 전문 업체입니다.</p>
        <p>현재 충남(천안·아산 외) 서울·경기 및 전국의 많은 일반 피트니스 센터, 관공서, 기업체, 아파트 단지 내 피트니스 등의 관리대행 및 A/S를 진행하고 있습니다. 납품하는 기구는 조달청 및 나라장터에 등록된 기구를 취급하며, 저희 업체 또한 조달청과 나라장터에 등록되어 있습니다.</p>
        <p>전문 엔지니어 구성으로 단순한 일반 헬스용품점과 달리 매장 다이렉트 A/S가 가능하고, 타 업체에서 수리 불가한 국산 기구와 수입 기구까지도 완벽하게 수리할 수 있는 기술력을 보유하고 있습니다.</p>
        <p>글로벌 시대에 걸맞게 앞으로 더욱 노력하여 신뢰받는 업체로 거듭날 수 있도록 저희 임직원 모두 약속드립니다.</p>
      </div>
      <div class="sign">JS스포츠 대표 <b>송 종 수</b></div>
    </div>
  </div>
</section>

<section class="section alt" id="overview">
  <div class="wrap">
    <div class="sec-head left rv"><span class="eyebrow">Overview</span><h2>회사개요</h2></div>
    <div class="ov">
      <div class="pic rv"><img src="img/gym-dark.jpg" alt="JS스포츠 시설" style="object-position:center 40%"></div>
      <dl class="dl rv d1">
        <div><dt>회사명</dt><dd>JS스포츠</dd></div>
        <div><dt>대표</dt><dd>송종수</dd></div>
        <div><dt>설립일</dt><dd>2012년 3월 20일</dd></div>
        <div><dt>본사</dt><dd>충남 아산시 배방읍 고불로 690-7</dd></div>
        <div><dt>컨설팅상담</dt><dd>1688-9634</dd></div>
        <div><dt>FAX</dt><dd>041-534-0126</dd></div>
        <div><dt>H.P</dt><dd>010-9229-8051</dd></div>
        <div><dt>홈페이지</dt><dd>www.js-sports.kr</dd></div>
        <div><dt>사업분야</dt><dd>운동기구 납품·A/S, 시설 정기점검, 헬스기구 렌탈·리스, 체육시설 위탁운영, 전문강사·인력파견, 헬스장 인테리어·시공</dd></div>
        <div><dt>등록</dt><dd>조달청 · 나라장터 등록업체</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="band" id="warehouse">
  <div class="bg" style="background-image:url(img/warehouse-2.jpg)"></div>
  <div class="wrap">
    <div class="rv">
      <span class="eyebrow">Warehouse</span>
      <h2>충청권 최대 규모<br><em>700평대</em> 웨이트기구<br>수입 창고 보유</h2>
      <p>JS스포츠는 충청권 최대 규모의 국내외 웨이트기구를 수입하는 700평대 창고형 매장을 운영하고 있습니다. 충청권 유일한 외산 브랜드 웨이트기구 수입업체로, A/S가 가능하고 매장 전시 및 시연이 가능합니다.</p>
    </div>
    <div class="stats rv d2" style="grid-template-columns:1fr">
      <div class="stat"><b>700<small>평</small></b><span>각종 웨이트기구 수입 창고 보유</span></div>
      <div class="stat"><b>유일</b><span>충청권 유일, 외산 브랜드 웨이트기구 수입 및 A/S 가능 업체</span></div>
      <div class="stat"><b>전시 · 시연</b><span>웨이트기구 매장 전시 및 시연 가능</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="feat3">
      <div class="fcard rv d1"><div class="pic"><img src="img/warehouse-1.jpg" alt="창고 외부"></div><div class="txt"><span class="no">01</span><h3>700평대 창고형 매장</h3><p>국내외 웨이트기구가 상시 입고되는 충청권 최대 규모 창고형 매장입니다.</p></div></div>
      <div class="fcard rv d2"><div class="pic"><img src="img/warehouse-3.jpg" alt="수입 기구 입고"></div><div class="txt"><span class="no">02</span><h3>외산 브랜드 직수입</h3><p>충청권 유일의 외산 웨이트기구 수입업체. 중간 유통 없이 합리적인 가격으로 공급합니다.</p></div></div>
      <div class="fcard rv d3"><div class="pic"><img src="img/warehouse-2.jpg" alt="창고 전시"></div><div class="txt"><span class="no">03</span><h3>전시 · 시연 · A/S</h3><p>매장에서 직접 보고, 사용해 보고, 수리까지. 전문 엔지니어가 상주합니다.</p></div></div>
    </div>
  </div>
</section>

<section class="team" id="process">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Team Process</span>
      <h2>JS스포츠는 체계적으로 팀을 만들어 운영합니다</h2>
    </div>
    <div class="team-grid">
      <div class="tcard rv d1">
        <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        <span class="no">TEAM 01</span><h3>시설관리팀<small>FACILITY MANAGEMENT</small></h3>
        <ul><li>운동시설 점검</li><li>A/S 매뉴얼 관리</li><li>지점관리 및 방문 순회</li><li>지점 운영 관리</li></ul>
      </div>
      <div class="tcard rv d2">
        <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M3 3h18v4H3zM3 10h18v11H3zm4 3v5h10v-5z"/></svg>
        <span class="no">TEAM 02</span><h3>영업 컨설팅팀<small>SALES CONSULTING</small></h3>
        <ul><li>체육시설 컨설팅</li><li>아파트 및 관공서 인력파견</li><li>헬스기구 구매 및 렌탈</li></ul>
      </div>
      <div class="tcard rv d3">
        <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M3 21V8l9-5 9 5v13h-6v-6H9v6z"/></svg>
        <span class="no">TEAM 03</span><h3>인테리어팀<small>INTERIOR &amp; CONSTRUCTION</small></h3>
        <ul><li>헬스장 건축 / 시공 / 견적</li><li>CAD 계획</li><li>인테리어 견적 및 컨설팅</li></ul>
      </div>
    </div>
  </div>
</section>
''')

# ---------------- SERVICE ----------------
PAGES['service.html'] = dict(
    title='시설 정기점검', desc='JS스포츠 운동시설 관리점검 프로그램 - A타입·B타입 정기점검, 유산소·웨이트 기구관리, 점검표 관리',
    on='service', visual='img/cardio-2.jpg', crumb='시설 정기점검', h1='운동시설 관리점검 프로그램',
    sub='2가지 타입의 체계화된 정기점검 프로그램으로 안전사고에 대비하세요',
    subnav=nav([('program','정기점검 프로그램'),('cardio','유산소 기구관리'),('weight','웨이트 기구관리'),('sheet','시설 및 점검표 관리')]),
    body='''
<section class="section" id="program">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Program</span>
      <h2>시설 정기점검 프로그램</h2>
      <p>JS스포츠는 기구 및 시설관리 정기점검 프로그램으로 안전사고를 대비합니다.</p>
    </div>
    <div class="points rv" style="margin-bottom:24px">
      <div class="point"><b>WHY 01</b><h3>체육공동시설은 안전이 최우선입니다</h3><p>위탁운영을 하여 전문인력이 상주하지 않는 체육시설의 경우, 자체 관리인력으로 기구 A/S를 하거나 사설 A/S 인력을 요청하여 해결하는 경우가 대부분입니다. 하지만 이 경우 정확한 A/S와 신속한 처리가 어려운 단점이 생깁니다.</p></div>
      <div class="point"><b>WHY 02</b><h3>연간 계약으로 사전에 예방합니다</h3><p>이러한 문제점을 사전에 예방하고자 JS스포츠는 연간 계약을 맺고 A타입·B타입 프로그램에 맞춰 시설물 정기점검 서비스를 진행합니다. 점검기간 외에 발생하는 A/S도 1~2일 안에 빠르게 방문하여 진행 가능합니다.</p></div>
    </div>
    <div class="types">
      <div class="type rv d1">
        <span class="lab">A TYPE</span>
        <h3>월 정기점검 수수료형</h3>
        <p>월 정기점검 수수료를 지불하고, 기구 A/S 비용은 발생 시 별도로 청구되는 기본형 프로그램입니다.</p>
        <ul><li>고객 요청에 따라 월 1회 또는 2회 전문 엔지니어 방문</li><li>유산소 · 웨이트 기구 작동여부 및 전장류 점검</li><li>점검표 작성 및 추후 필요 사항 보고</li><li>기구 A/S 비용 별도 청구</li></ul>
        <span class="big">A</span>
      </div>
      <div class="type b rv d2">
        <span class="lab">B TYPE</span>
        <h3>A/S 전액 책임형</h3>
        <p>정기점검 계약기간 동안 체육공동시설에서 발생하는 모든 A/S 비용을 JS스포츠가 책임지는 안심형 프로그램입니다.</p>
        <ul><li>월 1~2회 전문 엔지니어 정기 방문</li><li>계약기간 내 발생하는 모든 A/S 비용 업체 부담</li><li>점검기간 외 A/S도 1~2일 내 방문</li><li>국산 · 수입 브랜드 구분 없이 원스톱 처리</li></ul>
        <span class="big">B</span>
      </div>
    </div>
    <p class="note rv">※ 납품되어 있는 기구 브랜드 및 연식에 따라 견적이 상이합니다. 정확한 견적은 현장 방문 후 안내드립니다.</p>
  </div>
</section>

<section class="section alt" id="cardio">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>CARDIO</small>유산소기구 관리</h3>
      <p>유산소기구(런닝머신 및 싸이클)의 작동여부 및 전장류 점검. 주기적으로 관리가 안 된 런닝머신과 싸이클은 인버터류(전장부) 및 먼지와 오염으로 오작동 발생 시 전원 꺼짐, 순간 멈춤으로 인한 낙하사고, 전원부 과부하로 인한 화재 발생의 위험이 있습니다. 정기적인 오일류 도포와 청소작업으로 안전사고 예방 및 고장률 최소화를 목적으로 합니다.<br><br><strong style="color:var(--red)">매월 1~2회 정기점검 방문</strong></p>
    </div>
    <div class="feat3">
      <div class="fcard rv d1"><div class="pic"><img src="img/cardio-1.jpg" alt="유산소기구 전장류 관리"></div><div class="txt"><span class="no">CHECK 01</span><h3>유산소기구 전장류 관리</h3><p>인버터 · 제어보드 등 전장부 점검과 과부하 예방</p></div></div>
      <div class="fcard rv d2"><div class="pic"><img src="img/cardio-2.jpg" alt="유산소기구 세부청소"></div><div class="txt"><span class="no">CHECK 02</span><h3>유산소기구 세부청소</h3><p>내부 먼지 · 오염 제거로 오작동과 화재 위험 차단</p></div></div>
      <div class="fcard rv d3"><div class="pic"><img src="img/cardio-3.jpg" alt="벨트류 점검 및 오일 도포"></div><div class="txt"><span class="no">CHECK 03</span><h3>벨트류 점검 및 오일 도포</h3><p>벨트 마모 확인과 정기적인 오일 도포로 수명 연장</p></div></div>
    </div>
  </div>
</section>

<section class="section" id="weight">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>WEIGHT</small>웨이트기구 관리</h3>
      <p>웨이트기구의 작동여부 및 전장류 점검. 운동기구는 항상 안전사고에 대비하여 각종 손잡이류와 와이어 상태를 주기적으로 점검해야 합니다. 미관상 보기 안 좋은 레자 부분도 정기적으로 교체해 주어야 합니다.<br><br><strong style="color:var(--red)">매월 1~2회 정기점검 방문</strong></p>
    </div>
    <div class="feat3">
      <div class="fcard rv d1"><div class="pic"><img src="img/weight-1.jpg" alt="와이어 및 롤러부위 점검"></div><div class="txt"><span class="no">CHECK 01</span><h3>와이어 및 롤러부위 점검</h3><p>와이어 피복 손상 · 롤러 마모 점검으로 끊어짐 사고 예방</p></div></div>
      <div class="fcard rv d2"><div class="pic"><img src="img/weight-2.jpg" alt="패드류 및 손잡이 고무 점검"></div><div class="txt"><span class="no">CHECK 02</span><h3>패드류 및 손잡이 고무 점검</h3><p>레자 · 패드 · 그립 고무 상태 확인 및 교체</p></div></div>
      <div class="fcard rv d3"><div class="pic"><img src="img/weight-3.jpg" alt="베어링 및 작동부 오일 점검"></div><div class="txt"><span class="no">CHECK 03</span><h3>베어링 및 작동부 오일 점검</h3><p>각종 베어링 · 체인 · 작동부 윤활 상태 점검</p></div></div>
    </div>
  </div>
</section>

<section class="section dark" id="sheet">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Check Sheet</span>
      <h2>시설 및 점검표 관리</h2>
      <p>전문인력이 주기적으로 관리하는 시설 점검. 체계적인 관리를 위해 점검표를 작성해 기구들의 수명을 관리하고<br>사용자들의 편의와 안전을 위해 최선을 다합니다.</p>
    </div>
    <div class="ov">
      <div class="pic rv"><img src="img/facility.jpg" alt="시설 점검"></div>
      <div class="rv d1" style="display:grid;gap:20px">
        <div class="point" style="background:var(--ink-2);border-color:rgba(255,255,255,.1);color:#fff"><b>POINT 1</b><h3>매 방문 시 점검차트 작성</h3><p style="color:var(--steel-3)">매 방문 시 점검차트로 그날 점검내용과 추후 필요한 부분을 작성합니다. 시설관리는 회원들의 안전 및 기구들의 수명과 직결되는 부분이기에 주기적인 안전점검과 관리가 필요합니다. JS스포츠는 전문인력의 주기적인 관리로 사용자들의 안전을 최우선시합니다.</p></div>
        <div class="point" style="background:var(--ink-2);border-color:rgba(255,255,255,.1);color:#fff"><b>POINT 2</b><h3>어떤 브랜드든 원스톱 A/S</h3><p style="color:var(--steel-3)">관리 시설마다 다른 브랜드의 운동기구 및 유산소기구가 설치되어 있습니다. JS스포츠는 기구 본사와 달리 A/S 진행 시 원스톱 시스템으로 어떠한 브랜드(국산 · 수입)도 본사 대비 빠르고 저렴하게 A/S 진행이 가능합니다.</p></div>
      </div>
    </div>
  </div>
</section>
''')

# ---------------- RENTAL ----------------
PAGES['rental.html'] = dict(
    title='기구 렌탈', desc='JS스포츠 운동기구 렌탈 프로그램 - 목돈 ZERO, 정기점검, A/S 무료, 소유권 이전. 아파트·기업체 렌탈 시공사례',
    on='rental', visual='img/rental-co-1.jpg', crumb='기구 렌탈', h1='운동기구 렌탈 및 납품',
    sub='런닝머신 1대부터 피트니스센터 인테리어까지, 최소한의 비용으로 운동기구를 이용하세요',
    subnav=nav([('program','렌탈 프로그램'),('case-apt','시공사례 · 아파트'),('case-corp','시공사례 · 회사')]),
    body='''
<section class="section alt" id="program">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Rental Program</span>
      <h2>합리적인 가격, 기구렌탈 프로그램<br>4가지 체크리스트</h2>
      <p>기존의 노후된 기구로 인한 안전사고와 잦은 유상 A/S로 새로운 기구 구매를 고민하고 계시다면, 최소한의 비용으로 운동기구를 렌탈하여 이용할 수 있는 렌탈 프로그램을 추천합니다.<br>런닝머신 1대부터 피트니스센터의 인테리어까지 원하시는 공간에 전문인력을 파견하여 공간에 맞는 컨설팅과 견적을 상담해 드립니다.</p>
    </div>
    <div class="check4">
      <div class="chk rv d1"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div><h3>목돈 ZERO</h3><p>고가의 클럽용 제품을 초기비용 부담 없이 렌트로 이용 가능합니다.</p></div>
      <div class="chk rv d2"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div><h3>정기점검</h3><p>기구의 퀄리티 유지와 안전점검을 위해 정기적으로 기술자를 파견, 안전하게 관리합니다.</p></div>
      <div class="chk rv d3"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div><h3>A/S 무료</h3><p>구매 시 무상 A/S 기간이 지난 후에는 출장비와 부품비가 추가 발생하지만, 렌탈은 계약기간 내 A/S가 무료입니다.</p></div>
      <div class="chk rv d4"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16M12 4l8 8-8 8"/></svg></div><h3>소유권 이전</h3><p>렌탈 기간에 따라 소유권 이전이나 반납 중 택일. 재계약 시 할인 혜택을 드립니다.</p></div>
    </div>
  </div>
</section>

<section class="section" id="case-apt">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>CASE 01 · 아파트</small>세종 수루배 8단지</h3>
      <p>운동기구 렌탈 실제사례. 장기렌탈 시 바닥공사 및 기초 인테리어 공사를 무상으로 서비스해 드립니다. 체육관 바닥공사는 전용 고무바닥재 및 고무블럭으로 시공했습니다.</p>
    </div>
    <div class="gal rv">
      <figure class="wide"><img src="img/rental-apt-floor.jpg" alt="체육관 바닥공사" style="object-position:center 60%"><figcaption>체육관 바닥공사 (전용 고무바닥재 및 고무블럭 시공)</figcaption></figure>
      <figure><img src="img/rental-apt-1.jpg" alt="웨이트 머신 설치"><figcaption>웨이트 머신 설치</figcaption></figure>
      <figure><img src="img/rental-apt-2.jpg" alt="프리웨이트 존"><figcaption>프리웨이트 존</figcaption></figure>
      <figure><img src="img/rental-apt-3.jpg" alt="유산소 존"><figcaption>유산소 존</figcaption></figure>
      <figure><img src="img/rental-co-3.jpg" alt="렌탈 기구 설치"><figcaption>렌탈 기구 설치</figcaption></figure>
    </div>
  </div>
</section>

<section class="section alt" id="case-corp">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>CASE 02 · 회사</small>천안 풍세공단 자동차 연구원 체육관</h3>
      <p>기업체 사내 체육관 운동기구 렌탈 실제사례. 임직원 복지시설에 런닝머신 · 바이크 등 유산소 기구와 웨이트 머신을 렌탈로 구성하고 정기점검으로 관리합니다.</p>
    </div>
    <div class="gal rv">
      <figure><img src="img/rental-co-1.jpg" alt="유산소 존"><figcaption>유산소 존</figcaption></figure>
      <figure><img src="img/rental-co-2.jpg" alt="웨이트 머신"><figcaption>웨이트 머신</figcaption></figure>
      <figure><img src="img/rental-co-3.jpg" alt="프리웨이트 랙"><figcaption>프리웨이트 랙</figcaption></figure>
    </div>
  </div>
</section>
''')

# ---------------- PORTFOLIO ----------------
chips_fit = ['헬스보이 서울·경기·충청·경상 전지점','쌍용동 레시피','백석동 비타민사우나','두정동 골드스파','두정동 조이랜드','신방동 마르지아','배방 플렉스짐','아산 퍼스트짐','두정·신부 팀윤','백석파워짐 1·2호점','배방 팀H','두정동 탄이짐','성정동 곰짐','바디PT (두정·불당·신방·차암·오창·배방·장재·세종)','쌍용동 더머슬짐','안성 머슬K','수원·춘천 아리랑휘트니스','용인·수원 맥스짐','안성 JW요가']
chips_corp = ['삼성디스플레이 사내 · 기숙사','코닝정밀 사내 · 기숙사','해태음료','스테코','한국NSK','㈜TMC','㈜덕산네오룩스','동서산업','오산 램리서치','탕정 삼성트라팰리스','신방동 한성필하우스','신방동·용곡동 한라비발디','용곡동 동일하이빌','성성 푸르지오','불당 동일하이빌','불당 이안아파트','두정동 푸르지오','아산 푸르지오 · 포스코','아산 W호텔']
chips_pub = ['나사렛대학교','단국대학교','상명대학교','남서울대학교','호서대학교','경찰대학교','천안인애학교','천안중 · 고등학교','목천고등학교','두정중 · 고등학교','청수고등학교','충남예술고등학교','두정동 장애인복지관','아산건강문화센터','수신면사무소','배방 · 탕정 주민센터','예산 · 아산 소방서','한들문화센터','천안3산업단지 · 천안산업단지','민방위재난']
def chips(l): return ''.join(f'<span>{c}</span>' for c in l)+'<span class="etc">외 다수</span>'

PAGES['portfolio.html'] = dict(
    title='실적현황', desc='JS스포츠 천안·아산 및 전국 피트니스, 기업체·아파트, 학교·관공서 납품 및 A/S 관리 실적',
    on='portfolio', visual='img/install-2.jpg', crumb='실적현황', h1='실적현황',
    sub='개인 피트니스 센터부터 기업체, 아파트, 학교·관공서까지 토탈 스포츠 서비스를 제공해 온 신뢰할 수 있는 기업',
    subnav=nav([('fit','피트니스 · 개인PT'),('corp','기업체 · 아파트'),('pub','학교 · 관공서'),('photos','납품 사진')]),
    body=f'''
<section class="section" id="fit">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>01 · FITNESS</small>피트니스, 개인PT<br>납품 및 A/S 관리</h3>
      <p>JS스포츠는 개인 피트니스 센터부터 기업체, 아파트 단지 내 운동시설 운영, 학교 및 관공서까지 다양한 유형의 업체에 '토탈 스포츠 서비스'를 제공한 경험을 보유하고 있는 신뢰할 수 있는 기업입니다.</p>
    </div>
    <div class="chips rv" style="justify-content:flex-start">{chips(chips_fit)}</div>
  </div>
</section>
<section class="section alt" id="corp">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>02 · CORPORATE</small>기업체, 아파트<br>납품 및 A/S 관리</h3>
      <p>삼성디스플레이 · 코닝정밀 사내 피트니스와 기숙사, 탕정 삼성트라팰리스 · 푸르지오 · 한라비발디 등 아파트 단지 내 커뮤니티 운동시설의 납품과 관리대행을 진행하고 있습니다.</p>
    </div>
    <div class="chips rv" style="justify-content:flex-start">{chips(chips_corp)}</div>
  </div>
</section>
<section class="section" id="pub">
  <div class="wrap">
    <div class="casehead rv">
      <h3><small>03 · PUBLIC</small>학교, 관공서<br>납품 및 A/S 관리</h3>
      <p>조달청 · 나라장터 등록 업체로서 대학교, 중·고등학교, 주민센터, 소방서, 복지관 등 공공 체육시설에 조달 등록 기구를 납품하고 A/S를 관리합니다.</p>
    </div>
    <div class="chips rv" style="justify-content:flex-start">{chips(chips_pub)}</div>
  </div>
</section>
<section class="section dark" id="photos">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Photos</span>
      <h2>충청권 전역 피트니스 기구<br>실제 납품 사진</h2>
      <p>700평 창고에서 현장까지, 직접 운송 · 설치 · 시운전까지 책임집니다.</p>
    </div>
    <div class="gal rv">
      <figure class="wide"><img src="img/install-2.jpg" alt="덤벨 · 플레이트 납품"><figcaption>덤벨 · 원판 대량 납품</figcaption></figure>
      <figure><img src="img/install-1.jpg" alt="머신 설치"><figcaption>웨이트 머신 조립 · 설치</figcaption></figure>
      <figure><img src="img/install-3.jpg" alt="운송"><figcaption>자체 차량 운송</figcaption></figure>
      <figure><img src="img/rental-co-2.jpg" alt="웨이트 머신"><figcaption>웨이트 머신 납품</figcaption></figure>
      <figure><img src="img/rental-apt-2.jpg" alt="프리웨이트"><figcaption>프리웨이트 존 구성</figcaption></figure>
    </div>
  </div>
</section>
''')

# ---------------- CONTACT ----------------
PAGES['contact.html'] = dict(
    title='상담문의', desc='JS스포츠 컨설팅상담 1688-9634, 충남 아산시 배방읍 고불로 690-7',
    on='contact', visual='img/hero-3.jpg', crumb='상담문의', h1='상담문의',
    sub='운동시설에 관한 모든 고민, 전문인력이 직접 방문하여 공간에 맞는 컨설팅과 견적을 상담해 드립니다',
    subnav=nav([('info','연락처 · 오시는 길'),('form','온라인 상담')]),
    body='''
<section class="section" id="info">
  <div class="wrap contact">
    <div class="info rv">
      <span class="eyebrow">Contact</span>
      <h3>컨설팅상담</h3>
      <a href="tel:16889634" class="tel">1688-9634</a>
      <dl class="dl">
        <div><dt>본사</dt><dd>충남 아산시 배방읍 고불로 690-7</dd></div>
        <div><dt>FAX</dt><dd>041-534-0126</dd></div>
        <div><dt>H.P</dt><dd><a href="tel:01092298051">010-9229-8051</a></dd></div>
        <div><dt>홈페이지</dt><dd>www.js-sports.kr</dd></div>
        <div><dt>상담시간</dt><dd>평일 09:00 – 18:00 (A/S 긴급 출동 별도 문의)</dd></div>
      </dl>
    </div>
    <div class="map rv d1">
      <iframe src="https://maps.google.com/maps?q=%EC%B6%A9%EB%82%A8%20%EC%95%84%EC%82%B0%EC%8B%9C%20%EB%B0%B0%EB%B0%A9%EC%9D%8D%20%EA%B3%A0%EB%B6%88%EB%A1%9C%20690-7&t=&z=15&ie=UTF8&iwloc=&output=embed" loading="lazy" title="JS스포츠 위치"></iframe>
      <div class="maplinks"><a href="https://map.naver.com/p/search/%EC%B6%A9%EB%82%A8%20%EC%95%84%EC%82%B0%EC%8B%9C%20%EB%B0%B0%EB%B0%A9%EC%9D%8D%20%EA%B3%A0%EB%B6%88%EB%A1%9C%20690-7" target="_blank" rel="noopener">네이버 지도</a><a href="https://map.kakao.com/?q=%EC%B6%A9%EB%82%A8%20%EC%95%84%EC%82%B0%EC%8B%9C%20%EB%B0%B0%EB%B0%A9%EC%9D%8D%20%EA%B3%A0%EB%B6%88%EB%A1%9C%20690-7" target="_blank" rel="noopener">카카오맵</a><a href="https://www.google.com/maps/search/?api=1&query=%EC%B6%A9%EB%82%A8%20%EC%95%84%EC%82%B0%EC%8B%9C%20%EB%B0%B0%EB%B0%A9%EC%9D%8D%20%EA%B3%A0%EB%B6%88%EB%A1%9C%20690-7" target="_blank" rel="noopener">구글 지도</a></div>
    </div>
  </div>
</section>
<section class="section alt" id="form">
  <div class="wrap" style="max-width:860px">
    <div class="sec-head rv">
      <span class="eyebrow">Online</span>
      <h2>온라인 상담 신청</h2>
      <p>내용을 남겨주시면 담당자가 확인 후 빠르게 연락드립니다.</p>
    </div>
    <form class="form rv">
      <div class="r2"><input name="name" placeholder="이름 / 업체명" required><input name="tel" placeholder="연락처" required></div>
      <select name="type"><option>시설 유형 선택</option><option>피트니스 센터 · PT샵</option><option>기업체 사내 체육시설</option><option>아파트 커뮤니티</option><option>학교 · 관공서</option><option>기타</option></select>
      <textarea name="msg" placeholder="문의내용 (기구 납품 / 정기점검 / 렌탈 / 위탁운영 / 인테리어 등)"></textarea>
      <label class="agree"><input type="checkbox" required> 개인정보 수집 및 이용에 동의합니다.</label>
      <button class="btn btn-red" type="submit" style="justify-content:center">상담 신청하기</button>
    </form>
  </div>
</section>
''')

for fn, p in PAGES.items():
    ons = {k: (' class="on"' if p['on'] == k else '') for k in ['about','service','rental','portfolio','contact']}
    html = HEAD.format(title=p['title'], desc=p['desc'], visual=p['visual'], crumb=p['crumb'], h1=p['h1'], sub=p['sub'], subnav=p['subnav'],
                       on_about=ons['about'], on_service=ons['service'], on_rental=ons['rental'], on_portfolio=ons['portfolio'], on_contact=ons['contact'])
    html += p['body'] + FOOT
    with io.open(os.path.join(ROOT, fn), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', fn, len(html))
