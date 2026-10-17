const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const sharp=require(path.join(runtime,'sharp')),{chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'../explorations/round-03');
const matrix=JSON.parse(fs.readFileSync(path.join(root,'sources/script-matrix.json')));
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.DUM_E_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage({viewport:{width:1800,height:1200}}),errors=[],exports=[],checks=[],switches=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
 async function open(name){await page.goto(pathToFileURL(path.join(root,name+'.html')).href);await page.evaluate(()=>document.fonts.ready);await page.locator('img').evaluateAll(async xs=>Promise.all(xs.map(x=>x.decode())));}
 for(const script of ['hindi','odia'])for(const position of ['initial','middle','end','wordmark']){
  await open(`${script}-${position}-artwork`);
  const proof=await page.locator('.logo-art').evaluate(x=>{
   const bounds=x.getBoundingClientRect();
   return {width:bounds.width,height:bounds.height,text:[...x.querySelectorAll('.name-line span')].map(y=>y.textContent).join(' '),nativeFont:getComputedStyle(x.querySelector('.native')).fontFamily,nativeFontLoaded:document.fonts.check('800 125px '+getComputedStyle(x.querySelector('.native')).fontFamily),clipped:[...x.querySelectorAll('.name-line span,.icon')].some(y=>{const b=y.getBoundingClientRect();return b.x<bounds.x||b.right>bounds.right||b.top<bounds.top||b.bottom>bounds.bottom})};
  });
  const expected=matrix.proposals[script][position==='wordmark'?matrix.primary[script]:position].join(' ');
  if(proof.text!==expected||proof.clipped||!proof.nativeFontLoaded)errors.push(`${script}-${position} layout/font/text failed: `+JSON.stringify(proof));
  const bounds=await page.locator('.logo-art').boundingBox();
  await page.screenshot({path:path.join(root,`assets/${script}-${position}.png`),omitBackground:true,clip:{x:Math.round(bounds.x),y:Math.round(bounds.y),width:1600,height:700}});
  const png=path.join(root,`assets/${script}-${position}.png`),exportMeta=await sharp(png).metadata(),alphaStats=await sharp(png).stats();
  const actual={width:exportMeta.width,height:exportMeta.height,hasAlpha:exportMeta.hasAlpha,alphaMin:alphaStats.channels[3]?.min,alphaMax:alphaStats.channels[3]?.max};
  if(actual.width!==1600||actual.height!==700||!actual.hasAlpha||actual.alphaMin!==0||actual.alphaMax!==255)errors.push(`${script}-${position} export dimensions/alpha failed`);
  exports.push({file:`${script}-${position}.png`,...proof,actual});
 }
 await open('host-display');await page.locator('.display').screenshot({path:path.join(root,'assets/host-display.png')});
 await page.locator('[contenteditable]').fill('A warm welcome.');const editable=(await page.locator('[contenteditable]').textContent())==='A warm welcome.';
 for(const name of ['index','handi-host','hindi','odia','reference-study'])for(const width of [1440,390,320]){
  await page.setViewportSize({width,height:950});await open(name);
  checks.push({page:name,width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),missingAlt:await page.locator('img:not([alt])').count()});
 }
 for(const script of ['hindi','odia']){
  await open(script);
  for(const position of ['initial','middle','end']){
   await page.locator(`[data-position=${position}]`).click();await page.locator('#script-logo').evaluate(x=>x.decode());
   switches.push({script,position,text:await page.locator('#script-reading').textContent(),expected:matrix.proposals[script][position].join(' '),pressed:await page.locator(`[data-position=${position}]`).getAttribute('aria-pressed'),download:await page.locator('#script-download').getAttribute('href'),editableLink:await page.locator('#editable-link').getAttribute('href')});
  }
 }
 await page.setViewportSize({width:1440,height:1000});
 for(const name of ['index','handi-host','hindi','odia']){await open(name);await page.screenshot({path:path.join(root,`proofs/${name}-desktop.png`)});if(name==='handi-host')await page.locator('.small-proof').screenshot({path:path.join(root,'proofs/small-size-proof.png')});}
 await page.setViewportSize({width:390,height:844});await open('index');await page.screenshot({path:path.join(root,'proofs/index-mobile.png'),fullPage:true});
 await page.keyboard.press('Tab');const skipFocused=await page.evaluate(()=>document.activeElement.classList.contains('skip'));
 const links=[];for(const relative of ['../index.html','../../index.html','../../../../index.html']){await page.goto(pathToFileURL(path.join(root,relative)).href);links.push({page:relative,newLinks:await page.locator('a[href*="round-03"]').count(),overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});}
 const host=await sharp(path.join(root,'assets/handi-host.png')).metadata(),stamp=await sharp(path.join(root,'assets/handi-stamp-source.png')).metadata();
 const stats=await sharp(path.join(root,'assets/handi-host.png')).stats();
 const failures=checks.filter(x=>x.overflow||x.missingAlt);const switchFailures=switches.filter(x=>x.text!==x.expected||x.pressed!=='true'||!x.download.endsWith(`${x.script}-${x.position}.png`)||x.editableLink!==`${x.script}-${x.position}-artwork.html`);
 const report={date:new Date().toISOString(),exports,host:{width:host.width,height:host.height,hasAlpha:host.hasAlpha,alphaMin:stats.channels[3]?.min,alphaMax:stats.channels[3]?.max},stamp:{width:stamp.width,height:stamp.height},checks,switches,links,editable,skipFocused,errors,failures,switchFailures};
 fs.writeFileSync(path.join(root,'proofs/browser-checks.json'),JSON.stringify(report,null,2)+'\n');
 fs.writeFileSync(path.join(root,'proofs/export-alpha-checks.json'),JSON.stringify(exports.map(x=>({file:x.file,...x.actual})),null,2)+'\n');
 console.log(JSON.stringify(report,null,2));await browser.close();
 if(errors.length||failures.length||switchFailures.length||!editable||!skipFocused||links.some(x=>!x.newLinks||x.overflow)||!host.hasAlpha)process.exitCode=1;
})();
