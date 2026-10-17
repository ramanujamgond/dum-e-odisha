const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const sharp=require(path.join(runtime,'sharp')),{chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../explorations/dum-club-refinement');
(async()=>{
 const source=path.join(root,'assets/negative-space-primary.png'),meta=await sharp(source).metadata();
 // Actual-artwork crops for inspecting the kernel and lid, not standalone icons.
 await sharp(source).extract({left:85,top:350,width:260,height:280}).flatten({background:'#FFF3DD'}).resize(520).png().toFile(path.join(root,'proofs/rice-counter-detail.png'));
 await sharp(source).extract({left:225,top:85,width:610,height:250}).flatten({background:'#FFF3DD'}).resize(850).png().toFile(path.join(root,'proofs/lid-detail.png'));
 const dimensions=[];
 for(const name of ['brand-system','wall-concept']){
  const file=path.join(root,`assets/${name}.png`),m=await sharp(file).metadata();dimensions.push({file:path.basename(file),width:m.width,height:m.height});
  await sharp(file).resize({width:2000,withoutEnlargement:true}).webp({quality:92}).toFile(file.replace('.png','.webp'));
 }
 const browser=await chromium.launch({headless:true,executablePath:process.env.DUM_E_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:2200,height:1400}}),errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
 await page.goto(pathToFileURL(path.join(root,'tv-display.html')).href);await page.locator('img').evaluateAll(async list=>Promise.all(list.map(x=>x.decode())));
 await page.locator('.canvas').screenshot({path:path.join(root,'assets/tv-display.png')});
 const columns=await page.locator('.canvas').evaluate(x=>({width:x.clientWidth,height:x.clientHeight,identityWidth:x.querySelector('.identity').getBoundingClientRect().width,messageWidth:x.querySelector('.message').getBoundingClientRect().width}));
 const actualPhi=columns.identityWidth/columns.messageWidth;
 await page.locator('[contenteditable]').fill('Flavour in Every Layer.');
 const editWorks=(await page.locator('[contenteditable]').textContent())==='Flavour in Every Layer.';
 for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:950});await page.goto(pathToFileURL(path.join(root,'index.html')).href);
  await page.locator('img').evaluateAll(async list=>Promise.all(list.map(x=>x.decode())));
  checks.push({width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),missingAlt:await page.locator('img:not([alt])').count()});
 }
 await page.locator('[data-variant=faithful]').click();await page.locator('#active-logo').evaluate(x=>x.decode());
 const faithfulSwitch={pressed:await page.locator('[data-variant=faithful]').getAttribute('aria-pressed'),download:await page.locator('#active-download').getAttribute('href')};
 await page.locator('[data-variant=negative-space]').click();await page.locator('#active-logo').evaluate(x=>x.decode());
 const negativeSwitch={pressed:await page.locator('[data-variant=negative-space]').getAttribute('aria-pressed'),download:await page.locator('#active-download').getAttribute('href')};
 await page.setViewportSize({width:1440,height:1000});await page.goto(pathToFileURL(path.join(root,'index.html')).href);
 await page.screenshot({path:path.join(root,'proofs/guide-desktop.png')});
 await page.locator('#geometry').screenshot({path:path.join(root,'proofs/geometry-section.png')});
 await page.setViewportSize({width:390,height:844});await page.goto(pathToFileURL(path.join(root,'index.html')).href);
 await page.screenshot({path:path.join(root,'proofs/guide-mobile.png')});
 await page.keyboard.press('Tab');const skipFocused=await page.evaluate(()=>document.activeElement.classList.contains('skip'));
 const g=JSON.parse(fs.readFileSync(path.join(root,'sources/geometry.json')));
 const failed=checks.filter(x=>x.overflow||x.missingAlt);
 const report={date:new Date().toISOString(),dimensions,normalizedMaster:meta.width+'x'+meta.height,checks,faithfulSwitch,negativeSwitch,editWorks,skipFocused,tv:columns,tvWidthRatio:actualPhi,phi:g.phi,measuredNameWidthRatio:g.mainWidth/g.subWidth,nameWidthRatioRelativeErrorPercent:Math.abs(g.mainWidth/g.subWidth-g.phi)/g.phi*100,errors,failed};
 fs.writeFileSync(path.join(root,'proofs/browser-checks.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report,null,2));await browser.close();
 if(errors.length||failed.length||!editWorks||!skipFocused||Math.abs(actualPhi-g.phi)>.001||faithfulSwitch.pressed!=='true'||negativeSwitch.pressed!=='true')process.exitCode=1;
})();
