const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/Users/syush/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '../sites/small-ops-lab');
const docs = path.resolve(__dirname, '../docs');
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
  await new Promise(resolve => server.listen(4181, '127.0.0.1', resolve));
  const browser = await chromium.launch({ headless:true, executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport:{ width:1440, height:1000 }, deviceScaleFactor:1 });
  const errors = [];
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('pageerror', error => errors.push(error.message));
  const settle = () => page.waitForTimeout(500);

  await page.goto('http://127.0.0.1:4181/', { waitUntil:'domcontentloaded' }); await settle();
  const home = await page.evaluate(() => ({ h1:document.querySelector('h1')?.textContent, cards:document.querySelectorAll('.article-card').length, overflow:document.documentElement.scrollWidth > window.innerWidth }));

  await page.goto('http://127.0.0.1:4181/categories/client-acquisition.html', { waitUntil:'domcontentloaded' }); await settle();
  const category = await page.locator('.article-card').count();

  await page.goto('http://127.0.0.1:4181/guides/find-first-five-clients-without-spam.html', { waitUntil:'domcontentloaded' }); await settle();
  const article = await page.evaluate(() => ({ h1:document.querySelector('h1')?.textContent, ads:document.querySelectorAll('.ad-slot').length }));

  await page.goto('http://127.0.0.1:4181/tools/quote-builder.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-quote-rate]').fill('80');
  await page.locator('[data-quote-hours]').fill('30');
  await page.locator('[data-quote-form] button[type="submit"]').click();
  const quoteResult = await page.locator('[data-quote-result]').innerText();

  await page.goto('http://127.0.0.1:4181/tools/sop-builder.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-sop-form] button[type="submit"]').click();
  const sopResult = await page.locator('[data-sop-result]').innerText();

  await page.setViewportSize({ width:390, height:844 });
  await page.goto('http://127.0.0.1:4181/', { waitUntil:'domcontentloaded' }); await settle();
  await page.getByRole('button', { name:'Toggle navigation' }).click();
  const mobile = await page.evaluate(() => ({ overflow:document.documentElement.scrollWidth > window.innerWidth, nav:document.querySelector('[data-site-nav]')?.classList.contains('is-open') }));

  console.log(JSON.stringify({ home, category, article, quoteResult, sopResult, mobile, errors }, null, 2));
  await browser.close(); server.close();
})().catch(error => { console.error(error); server.close(); process.exit(1); });
