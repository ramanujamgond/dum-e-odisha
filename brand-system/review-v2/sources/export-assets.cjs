/* Export-only color separations of the generated raster master. No geometry is redrawn. */
const fs = require('node:fs');
const path = require('node:path');
const runtime = process.env.DUM_E_NODE_MODULES || '/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const sharp = require(path.join(runtime, 'sharp'));
const root = path.resolve(__dirname, '..');
const colors = {primary:[133,45,38], mono:[41,35,31], reversed:[255,246,231]};
(async () => {
 const {data,info} = await sharp(path.join(root,'assets/logo/primary-source.png')).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const {width:w,height:h}=info;
 // Red ink and golden accent both separate cleanly from the light cream scan.
 let left=w,top=h,right=0,bottom=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const i=(y*w+x)*3;
  if(data[i+1]<180 && data[i]-data[i+1]>28){left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);}
 }
 const pad=70;left=Math.max(0,left-pad);top=Math.max(0,top-pad);right=Math.min(w-1,right+pad);bottom=Math.min(h-1,bottom+pad);
 const cw=right-left+1,ch=bottom-top+1;
 for(const [name,color] of Object.entries(colors)){
  const out=Buffer.alloc(cw*ch*4);
  for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){
   const i=((y+top)*w+x+left)*3,j=(y*cw+x)*4;
   const r=data[i],g=data[i+1],b=data[i+2];
   const gold=g>110 && g/r>.5 && r>g*1.2 && g>b*1.35;
   let alpha=Math.max(0,Math.min(1,gold?(210-b)/157:(225-g)/168));
   if(alpha<.08)alpha=0;
   const ink=name==='primary' && gold ? [232,165,53]:color;
   out[j]=ink[0];out[j+1]=ink[1];out[j+2]=ink[2];out[j+3]=Math.round(alpha*255);
  }
  await sharp(out,{raw:{width:cw,height:ch,channels:4}}).png().toFile(path.join(root,`assets/logo/${name}.png`));
 }
 // Symbol is an exact crop of this logo's lid, not a newly drawn approximation.
 const icon=await sharp(path.join(root,'assets/logo/primary.png')).extract({left:Math.round(cw*.32),top:0,width:Math.round(cw*.36),height:Math.round(ch*.303)}).resize({width:400}).png().toBuffer();
 await sharp(icon).resize(512,512,{fit:'contain',background:'#FFF6E7'}).flatten({background:'#FFF6E7'}).png().toFile(path.join(root,'assets/logo/avatar.png'));
 await sharp(path.join(root,'assets/logo/avatar.png')).resize(48,48,{fit:'contain',background:'#FFF6E7'}).png().toFile(path.join(root,'assets/logo/favicon.png'));
 for(const name of Object.keys(colors)){
  await sharp(path.join(root,`assets/logo/${name}.png`)).flatten({background:name==='reversed'?'#852D26':'#FFF6E7'}).jpeg({quality:95}).toFile(path.join(root,`proofs/logo-${name}.jpg`));
 }
 const layers=[];
 const labels=Buffer.from('<svg width="1200" height="740"><g font-family="Arial" fill="#29231F" font-size="18"><text x="40" y="40">DUM E ODISHA / REVIEW 02 — RASTER VARIANTS AND ACTUAL DISPLAY SIZES</text><text x="40" y="320">Primary / transparent PNG</text><text x="430" y="320">Single ink</text><text x="820" y="320">Reverse on chilli</text><text x="40" y="650">180 px</text><text x="290" y="650">240 px</text><text x="650" y="650">32 px</text><text x="760" y="650">48 px</text><text x="880" y="650">64 px</text></g><rect x="790" y="60" width="370" height="235" fill="#852D26"/></svg>');
 for(const [idx,name] of ['primary','mono','reversed'].entries())layers.push({input:await sharp(path.join(root,`assets/logo/${name}.png`)).resize(280).png().toBuffer(),left:60+idx*390,top:65});
 for(const [idx,size] of [180,240].entries())layers.push({input:await sharp(path.join(root,'assets/logo/primary.png')).resize(size).png().toBuffer(),left:40+idx*250,top:380});
 for(const [idx,size] of [32,48,64].entries())layers.push({input:await sharp(path.join(root,'assets/logo/avatar.png')).resize(size).png().toBuffer(),left:650+idx*115,top:440});
 await sharp({create:{width:1200,height:740,channels:4,background:'#FFF6E7'}}).composite([{input:labels},...layers]).png().toFile(path.join(root,'proofs/logo-size-sheet.png'));
 console.log(JSON.stringify({master:[w,h],export:[cw,ch],crop:{left,top,right,bottom},format:'RGBA PNG; raster, not vector'},null,2));
})();
