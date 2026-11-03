# -*- coding: utf-8 -*-
"""아파트 위탁운영 · 전문인력 배치 페이지 정의 — build_sub.py 가 import 해서 PAGES 에 추가 (2026-11-03 최종 PPT 15~22p 반영)"""

def nav(items):
    return ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)

BODY = '''
<section class="section" id="intro">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Operation</span>
      <h2 class="split">아파트 커뮤니티 체육시설 <b class="hl">위탁운영</b></h2>
      <p>관리사무소의 운영 부담은 줄이고, 입주민의 이용 편의와 시설관리의 일관성을 높이는 운영 모델입니다.<br>JS스포츠가 시설 운영관리부터 회원·프로그램 관리까지 맡습니다.</p>
    </div>
    <div class="ov">
      <div class="pic rv"><img src="img/op-ian-1.jpg" alt="신불당 이안 아파트 커뮤니티 헬스장"></div>
      <div class="rv d1" style="display:grid;gap:20px">
        <div class="point"><b>01 · FACILITY</b><h3>시설 운영관리</h3><ul class="plist"><li>운영시간 · 이용수칙 관리</li><li>입 · 퇴장 및 이용현황 관리</li><li>기구 상태 점검 및 유지관리 연계</li><li>현장 민원 접수 · 처리 지원</li></ul></div>
        <div class="point"><b>02 · MEMBER</b><h3>회원 · 프로그램 관리</h3><ul class="plist"><li>입주민 이용 안내 및 회원관리</li><li>필요 시 트레이너 · 안내 인력 배치</li><li>OT 및 운동지도 프로그램 운영</li><li>월간 운영보고와 개선사항 제안</li></ul></div>
      </div>
    </div>
    <p class="note rv">※ 인력 규모 · 운영시간 · 프로그램 · 수익 귀속 구조는 단지 여건에 맞춰 협의합니다.</p>
  </div>
</section>

<section class="section alt" id="plans">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Plan</span>
      <h2 class="split">위탁운영 방식은 <b class="hl">단지별로 맞춤 설계</b></h2>
      <p>기구 교체가 반드시 필요한 것은 아닙니다. 기존 자산을 활용하면서 필요한 운영 기능을 보완합니다.</p>
    </div>
    <div class="types plans">
      <div class="type rv d1">
        <span class="lab">PLAN A</span>
        <h3>전면 위탁운영</h3>
        <p>운영인력과 회원관리, 시설 유지관리까지 커뮤니티 체육시설 전체를 JS스포츠가 책임지는 방식입니다.</p>
        <ul><li>운영인력 + 회원관리</li><li>시설 · 기구 유지관리 연계</li><li>프로그램 기획 · 운영</li><li>실적 및 정산 보고</li></ul>
        <span class="big">A</span>
      </div>
      <div class="type b rv d2">
        <span class="lab">PLAN B</span>
        <h3>부분 위탁운영</h3>
        <p>기존 관리체계는 유지하면서 안내데스크나 트레이너 등 필요한 업무만 분리해 위탁하는 방식입니다.</p>
        <ul><li>안내데스크 또는 트레이너</li><li>일부 시간대 선택 운영</li><li>기존 관리체계와 병행</li><li>필수 업무만 분리 위탁</li></ul>
        <span class="big">B</span>
      </div>
      <div class="type rv d3">
        <span class="lab">PLAN C</span>
        <h3>통합 패키지</h3>
        <p>위탁운영에 정기점검과 기구 렌탈·교체, A/S 대응체계까지 단지 예산에 맞춰 조합하는 방식입니다.</p>
        <ul><li>위탁운영 + 정기점검</li><li>필요한 기구만 렌탈 · 교체</li><li>A/S 대응체계 연계</li><li>단지 예산에 맞춘 조합</li></ul>
        <span class="big">C</span>
      </div>
    </div>
    <p class="note rv">※ 운영조건 예시이며 실제 계약 범위 · 비용 · 책임구분은 현장 실사 후 제안합니다.</p>
  </div>
</section>

<section class="section dark" id="staff">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Staffing</span>
      <h2 class="split">기존 시설 <b class="hl">전문인력 배치 · 파견</b> 서비스</h2>
      <p>운동기구와 시설은 이미 갖췄지만, 상주 관리인력이 없어 운영이 어려운 아파트에 적합합니다.</p>
    </div>
    <div class="ov">
      <div class="rv" style="display:grid;gap:20px">
        <div class="point dk"><b>01</b><h3>필요한 인력만 배치</h3><ul class="plist"><li>헬스장 트레이너 / 운동지도 인력</li><li>인포데스크 / 회원관리 인력</li><li>시설 순회 · 관리 지원 인력</li><li>요일별 · 시간대별 탄력 배치</li></ul></div>
        <div class="point dk"><b>02</b><h3>기존 시설 그대로 활용</h3><ul class="plist"><li>기구 신규 구매 · 렌탈 없이 시작 가능</li><li>입주민 응대 및 이용질서 관리</li><li>기구 이상 발견 시 점검 · A/S 연계</li><li>인력 관리 및 운영현황 보고 지원</li></ul></div>
      </div>
      <div class="pic rv d1"><img src="img/op-dongil-2.jpg" alt="불당 동일하이빌 커뮤니티 헬스장"></div>
    </div>
    <div class="quote rv"><span>핵심 제안</span>“기구는 그대로, 필요한 사람만 배치합니다.”</div>
  </div>
</section>

<section class="section" id="pick">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Service</span>
      <h2 class="split">단지 상황에 따라 선택하는 <b class="hl">4가지 서비스</b></h2>
      <p>시설 상태 · 운영 인력 · 관리예산에 맞춰 단독 서비스 또는 결합형 운영이 가능합니다.</p>
    </div>
    <div class="check4 pick4">
      <a class="chk rv d1" href="service.html"><span class="no">01</span><h3>정기점검 · A/S</h3><p>기구는 있고 전문 점검이 필요한 단지</p><span class="go">자세히 보기</span></a>
      <a class="chk rv d2" href="rental.html"><span class="no">02</span><h3>기구 렌탈 · 납품</h3><p>노후 기구 교체 · 보강이 필요한 단지</p><span class="go">자세히 보기</span></a>
      <a class="chk rv d3" href="#staff"><span class="no">03</span><h3>전문인력 배치</h3><p>시설은 있지만 상주 관리인력이 없는 단지</p><span class="go">자세히 보기</span></a>
      <a class="chk rv d4" href="#intro"><span class="no">04</span><h3>아파트 위탁운영</h3><p>회원 · 시설 · 인력 운영을 통합 맡기려는 단지</p><span class="go">자세히 보기</span></a>
    </div>
    <p class="pick-tag rv">선택형 서비스 · 필요 항목만 결합 · 현장 진단을 통한 맞춤 운영 제안</p>
  </div>
</section>

<section class="section alt" id="cases">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Cases</span>
      <h2 class="split">아파트 커뮤니티 체육시설 <b class="hl">위탁운영 사례</b></h2>
      <p>JS스포츠가 위탁운영하는 아파트 커뮤니티 체육시설을 실제 현장 사진으로 소개합니다.</p>
    </div>
    <div class="opcase rv">
      <div class="casehead"><h3><small>CASE 01 · 천안</small>신불당 이안 아파트</h3><p>아파트 커뮤니티 체육시설 위탁운영. 웨이트 머신 · 프리웨이트 존과 유산소 존을 갖춘 단지 내 헬스장을 운영 · 관리합니다.</p></div>
      <div class="gal g2">
        <figure><img src="img/op-ian-1.jpg" alt="신불당 이안 아파트 헬스장 1"><figcaption>위탁운영 현장 · 웨이트 존</figcaption></figure>
        <figure><img src="img/op-ian-2.jpg" alt="신불당 이안 아파트 헬스장 2"><figcaption>위탁운영 현장 · 유산소 존</figcaption></figure>
      </div>
    </div>
    <div class="opcase rv">
      <div class="casehead"><h3><small>CASE 02 · 천안</small>불당 동일하이빌</h3><p>아파트 커뮤니티 체육시설 위탁운영. 유산소 기구와 웨이트 머신, 프리웨이트 랙까지 입주민이 안전하게 이용하도록 상주 관리합니다.</p></div>
      <div class="gal">
        <figure><img src="img/op-dongil-1.jpg" alt="불당 동일하이빌 헬스장 1"><figcaption>위탁운영 현장 · 유산소 존</figcaption></figure>
        <figure><img src="img/op-dongil-2.jpg" alt="불당 동일하이빌 헬스장 2"><figcaption>위탁운영 현장 · 웨이트 존</figcaption></figure>
        <figure><img src="img/op-dongil-3.jpg" alt="불당 동일하이빌 헬스장 3"><figcaption>위탁운영 현장 · 머신 존</figcaption></figure>
      </div>
    </div>
    <div class="opcase rv">
      <div class="casehead"><h3><small>CASE 03 · 천안</small>용곡 두산위브</h3><p>아파트 커뮤니티 체육시설 위탁운영. 스쿼트 랙 · 벤치 등 프리웨이트 구역과 머신 구역을 함께 운영합니다.</p></div>
      <div class="gal g2">
        <figure><img src="img/op-doosan-1.jpg" alt="용곡 두산위브 헬스장 1"><figcaption>위탁운영 현장 · 프리웨이트 존</figcaption></figure>
        <figure><img src="img/op-doosan-2.jpg" alt="용곡 두산위브 헬스장 2"><figcaption>위탁운영 현장 · 머신 존</figcaption></figure>
      </div>
    </div>
    <div class="oplist rv">
      <span class="lab">JS SPORTS · 아파트 커뮤니티시설 운영관리 실적</span>
      <div class="chips" style="justify-content:flex-start"><span>신불당 이안 아파트</span><span>불당 동일하이빌</span><span>용곡 두산위브</span><span>용곡 세광 2차</span><span class="etc">외 다수</span></div>
    </div>
  </div>
</section>
'''

PAGE = dict(
    title='아파트 위탁운영 · 인력파견',
    desc='JS스포츠 아파트 커뮤니티 체육시설 위탁운영 - 전면·부분·통합 패키지 위탁운영, 기존 시설 전문인력 배치·파견, 신불당 이안·불당 동일하이빌·용곡 두산위브 위탁운영 사례',
    on='operation', visual='img/op-doosan-1.jpg', crumb='위탁운영 · 인력파견', h1='아파트 위탁운영 · 인력파견',
    sub='관리사무소의 운영 부담은 줄이고, 입주민의 이용 편의와 시설관리의 일관성을 높이는 운영 모델',
    subnav=nav([('intro','위탁운영'),('plans','운영 방식'),('staff','전문인력 배치'),('pick','서비스 선택'),('cases','위탁운영 사례')]),
    body=BODY,
)
