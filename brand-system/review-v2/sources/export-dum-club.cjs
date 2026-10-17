/* Separate generated ink from paper, then apply a measured raster lockup layout.
   SVG output here is a construction diagram containing raster, not a vector logo. */
const fs=require('node:fs'),path=require('node:path');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const sharp=require(path.join(runtime,'sharp'));
const root=path.resolve(__dirname,'../explorations/dum-club-refinement');
const phi=(1+Math.sqrt(5))/2;
const mainWidth=1000,subWidth=Math.round(mainWidth/phi),gap=Math.round(mainWidth/phi**6),margin=Math.round(mainWidth/phi**5);
const colors={gold:[236,170,53],chilli:[166,56,37],ink:[41,35,31],cream:[255,243,221]};
function bbox(data,w,h,y0,y1){let l=w,r=0,t=h,b=0;for(let y=y0;y<y1;y++)for(let x=0;x<w;x++)if(data[(y*w+x)*4+3]>128){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y)};if(r<=l)throw Error('No ink found in block');return{left:l,top:t,width:r-l+1,height:b-t+1};}
(async()=>{
 const reports=[];
 for(const slug of ['faithful','negative-space']){
  const {data,info}=await sharp(path.join(root,`assets/${slug}-source.png`)).removeAlpha().raw().toBuffer({resolveWithObject:true});
  const w=info.width,h=info.height,rgba=Buffer.alloc(w*h*4),rows=Array(h).fill(0),paper=[data[0],data[1],data[2]];
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
   const i=(y*w+x)*3,j=(y*w+x)*4,r=data[i],g=data[i+1],b=data[i+2];
   // Classify the paper-to-ink colour direction, including antialiased edges.
   // A simple absolute hue threshold would turn red edge pixels gold.
   const gold=(paper[0]-r)/Math.max(1,paper[1]-g)<.36;
   let alpha=(r-b>65&&g<230)?Math.max(0,Math.min(1,gold?(paper[2]-b)/(paper[2]-53):(paper[1]-g)/(paper[1]-56))):0;
   if(alpha<.1)alpha=0;
   const c=gold?colors.gold:colors.chilli;rgba[j]=c[0];rgba[j+1]=c[1];rgba[j+2]=c[2];rgba[j+3]=Math.round(alpha*255);if(alpha>.5)rows[y]++;
  }
  const all=bbox(rgba,w,h,0,h);let best={start:0,length:0};
  for(let y=Math.floor(all.top+all.height*.48);y<all.top+all.height*.92;y++){
   if(rows[y]!==0)continue;let end=y;while(end<h&&rows[end]===0)end++;
   if(end<h&&end-y>best.length)best={start:y,length:end-y};y=end;
  }
  if(best.length<5)throw Error('No safe name-line separation: '+slug);
  const top=bbox(rgba,w,h,0,best.start),lower=bbox(rgba,w,h,best.start+best.length,h);
  // ODISHA is a one-ink line. Remove warm-paper specks wrongly classified as
  // gold, then discard tiny disconnected scan/export noise (not letter forms).
  for(let y=lower.top;y<lower.top+lower.height;y++)for(let x=lower.left;x<lower.left+lower.width;x++){
   const k=(y*w+x)*4;if(rgba[k]===colors.gold[0])rgba[k+3]=0;
  }
  const visited=new Uint8Array(lower.width*lower.height);
  for(let sy=0;sy<lower.height;sy++)for(let sx=0;sx<lower.width;sx++){
   const start=sy*lower.width+sx;if(visited[start])continue;visited[start]=1;
   const inkIndex=((sy+lower.top)*w+sx+lower.left)*4+3;if(rgba[inkIndex]<26)continue;
   const queue=[start];
   for(let q=0;q<queue.length;q++){
    const v=queue[q],vx=v%lower.width,vy=Math.floor(v/lower.width);
    for(const [nx,ny] of [[vx-1,vy],[vx+1,vy],[vx,vy-1],[vx,vy+1]]){
     if(nx<0||ny<0||nx>=lower.width||ny>=lower.height)continue;
     const n=ny*lower.width+nx;if(visited[n])continue;visited[n]=1;
     if(rgba[((ny+lower.top)*w+nx+lower.left)*4+3]>=26)queue.push(n);
    }
   }
   if(queue.length<70)for(const v of queue)rgba[((Math.floor(v/lower.width)+lower.top)*w+v%lower.width+lower.left)*4+3]=0;
  }
  const raw=sharp(rgba,{raw:{width:w,height:h,channels:4}});
  const topBuffer=await raw.clone().extract(top).png().toBuffer(),lowerBuffer=await raw.clone().extract(lower).png().toBuffer();
  await sharp(topBuffer).toFile(path.join(root,`sources/${slug}-wordmark.png`));await sharp(lowerBuffer).toFile(path.join(root,`sources/${slug}-odisha.png`));
  const main=await sharp(topBuffer).resize(mainWidth).png().toBuffer(),sub=await sharp(lowerBuffer).resize(subWidth).png().toBuffer();
  const mh=(await sharp(main).metadata()).height,sh=(await sharp(sub).metadata()).height;
  const width=mainWidth+margin*2,height=margin*2+mh+gap+sh,lowerTop=margin+mh+gap,lowerLeft=Math.round((width-subWidth)/2);
  const png=await sharp({create:{width,height,channels:4,background:'#00000000'}}).composite([{input:main,left:margin,top:margin},{input:sub,left:lowerLeft,top:lowerTop}]).png().toBuffer();
  await sharp(png).toFile(path.join(root,`assets/${slug}-primary.png`));
  await sharp(png).resize({width:1200,withoutEnlargement:true}).webp({quality:96}).toFile(path.join(root,`assets/${slug}-primary.webp`));
  const normalized=await sharp(png).raw().toBuffer();
  for(const [name,c] of [['mono',colors.ink],['reversed',colors.cream]]){
   const out=Buffer.from(normalized);for(let i=0;i<out.length;i+=4){out[i]=c[0];out[i+1]=c[1];out[i+2]=c[2];}
   await sharp(out,{raw:{width,height,channels:4}}).png().toFile(path.join(root,`assets/${slug}-${name}.png`));
  }
  reports.push({slug,source:{width:w,height:h,topInkBounds:top,odishaInkBounds:lower},export:{width,height,main:{x:margin,y:margin,width:mainWidth,height:mh},odisha:{x:lowerLeft,y:lowerTop,width:subWidth,height:sh},gap,margin},phiTarget:phi,exportWidthRatio:mainWidth/subWidth,relativeRatioErrorPercent:Math.abs(mainWidth/subWidth-phi)/phi*100,note:'Measured raster block layout, not mathematically constructed letter outlines.'});
 }
 const report={date:'2026-10-17',method:'Generated shape retained; alpha/ink export and measured name-line layout',phi,mainWidth,subWidth,gap,margin,reports};
 fs.writeFileSync(path.join(root,'sources/geometry.json'),JSON.stringify(report,null,2)+'\n');
 const r=reports.find(x=>x.slug==='negative-space'),e=r.export,scale=.8,ox=128,oy=120;
 const image=fs.readFileSync(path.join(root,'assets/negative-space-primary.png')).toString('base64');
 const x=ox+e.main.x*scale,y=oy+e.main.y*scale,lx=ox+e.odisha.x*scale,ly=oy+e.odisha.y*scale;
 const diagram=`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="${Math.ceil(e.height*scale+260)}" viewBox="0 0 1200 ${Math.ceil(e.height*scale+260)}"><rect width="1200" height="100%" fill="#FFF3DD"/><g font-family="Arial" fill="#29231F"><text x="48" y="45" font-size="20">DUM CLUB / MEASURED LAYOUT STUDY</text><text x="48" y="78" font-size="15">φ = 1.61803398875 · Main name 1000 px · ODISHA 618 px · Digital rounding recorded</text></g><image x="${ox}" y="${oy}" width="${e.width*scale}" height="${e.height*scale}" href="data:image/png;base64,${image}"/><g fill="none" stroke="#6A6356" stroke-width="1.5" stroke-dasharray="6 5"><rect x="${x}" y="${y}" width="${1000*scale}" height="${e.main.height*scale}"/><rect x="${lx}" y="${ly}" width="${618*scale}" height="${e.odisha.height*scale}"/></g><g stroke="#A63825" stroke-width="2"><path d="M${x} ${y-24}h${1000*scale}"/><path d="M${lx} ${ly+e.odisha.height*scale+25}h${618*scale}"/></g><g font-family="Arial" fill="#A63825" font-size="16"><text x="${x}" y="${y-35}">Main-name image width: 1000</text><text x="${lx}" y="${ly+e.odisha.height*scale+48}">ODISHA image width: 618</text></g><g font-family="Arial" fill="#29231F" font-size="14"><text x="48" y="${Math.ceil(e.height*scale+215)}">Gap: ${gap}px ≈ 1000/φ⁶ · Clearspace: ${margin}px ≈ 1000/φ⁵ · Width ratio: ${(1000/618).toFixed(6)}</text><text x="48" y="${Math.ceil(e.height*scale+240)}">The boxes measure placed raster components. They do not claim the generated curves are exact golden circles.</text></g></svg>`;
 fs.writeFileSync(path.join(root,'proofs/phi-layout.svg'),diagram);
 await sharp(Buffer.from(diagram)).png().toFile(path.join(root,'proofs/phi-layout.png'));
 const layers=[],labels=Buffer.from('<svg width="1200" height="650"><rect width="1200" height="650" fill="#FFF3DD"/><rect x="800" y="45" width="360" height="275" fill="#A63825"/><g font-family="Arial" fill="#29231F" font-size="18"><text x="35" y="30">NEGATIVE-SPACE VERSION / COLOUR AND SIZE PROOFS</text><text x="40" y="350">Two inks</text><text x="430" y="350">Single ink</text><text x="830" y="350">Reversed</text><text x="45" y="620">240 px</text><text x="400" y="620">180 px / inspect counters</text></g></svg>');
 for(const [i,mode] of ['primary','mono','reversed'].entries())layers.push({input:await sharp(path.join(root,`assets/negative-space-${mode}.png`)).resize(320).png().toBuffer(),left:40+i*390,top:60});
 for(const [i,size] of [240,180].entries())layers.push({input:await sharp(path.join(root,'assets/negative-space-mono.png')).resize(size).png().toBuffer(),left:45+i*355,top:400});
 await sharp({create:{width:1200,height:650,channels:4,background:'#FFF3DD'}}).composite([{input:labels},...layers]).png().toFile(path.join(root,'proofs/variants-and-sizes.png'));
 console.log(JSON.stringify(report,null,2));
})();
