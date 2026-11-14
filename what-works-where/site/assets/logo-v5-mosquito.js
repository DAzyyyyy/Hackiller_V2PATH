const root=document.getElementById('logo-preview');
const pause=document.getElementById('pause');
const theme=document.getElementById('theme');
const mark=document.getElementById('interactive-logo');
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
pause.addEventListener('click',()=>{
 const paused=root.dataset.logoPaused!=='true';
 root.dataset.logoPaused=String(paused);
 pause.setAttribute('aria-pressed',String(paused));
 pause.textContent=paused?'播放动效':'暂停动效';
});
theme.addEventListener('click',()=>{
 const light=document.body.classList.toggle('light');
 theme.setAttribute('aria-pressed',String(light));
 theme.textContent=light?'深色背景':'浅色背景';
});
mark.addEventListener('pointermove',e=>{
 if(reduced.matches||root.dataset.logoPaused==='true')return;
 const r=mark.getBoundingClientRect();
 mark.style.setProperty('--rx',`${-(e.clientY-r.top-r.height/2)/r.height*17}deg`);
 mark.style.setProperty('--ry',`${(e.clientX-r.left-r.width/2)/r.width*22}deg`);
});
mark.addEventListener('pointerleave',()=>{
 mark.style.setProperty('--rx','0deg');mark.style.setProperty('--ry','0deg');
});
