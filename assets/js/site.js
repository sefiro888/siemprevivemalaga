/* Siempre Vive · interacción del sitio */
(()=>{
const d=document,root=d.documentElement;
const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer=window.matchMedia('(hover: hover) and (pointer: fine)').matches;
root.classList.add('js');

/* ---------- WhatsApp personalizado por colección ---------- */
const PHONE='34622749770';
const pageTopics={
  'ramos.html':'Ramos','orquideas.html':'Orquídeas','macetas.html':'Macetas','cactus-y-plantas.html':'Cactus y plantas',
  'variedad-de-flores.html':'Variedad de flores','fechas-especiales.html':'Fechas especiales','rosas.html':'Rosas',
  'rosas-eternas.html':'Rosas eternas','packs-de-regalo.html':'Packs de regalo','bodas.html':'Ramos de novia y bodas',
  'eventos.html':'Eventos corporativos y sociales','galeria.html':'Galería'
};
const page=location.pathname.split('/').pop()||'index.html';
const pageTopic=pageTopics[page]||'';
const waMessage=topic=>topic
  ?`¡Hola, Siempre Vive! 🌷 Me interesa la colección «${topic}». ¿Me contáis qué opciones tenéis disponibles? Muchas gracias.`
  :'¡Hola, Siempre Vive! 🌷 He visto vuestra web y me gustaría consultar una idea floral. ¿Podemos hablar? Muchas gracias.';
const waUrl=topic=>`https://wa.me/${PHONE}?text=${encodeURIComponent(waMessage(topic))}`;
const waIcon='<svg class="wa-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a9.9 9.9 0 0 0-8.53 15L2 22l5.15-1.4A10 10 0 1 0 12 2Zm0 18a8 8 0 0 1-4.1-1.12l-.3-.18-3 .82.82-2.9-.2-.31A8 8 0 1 1 12 20Zm4.5-5.8c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.25-.75-.67-1.25-1.5-1.4-1.75-.15-.25-.02-.39.11-.52.11-.11.25-.3.37-.44.12-.14.17-.25.25-.42.08-.17.04-.32-.02-.45-.06-.12-.57-1.37-.78-1.87-.21-.49-.42-.42-.57-.43h-.49c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1s.9 2.44 1.03 2.6c.12.17 1.77 2.7 4.28 3.78.6.26 1.07.42 1.44.53.61.19 1.16.16 1.6.1.49-.07 1.48-.61 1.69-1.2.21-.59.21-1.09.15-1.2-.07-.1-.23-.16-.48-.29Z"/></svg>';
d.querySelectorAll(`a[href^="https://wa.me/${PHONE}"]`).forEach(link=>{
  // data-wa="" explícito = mensaje general; sin atributo = tema de la página
  const topic=link.hasAttribute('data-wa')?link.dataset.wa:pageTopic;
  link.href=waUrl(topic);
  if(link.classList.contains('button')&&!link.querySelector('.wa-ico')){link.classList.add('btn-wa');link.insertAdjacentHTML('afterbegin',waIcon);}
});

/* ---------- Cabecera: estado al hacer scroll y barra de progreso ---------- */
const header=d.querySelector('.site-header');
const progress=d.createElement('div');progress.className='scroll-progress';progress.setAttribute('aria-hidden','true');d.body.append(progress);
const toTop=d.createElement('button');toTop.className='to-top';toTop.type='button';toTop.setAttribute('aria-label','Volver arriba');toTop.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';d.body.append(toTop);
toTop.addEventListener('click',()=>window.scrollTo({top:0,behavior:reduceMotion?'auto':'smooth'}));
let ticking=false;
const onScroll=()=>{
  const y=window.scrollY,max=d.documentElement.scrollHeight-window.innerHeight;
  header&&header.classList.toggle('is-scrolled',y>40);
  progress.style.transform=`scaleX(${max>0?Math.min(y/max,1):0})`;
  toTop.classList.toggle('show',y>900);
  if(!reduceMotion)parallaxEls.forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom<-200||r.top>window.innerHeight+200)return;const c=r.top+r.height/2-window.innerHeight/2;el.style.setProperty('--py',`${(c*-(parseFloat(el.dataset.parallax)||.08)).toFixed(1)}px`);});
  ticking=false;
};
const parallaxEls=[...d.querySelectorAll('[data-parallax]')];
window.addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(onScroll);ticking=true;}},{passive:true});
window.addEventListener('resize',onScroll,{passive:true});
onScroll();

/* ---------- Menús desplegables de escritorio ---------- */
d.querySelectorAll('.nav-dropdown').forEach(dd=>{
  const trigger=dd.querySelector('.nav-trigger');let closeTimer,openedAt=0;
  const set=open=>{if(open&&!dd.classList.contains('open'))openedAt=Date.now();dd.classList.toggle('open',open);trigger.setAttribute('aria-expanded',String(open));};
  const closeOthers=()=>d.querySelectorAll('.nav-dropdown.open').forEach(o=>{if(o!==dd){o.classList.remove('open');o.querySelector('.nav-trigger').setAttribute('aria-expanded','false');}});
  trigger.addEventListener('click',()=>{closeOthers();const isOpen=dd.classList.contains('open');set(!(isOpen&&Date.now()-openedAt>450));});
  if(finePointer){
    dd.addEventListener('mouseenter',()=>{clearTimeout(closeTimer);closeOthers();set(true);});
    dd.addEventListener('mouseleave',()=>{closeTimer=setTimeout(()=>set(false),180);});
  }
  dd.addEventListener('focusout',e=>{if(!dd.contains(e.relatedTarget))set(false);});
  d.addEventListener('keydown',e=>{if(e.key==='Escape'&&dd.classList.contains('open')){set(false);trigger.focus();}});
  d.addEventListener('click',e=>{if(!dd.contains(e.target))set(false);});
});

/* ---------- Menú móvil a pantalla completa ---------- */
const toggle=d.querySelector('.menu-toggle'),mnav=d.querySelector('.mobile-nav');
if(toggle&&mnav){
  const closeBtn=mnav.querySelector('.mnav-close');
  const focusables=()=>[...mnav.querySelectorAll('a,button')].filter(el=>el.offsetParent!==null);
  const open=()=>{
    const r=toggle.getBoundingClientRect();
    mnav.style.setProperty('--ox',`${r.left+r.width/2}px`);mnav.style.setProperty('--oy',`${r.top+r.height/2}px`);
    mnav.removeAttribute('inert');mnav.classList.add('open');root.classList.add('menu-open');
    toggle.setAttribute('aria-expanded','true');toggle.setAttribute('aria-label','Cerrar menú');
    setTimeout(()=>(closeBtn||focusables()[0])?.focus(),60);
  };
  const close=()=>{
    mnav.classList.remove('open');root.classList.remove('menu-open');mnav.setAttribute('inert','');
    toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Abrir menú');
  };
  toggle.addEventListener('click',()=>mnav.classList.contains('open')?close():open());
  closeBtn&&closeBtn.addEventListener('click',()=>{close();toggle.focus();});
  mnav.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
  d.addEventListener('keydown',e=>{
    if(!mnav.classList.contains('open'))return;
    if(e.key==='Escape'){close();toggle.focus();}
    if(e.key==='Tab'){const f=focusables();if(!f.length)return;const first=f[0],last=f[f.length-1];
      if(e.shiftKey&&d.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&d.activeElement===last){e.preventDefault();first.focus();}}
  });
  window.addEventListener('resize',()=>{if(window.innerWidth>1100&&mnav.classList.contains('open'))close();});
}

/* ---------- Titulares que aparecen palabra a palabra ---------- */
d.querySelectorAll('[data-split]').forEach(el=>{
  if(reduceMotion)return;
  let i=0;
  const walk=node=>{
    [...node.childNodes].forEach(n=>{
      if(n.nodeType===3){
        const frag=d.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part=>{
          if(!part)return;
          if(/^\s+$/.test(part)){frag.append(part);return;}
          const w=d.createElement('span');w.className='w';const inner=d.createElement('span');inner.textContent=part;inner.style.setProperty('--i',i++);w.append(inner);frag.append(w);
        });
        n.replaceWith(frag);
      }else if(n.nodeType===1&&!n.classList.contains('w'))walk(n);
    });
  };
  walk(el);el.classList.add('is-split');
  requestAnimationFrame(()=>requestAnimationFrame(()=>el.classList.add('split-in')));
});

/* ---------- Apariciones al hacer scroll ---------- */
d.querySelectorAll('[data-stagger]').forEach(p=>[...p.children].forEach((c,i)=>{c.setAttribute('data-reveal',c.getAttribute('data-reveal')||'');c.style.setProperty('--d',`${Math.min(i,8)*90}ms`);}));
const reveals=d.querySelectorAll('[data-reveal],.orn,.orn-divider,.reveal-img');
if('IntersectionObserver'in window&&!reduceMotion){
  const io=new IntersectionObserver(entries=>entries.forEach(en=>{if(en.isIntersecting){en.target.classList.add('visible');io.unobserve(en.target);}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  reveals.forEach(el=>io.observe(el));
}else reveals.forEach(el=>el.classList.add('visible'));

/* ---------- Pétalos flotantes ---------- */
if(!reduceMotion)d.querySelectorAll('[data-petals]').forEach(box=>{
  const n=window.innerWidth<700?7:14;
  for(let i=0;i<n;i++){const p=d.createElement('span');p.className='petal';
    p.style.cssText=`--x:${Math.random()*100}%;--s:${.55+Math.random()*.8};--t:${11+Math.random()*10}s;--dl:${-Math.random()*20}s;--dx:${(Math.random()*160-80).toFixed(0)}px;--h:${Math.random()>.5?'#f2c9cf':'#ead7ee'}`;
    box.append(p);}
});

/* ---------- Pestañas «Ideas para elegir» ---------- */
d.querySelectorAll('[data-tabs]').forEach(tabs=>{
  const btns=[...tabs.querySelectorAll('[role="tab"]')];
  const select=(btn,focus)=>{
    btns.forEach(b=>{const on=b===btn;b.setAttribute('aria-selected',String(on));b.tabIndex=on?0:-1;
      const panel=d.getElementById(b.getAttribute('aria-controls'));if(panel){panel.hidden=!on;if(on){panel.classList.remove('panel-in');void panel.offsetWidth;panel.classList.add('panel-in');}}});
    if(focus)btn.focus();
    btn.scrollIntoView({block:'nearest',inline:'center',behavior:reduceMotion?'auto':'smooth'});
  };
  btns.forEach((b,i)=>{
    b.addEventListener('click',()=>select(b));
    b.addEventListener('keydown',e=>{
      let j=null;if(e.key==='ArrowRight')j=(i+1)%btns.length;if(e.key==='ArrowLeft')j=(i-1+btns.length)%btns.length;if(e.key==='Home')j=0;if(e.key==='End')j=btns.length-1;
      if(j!==null){e.preventDefault();select(btns[j],true);}
    });
  });
});

/* ---------- Filtros de galería ---------- */
d.querySelectorAll('[data-filter-group]').forEach(group=>{
  const grid=d.getElementById(group.dataset.filterGroup);if(!grid)return;
  group.querySelectorAll('button').forEach(btn=>btn.addEventListener('click',()=>{
    group.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));
    const f=btn.dataset.filter;
    grid.querySelectorAll('[data-cat]').forEach(it=>{const show=f==='todo'||it.dataset.cat.split(' ').includes(f);it.hidden=!show;if(show){it.classList.remove('pop');void it.offsetWidth;it.classList.add('pop');}});
  }));
});

/* ---------- Visor de imágenes (lightbox) ---------- */
const lbItems=()=>[...d.querySelectorAll('[data-lightbox]')].filter(el=>!el.closest('[hidden]'));
if(d.querySelector('[data-lightbox]')){
  const lb=d.createElement('div');lb.className='lightbox';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Imagen ampliada');lb.hidden=true;
  lb.innerHTML=`<button class="lb-close" type="button" aria-label="Cerrar">×</button><button class="lb-prev" type="button" aria-label="Imagen anterior">‹</button><figure class="lb-figure"><img alt=""><figcaption><span class="lb-caption"></span><span class="lb-count"></span></figcaption></figure><button class="lb-next" type="button" aria-label="Imagen siguiente">›</button>`;
  d.body.append(lb);
  const img=lb.querySelector('img'),cap=lb.querySelector('.lb-caption'),count=lb.querySelector('.lb-count');
  let list=[],idx=0,lastFocus=null;
  const srcOf=el=>el.dataset.full||el.querySelector('img')?.currentSrc||el.querySelector('img')?.src||el.getAttribute('href');
  const show=i=>{
    idx=(i+list.length)%list.length;const el=list[idx],im=el.querySelector('img');
    lb.classList.remove('lb-ready');
    img.onload=()=>lb.classList.add('lb-ready');
    img.src=srcOf(el);img.alt=im?.alt||'';
    cap.textContent=el.dataset.caption||el.querySelector('figcaption')?.textContent||im?.alt||'';
    count.textContent=`${idx+1} / ${list.length}`;
    [list[(idx+1)%list.length],list[(idx-1+list.length)%list.length]].forEach(n=>{const p=new Image();p.src=srcOf(n);});
  };
  const open=el=>{list=lbItems();lastFocus=d.activeElement;lb.hidden=false;root.classList.add('lb-open');requestAnimationFrame(()=>lb.classList.add('open'));show(list.indexOf(el));lb.querySelector('.lb-close').focus();};
  const close=()=>{lb.classList.remove('open');root.classList.remove('lb-open');setTimeout(()=>{lb.hidden=true;img.src='';},250);lastFocus&&lastFocus.focus();};
  d.addEventListener('click',e=>{const t=e.target.closest('[data-lightbox]');if(t){e.preventDefault();open(t);}});
  d.querySelectorAll('[data-lightbox]').forEach(el=>{if(el.tagName!=='A'&&el.tagName!=='BUTTON'){el.tabIndex=0;el.setAttribute('role','button');el.setAttribute('aria-label',`Ampliar imagen: ${el.querySelector('img')?.alt||''}`);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(el);}});}});
  lb.querySelector('.lb-close').addEventListener('click',close);
  lb.querySelector('.lb-prev').addEventListener('click',()=>show(idx-1));
  lb.querySelector('.lb-next').addEventListener('click',()=>show(idx+1));
  lb.addEventListener('click',e=>{if(e.target===lb)close();});
  d.addEventListener('keydown',e=>{if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(idx+1);if(e.key==='ArrowLeft')show(idx-1);
    if(e.key==='Tab'){const f=[...lb.querySelectorAll('button')];const i=f.indexOf(d.activeElement);e.preventDefault();f[(i+(e.shiftKey?-1:1)+f.length)%f.length].focus();}});
  let sx=0,sy=0;
  lb.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;sy=e.touches[0].clientY;},{passive:true});
  lb.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))show(idx+(dx<0?1:-1));else if(dy>90)close();},{passive:true});
}

/* ---------- Botón flotante de contacto ---------- */
const dock=d.createElement('aside');
dock.className='contact-dock';dock.setAttribute('aria-label','Contacto directo con Siempre Vive');
const shortTopics={'bodas.html':'Bodas','eventos.html':'Eventos','variedad-de-flores.html':'Variedad de flores'};
const dockLabel=pageTopic&&page!=='galeria.html'?`Pedir ${shortTopics[page]||pageTopic}`:'Escríbenos';
dock.innerHTML=`<a class="dock-whatsapp" href="${waUrl(page==='galeria.html'?'':pageTopic)}" target="_blank" rel="noopener noreferrer" aria-label="${dockLabel} por WhatsApp">${waIcon}<span class="dock-text"><small>WhatsApp</small>${dockLabel}</span></a>`;
d.body.append(dock);
setTimeout(()=>dock.classList.add('show'),reduceMotion?0:1400);
})();
