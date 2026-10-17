const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const sharp=require(path.join(runtime,'sharp')),{chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../explorations');
const routes=['current','letter-and-lid','odia-first','hindi-signature'];
(async()=>{
 for(const slug of routes){
  if(slug!=='current')await sharp(path.join(root,`assets/${slug}-logo.png`)).trim({threshold:35}).extend({top:60,bottom:60,left:60,right:60,background:'#FFF6E7'}).resize({width:1100,height:850,fit:'inside',withoutEnlargement:true}).webp({quality:94}).toFile(path.join(root,`assets/${slug}-logo-preview.webp`));
  await sharp(path.join(root,`assets/${slug}-wall.png`)).resize({width:1800,withoutEnlargement:true}).webp({quality:91}).toFile(path.join(root,`assets/${slug}-wall.webp`));
 }
 const browser=await chromium.launch({headless:true,executablePath:process.env.DUM_E_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:2200,height:2100},deviceScaleFactor:1});
 const errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
 for(const slug of routes)for(const medium of ['banner','tv','standee']){
  await page.goto(pathToFileURL(path.join(root,`${slug}-${medium}.html`)).href);
  await page.locator('img').evaluateAll(async imgs=>Promise.all(imgs.map(x=>x.decode())));
  await page.locator('.canvas').screenshot({path:path.join(root,`assets/${slug}-${medium}.png`)});
  const geometry=await page.locator('.canvas').evaluate(x=>({width:x.clientWidth,height:x.clientHeight,overflow:x.scrollWidth>x.clientWidth||x.scrollHeight>x.clientHeight}));
  checks.push({page:`${slug}-${medium}`,geometry});
 }
 for(const filename of ['index','current','letter-and-lid','odia-first','hindi-signature','type-lab','reference-study'])for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:950});
  await page.goto(pathToFileURL(path.join(root,`${filename}.html`)).href);
  await page.evaluate(()=>document.fonts.ready);
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  checks.push({page:filename,width,overflow});
 }
 await page.goto(pathToFileURL(path.join(root,'type-lab.html')).href);
 const fontLoads={};for(const name of ['Odia Serif','Odia Sans','Hindi Serif','Hindi Sans'])fontLoads[name]=await page.evaluate(async n=>(await document.fonts.load(`700 48px "${n}"`)).length>0,name);
 await page.locator('[data-specimen="odia-specimen"]').selectOption('odia-sans');
 const odiaSwitch=await page.locator('#odia-specimen').getAttribute('class');
 await page.locator('[data-specimen="hindi-specimen"]').selectOption('hindi-sans');
 const hindiSwitch=await page.locator('#hindi-specimen').getAttribute('class');
 const exactScriptStrings=await page.locator('.specimen').allTextContents();
 await page.setViewportSize({width:1440,height:1000});
 for(const name of ['index','current','odia-first','type-lab']){
  await page.goto(pathToFileURL(path.join(root,`${name}.html`)).href);await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:path.join(root,`proofs/${name}-desktop.png`)});
 }
 await page.setViewportSize({width:390,height:844});
 await page.goto(pathToFileURL(path.join(root,'type-lab.html')).href);await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:path.join(root,'proofs/type-lab-mobile.png'),fullPage:true});
 await page.goto(pathToFileURL(path.join(root,'../index.html')).href);
 const mainOverflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 await page.locator('#ideas').screenshot({path:path.join(root,'proofs/main-index-ideas.png')});
 const failed=checks.filter(x=>x.overflow||x.geometry?.overflow);
 const report={date:new Date().toISOString(),checks,fontLoads,odiaSwitch,hindiSwitch,exactScriptStrings,mainOverflow,errors,failed};
 fs.writeFileSync(path.join(root,'proofs/browser-checks.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({displayExports:12,readablePages:7,widths:[1440,390,320],fontLoads,odiaSwitch,hindiSwitch,exactScriptStrings,mainOverflow,errors,failed},null,2));
 await browser.close();if(errors.length||failed.length||mainOverflow||Object.values(fontLoads).some(x=>!x))process.exitCode=1;
})();
