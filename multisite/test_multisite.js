const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/Users/syush/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve('C:/Users/syush/.codex/worktrees/1ea4/廣告收入設定/sites');
const mime = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.xml':'application/xml','.txt':'text/plain','.json':'application/json','.webmanifest':'application/manifest+json'};
const server = http.createServer((req,res)=>{
  const urlPath = decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
  let file = path.join(root,urlPath === '/' ? 'index.html' : urlPath);
  if(!file.startsWith(root)){res.writeHead(403).end();return;}
  if(!fs.existsSync(file)||fs.statSync(file).isDirectory()) file=path.join(file,'index.html');
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404).end();return;}res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(data);});
});
(async()=>{
  await new Promise(r=>server.listen(4180,'127.0.0.1',r));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage({viewport:{width:1280,height:900}});
  await page.route('**/*',route=>route.request().url().includes('127.0.0.1:4180')?route.continue():route.abort());
  const results=[];
  const sites=fs.readdirSync(root,{withFileTypes:true}).filter(x=>x.isDirectory()).map(x=>x.name);
  for(const site of sites){
    const errors=[]; page.removeAllListeners('console'); page.removeAllListeners('pageerror');
    page.on('console',m=>{if(m.type()==='error')errors.push(m.text())}); page.on('pageerror',e=>errors.push(e.message));
    await page.goto(`http://127.0.0.1:4180/${site}/`,{waitUntil:'domcontentloaded'});
    const data=await page.evaluate(()=>({title:document.title,h1:document.querySelector('h1')?.textContent,client:window.SIGNALSHELF_ADSENSE_CLIENT||null,links:document.querySelectorAll('.tool-row a').length,overflow:document.documentElement.scrollWidth>window.innerWidth}));
    results.push({site,...data,errors});
  }
  console.log(JSON.stringify(results,null,2));
  await browser.close(); server.close();
})().catch(e=>{console.error(e);server.close();process.exit(1);});
