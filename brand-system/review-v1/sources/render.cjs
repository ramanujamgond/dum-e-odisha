const fs=require('fs'),path=require('path');
const sharp=require('/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=path.resolve(__dirname,'..');
(async()=>{for(const dir of ['assets/logo','applications'])for(const name of fs.readdirSync(path.join(root,dir)).filter(x=>x.endsWith('.svg'))){await sharp(path.join(root,dir,name)).png().toFile(path.join(root,'proofs',name.replace('.svg','.png')))}
 const layers=[];for(const [i,mode] of ['primary','mono','reversed'].entries()){layers.push({input:await sharp(path.join(root,'assets/logo',mode+'.svg')).resize(320).png().toBuffer(),left:40+i*380,top:80})}
 layers.push({input:await sharp(path.join(root,'assets/logo/primary.svg')).resize(160).png().toBuffer(),left:40,top:380});
 for(const [i,size] of [16,24,32,48].entries())layers.push({input:await sharp(path.join(root,'assets/logo/compact.svg')).resize(size).png().toBuffer(),left:280+i*90,top:390});
 const labels=Buffer.from('<svg width="1200" height="540"><g font-family="Arial" fill="#29231F" font-size="20"><text x="40" y="40">DUM E ODISHA / REVIEW V1 — VECTOR PROOFS</text><text x="40" y="330">Primary</text><text x="420" y="330">Single ink</text><text x="800" y="330">Reversed</text><text x="40" y="515">160 px lockup</text><text x="280" y="465">16</text><text x="370" y="465">24</text><text x="460" y="465">32</text><text x="550" y="465">48 px</text></g><rect x="780" y="60" width="380" height="245" rx="12" fill="#852D26"/></svg>');
 await sharp({create:{width:1200,height:540,channels:4,background:'#FFF6E7'}}).composite([{input:labels},...layers]).png().toFile(path.join(root,'proofs/logo-proof-sheet.png'));
 console.log('Rendered logo variants, applications and size proof');})();
