const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/Users/syush/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const root = path.resolve('C:/Users/syush/Documents/ChatGPT/廣告收入設定/site');
const mime = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.svg':'image/svg+xml', '.xml':'application/xml', '.txt':'text/plain', '.json':'application/json', '.webmanifest':'application/manifest+json' };

const server = http.createServer((req, res) => {
  const urlPath = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname);
  let filePath = path.join(root, urlPath === '/' ? 'index.html' : urlPath);
  if (!filePath.startsWith(root)) { res.writeHead(403).end(); return; }
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) filePath = path.join(filePath, 'index.html');
  fs.readFile(filePath, (error, data) => {
    if (error) { res.writeHead(404).end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': mime[path.extname(filePath)] || 'application/octet-stream' });
    res.end(data);
  });
});

(async () => {
  await new Promise(resolve => server.listen(4173, '127.0.0.1', resolve));
  const browser = await chromium.launch({ headless:true, executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport:{ width:1440, height:1000 }, deviceScaleFactor:1 });
  const errors = [];
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('pageerror', error => errors.push(error.message));

  await page.goto('http://127.0.0.1:4173/', { waitUntil:'networkidle' });
  await page.screenshot({ path:'C:/Users/syush/Documents/ChatGPT/廣告收入設定/site-home.png', fullPage:true });
  const home = await page.evaluate(() => ({ title:document.title, h1:document.querySelector('h1')?.textContent, overflow:document.documentElement.scrollWidth > window.innerWidth }));

  await page.goto('http://127.0.0.1:4173/directory.html', { waitUntil:'networkidle' });
  const allCount = await page.locator('[data-tool-row]:visible').count();
  await page.getByRole('button', { name:'Coding' }).click();
  const codingCount = await page.locator('[data-tool-row]:visible').count();
  await page.locator('[data-filter-search]').fill('video');
  await page.getByRole('button', { name:'All tools' }).click();
  const videoCount = await page.locator('[data-tool-row]:visible').count();
  await page.screenshot({ path:'C:/Users/syush/Documents/ChatGPT/廣告收入設定/site-directory.png', fullPage:true });

  await page.goto('http://127.0.0.1:4173/tools/chatgpt.html', { waitUntil:'networkidle' });
  const toolTitle = await page.locator('h1').first().textContent();
  await page.goto('http://127.0.0.1:4173/guides/best-ai-tools-for-small-business.html', { waitUntil:'networkidle' });
  const guideTitle = await page.locator('h1').first().textContent();

  await page.setViewportSize({ width:390, height:844 });
  await page.goto('http://127.0.0.1:4173/', { waitUntil:'networkidle' });
  await page.getByRole('button', { name:'Toggle navigation' }).click();
  const mobileNavOpen = await page.locator('[data-site-nav]').evaluate(element => element.classList.contains('is-open'));
  const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  await page.screenshot({ path:'C:/Users/syush/Documents/ChatGPT/廣告收入設定/site-mobile.png', fullPage:true });

  console.log(JSON.stringify({ home, allCount, codingCount, videoCount, toolTitle, guideTitle, mobileNavOpen, mobileOverflow, errors }, null, 2));
  await browser.close();
  server.close();
})().catch(error => { console.error(error); server.close(); process.exit(1); });

