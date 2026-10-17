document.querySelectorAll('[data-position]').forEach(button=>button.addEventListener('click',()=>{
 const position=button.dataset.position,script=document.body.dataset.script;
 document.querySelectorAll('[data-position]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
 const label=button.dataset.label;
 const preview=document.getElementById('script-logo');preview.src=`assets/${script}-${position}.png`;preview.alt=label+' mixed-script logo';
 document.getElementById('script-reading').textContent=label;
 const download=document.getElementById('script-download');download.href=preview.src;download.download=`dum-e-odisha-${script}-${position}.png`;
 document.getElementById('editable-link').href=`${script}-${position}-artwork.html`;
}));
