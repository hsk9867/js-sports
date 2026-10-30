/* JS스포츠 main.js */
(function(){
  const $=(s,c=document)=>c.querySelector(s);
  const $$=(s,c=document)=>[...c.querySelectorAll(s)];

  /* header + progress + totop */
  const header=$('.header'), prog=$('#progress'), totop=$('.totop');
  const isSub=header&&header.classList.contains('sub');
  function onScroll(){
    const y=window.scrollY||document.documentElement.scrollTop;
    const h=document.documentElement.scrollHeight-window.innerHeight;
    if(prog) prog.style.width=(h>0?(y/h*100):0)+'%';
    if(header&&!isSub) header.classList.toggle('solid',y>60);
    if(totop) totop.classList.toggle('show',y>500);
    const side=$('.hero .side i');
    if(side){const hero=$('.hero');side.style.height=Math.min(100,y/(hero.offsetHeight||1)*100)+'%';}
  }
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(totop) totop.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));

  /* full menu */
  const ham=$('.ham');
  if(ham){
    ham.addEventListener('click',()=>document.body.classList.toggle('menu-open'));
    $$('.fullmenu a').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('menu-open')));
    document.addEventListener('keydown',e=>{if(e.key==='Escape')document.body.classList.remove('menu-open');});
  }

  /* reveal */
  const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  $$('.rv').forEach(el=>io.observe(el));

  /* hero slider */
  const slides=$$('.hero .slide'), lines=$$('.hero .cap .line'), dots=$$('.hero .dots button'), num=$('.hero .num b');
  if(slides.length){
    let i=0,t;
    function go(n){
      i=(n+slides.length)%slides.length;
      slides.forEach((s,k)=>s.classList.toggle('on',k===i));
      lines.forEach((s,k)=>s.classList.toggle('on',k===i));
      dots.forEach((s,k)=>s.classList.toggle('on',k===i));
      if(num) num.textContent=String(i+1).padStart(2,'0');
      clearTimeout(t);t=setTimeout(()=>go(i+1),6000);
    }
    dots.forEach((d,k)=>d.addEventListener('click',()=>go(k)));
    go(0);
  }

  /* client tabs */
  $$('.ctabs button').forEach(b=>b.addEventListener('click',()=>{
    $$('.ctabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
    $$('.cpanel').forEach(p=>p.classList.toggle('on',p.dataset.tab===b.dataset.tab));
  }));

  /* subnav active */
  const subLinks=$$('.subnav a[href^="#"]');
  if(subLinks.length){
    const secs=subLinks.map(a=>$(a.getAttribute('href'))).filter(Boolean);
    const io2=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){subLinks.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id));}});},{rootMargin:'-40% 0px -55% 0px'});
    secs.forEach(s=>io2.observe(s));
  }

  /* contact form (mailto fallback) */
  const form=$('.form');
  if(form){
    form.addEventListener('submit',e=>{
      e.preventDefault();
      const d=new FormData(form);
      const body=['이름: '+d.get('name'),'연락처: '+d.get('tel'),'시설유형: '+d.get('type'),'문의내용:',d.get('msg')].join('\n');
      location.href='mailto:jssports@js-sports.kr?subject='+encodeURIComponent('[홈페이지 상담문의] '+d.get('name'))+'&body='+encodeURIComponent(body);
    });
  }
})();
