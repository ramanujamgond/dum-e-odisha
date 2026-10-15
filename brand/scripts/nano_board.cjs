const sharp=require('/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const path=require('path'); const root=path.resolve(__dirname,'..');
(async()=>{
 const names=['d-aroma-paisley','e-shared-handi','f-dum-lettering'];
 const layers=await Promise.all(names.map(async(n,i)=>({input:await sharp(path.join(root,'concepts',n+'.png')).resize(560,560).png().toBuffer(),left:30+590*i,top:100})));
 const labels=Buffer.from('<svg width="1800" height="740"><g fill="#254A39" font-family="Arial"><text x="30" y="48" font-size="26" font-weight="bold">DUM E BIRYANI · THREE NEW NANO BANANA DIRECTIONS</text><text x="30" y="710" font-size="23">04 / The Aroma Paisley</text><text x="620" y="710" font-size="23">05 / The Shared Handi</text><text x="1210" y="710" font-size="23">06 / The Dum Club</text></g></svg>');
 await sharp({create:{width:1800,height:740,channels:4,background:'#FFF3DD'}}).composite([...layers,{input:labels,left:0,top:0}]).png().toFile(path.join(root,'previews/nano-concepts-board.png'));
 console.log('Nano Banana comparison board saved');
})();
