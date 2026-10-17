const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.DUM_E_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage();
 const errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('requestfailed',r=>errors.push(r.url()+': '+r.failure()?.errorText));
 for(const file of fs.readdirSync(path.join(root,'docs')).filter(x=>x.endsWith('.html'))){
  for(const width of [1440,390,320]){
   await page.setViewportSize({width,height:900});
   await page.goto(pathToFileURL(path.join(root,'docs',file)).href);
   checks.push({file,width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),heading:await page.locator('h1').count(),markdownLinks:await page.locator('a[href$=".md"]').count()});
  }
 }
 await page.setViewportSize({width:1440,height:1000});
 await page.goto(pathToFileURL(path.join(root,'docs/brand-guidelines.html')).href);
 await page.screenshot({path:path.join(root,'proofs/document-desktop.png')});
 await page.goto(pathToFileURL(path.join(root,'docs/index.html')).href);
 await page.screenshot({path:path.join(root,'proofs/document-library.png')});
 await page.setViewportSize({width:390,height:844});
 await page.goto(pathToFileURL(path.join(root,'docs/public-research.html')).href);
 await page.screenshot({path:path.join(root,'proofs/document-mobile.png')});
 const tableScroll=await page.locator('.table-scroll').first().evaluate(x=>({contained:x.clientWidth<=innerWidth,canScroll:x.scrollWidth>x.clientWidth}));
 await page.goto(pathToFileURL(path.join(root,'docs/logo-system.html')).href);
 await page.keyboard.press('Tab');
 const skipFocused=await page.evaluate(()=>document.activeElement.classList.contains('skip'));
 await page.keyboard.press('Enter');
 const skipWorked=await page.evaluate(()=>location.hash==='#article');
 const failed=checks.filter(x=>x.overflow||x.heading!==1||x.markdownLinks);
 const report={date:new Date().toISOString(),method:'Installed Chrome via Playwright; file:// URLs',pages:checks.length/3,widths:[1440,390,320],checks,tableScroll,skipFocused,skipWorked,errors,failed};
 fs.writeFileSync(path.join(root,'proofs/document-checks.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({pages:report.pages,widths:report.widths,tableScroll,skipFocused,skipWorked,errors,failed},null,2));
 await browser.close();
 if(errors.length||failed.length||!skipFocused||!skipWorked)process.exitCode=1;
})();
