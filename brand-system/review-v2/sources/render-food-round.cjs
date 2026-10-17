const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const sharp=require(path.join(runtime,'sharp')),{chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../explorations/round-02');
const routes=JSON.parse(fs.readFileSync(path.join(root,'directions.json'))).routes;
(async()=>{
 const dimensions=[];
 for(const r of routes){
  for(const kind of ['logo','brand']){
   const file=path.join(root,`assets/${r.slug}-${kind}.png`);
   const meta=await sharp(file).metadata();dimensions.push({file:path.basename(file),width:meta.width,height:meta.height});
   let pipeline=sharp(file);
   if(kind==='logo')pipeline=pipeline.trim({threshold:35}).extend({top:60,bottom:60,left:60,right:60,background:'#FFF6E7'});
   await pipeline.resize({width:kind==='logo'?1100:2000,withoutEnlargement:true}).webp({quality:kind==='logo'?95:92}).toFile(file.replace('.png','.webp'));
  }
 }
 const browser=await chromium.launch({headless:true,executablePath:process.env.DUM_E_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage();const errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
 for(const name of ['index','reference-study',...routes.map(x=>x.slug)])for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:950});
  await page.goto(pathToFileURL(path.join(root,`${name}.html`)).href);
  await page.locator('img').evaluateAll(async images=>Promise.all(images.map(x=>x.decode())));
  checks.push({page:name,width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),headings:await page.locator('h1').count(),missingAlt:await page.locator('img:not([alt])').count()});
 }
 await page.setViewportSize({width:1440,height:1000});
 for(const name of ['index',...routes.map(x=>x.slug)]){
  await page.goto(pathToFileURL(path.join(root,`${name}.html`)).href);
  await page.screenshot({path:path.join(root,`proofs/${name}-desktop.png`)});
 }
 await page.setViewportSize({width:390,height:844});await page.goto(pathToFileURL(path.join(root,'index.html')).href);
 await page.screenshot({path:path.join(root,'proofs/index-mobile.png'),fullPage:true});
 const linkedChecks=[];
 for(const rel of ['../index.html','../../index.html']){
  await page.goto(pathToFileURL(path.join(root,rel)).href);
  linkedChecks.push({page:rel,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),newCollectionLinks:await page.locator('a[href*="round-02"]').count()});
 }
 const failures=checks.filter(x=>x.overflow||x.headings!==1||x.missingAlt);
 const report={date:new Date().toISOString(),dimensions,checks,linkedChecks,errors,failures};
 fs.writeFileSync(path.join(root,'proofs/browser-checks.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({pages:6,widths:[1440,390,320],dimensions,linkedChecks,errors,failures},null,2));
 await browser.close();if(errors.length||failures.length||linkedChecks.some(x=>x.overflow||!x.newCollectionLinks))process.exitCode=1;
})();
