document.addEventListener('DOMContentLoaded',()=>{
  const menu=document.querySelector('[data-menu]');
  const mobile=document.querySelector('[data-mobile-nav]');
  if(menu&&mobile){
    const close=(restoreFocus=true)=>{
      mobile.classList.remove('open');
      document.body.classList.remove('menu-open');
      menu.setAttribute('aria-expanded','false');
      menu.setAttribute('aria-label','Open navigation');
      if(restoreFocus) menu.focus();
    };
    const open=()=>{
      mobile.classList.add('open');
      document.body.classList.add('menu-open');
      menu.setAttribute('aria-expanded','true');
      menu.setAttribute('aria-label','Close navigation');
      mobile.querySelector('a')?.focus();
    };
    menu.addEventListener('click',()=>mobile.classList.contains('open')?close(false):open());
    mobile.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>close(false)));
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'&&mobile.classList.contains('open')) close();
      if(e.key==='Tab'&&mobile.classList.contains('open')){
        const focusable=[menu,...mobile.querySelectorAll('a[href]')];
        const first=focusable[0],last=focusable[focusable.length-1];
        if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
        else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
      }
    });
  }
  document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
  const path=window.location.pathname.replace(/\/+$/,'')||'/';
  document.querySelectorAll('[data-nav]').forEach(a=>{const href=a.getAttribute('href')||'';const normalized=href.replace(/\/+$/,'')||'/';if(normalized===path){a.classList.add('current');a.setAttribute('aria-current','page');}});
  const copyButtons=document.querySelectorAll('[data-copy-discord]');
  copyButtons.forEach(button=>button.addEventListener('click',async()=>{
    const value=button.getAttribute('data-copy-value')||'xlamus_op';
    const label=button.querySelector('[data-copy-label]');
    let copied=false;
    try{
      if(navigator.clipboard&&window.isSecureContext){
        await navigator.clipboard.writeText(value); copied=true;
      }else{
        const helper=document.createElement('textarea');
        helper.value=value; helper.setAttribute('readonly',''); helper.style.position='fixed'; helper.style.opacity='0';
        document.body.appendChild(helper); helper.select(); copied=document.execCommand('copy'); helper.remove();
      }
    }catch(_){copied=false;}
    if(label) label.textContent=copied?'COPIED':'COPY FAILED';
    button.classList.toggle('copied',copied);
    window.setTimeout(()=>{if(label) label.textContent='COPY';button.classList.remove('copied');},1700);
  }));
  document.querySelectorAll('.game-img').forEach(img=>img.addEventListener('error',()=>{
    img.style.display='none';
    const fallback=img.parentElement?.querySelector('.game-fallback');
    if(fallback) fallback.style.display='grid';
  }));
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!reduce){document.querySelectorAll('.reveal').forEach((el,i)=>{el.style.animationDelay=Math.min(i*40,200)+'ms';});}
});
