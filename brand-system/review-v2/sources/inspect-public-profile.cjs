/* Optional public research only. Fresh browser context; no account sign-in. */
const fs=require('node:fs'),path=require('node:path');
const runtime=process.env.DUM_E_NODE_MODULES||'/Users/string1301/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(runtime,'playwright'));
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.DUM_E_BROWSER||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage();
 const record={checkedAt:new Date().toISOString(),source:'https://www.instagram.com/dum_e_odisha/',method:'Fresh unauthenticated browser; no sign-in or access-control bypass'};
 try{
  const response=await page.goto(record.source,{waitUntil:'domcontentloaded',timeout:20000});
  record.httpStatus=response?.status();record.finalUrl=page.url();record.title=await page.title();
  record.publicText=(await page.locator('body').innerText({timeout:5000})).slice(0,7000);
  record.metaDescription=await page.locator('meta[name=description]').getAttribute('content',{timeout:3000}).catch(()=>null);
 }catch(error){record.error=error.message;}
 fs.writeFileSync(path.resolve(__dirname,'../data/instagram-access.json'),JSON.stringify(record,null,2)+'\n');
 console.log(JSON.stringify(record,null,2));await browser.close();
})();
