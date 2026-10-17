'use strict';
const descriptions={faithful:'Faithful refinement / retains the original positive grain detail with clearer spacing.','negative-space':'Negative space / the rice kernel is the counter, not an extra floating shape.'};
document.querySelectorAll('[data-variant]').forEach(button=>button.addEventListener('click',()=>{
 const variant=button.dataset.variant;
 document.querySelectorAll('[data-variant]').forEach(x=>x.setAttribute('aria-pressed',String(x===button)));
 const img=document.getElementById('active-logo');img.src=`assets/${variant}-primary.png`;img.alt=variant==='faithful'?'Faithful refinement of the owner-supplied Dum E Odisha logo':'Refined negative-space Dum E Odisha logo';
 document.getElementById('active-download').href=img.getAttribute('src');document.getElementById('variant-description').textContent=descriptions[variant];
}));
