const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/Users/syush/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '../sites/voice');
const docs = path.resolve(__dirname, '../docs');
const base = 'file:///' + root.replace(/\\/g, '/');
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
  page.on('console', message => { if (message.type() === 'error' && !message.text().includes('Failed to load resource')) errors.push(message.text()); });
  page.on('pageerror', error => errors.push(error.message));
  const settle = () => page.waitForTimeout(500);

  await page.goto(base + '/index.html', { waitUntil:'domcontentloaded' }); await settle();
  const home = await page.evaluate(() => ({ h1:document.querySelector('h1')?.textContent, cards:document.querySelectorAll('.article-card').length, overflow:document.documentElement.scrollWidth > window.innerWidth }));

  await page.goto(base + '/categories/voice-casting.html', { waitUntil:'domcontentloaded' }); await settle();
  const category = await page.locator('.article-card').count();

  await page.goto(base + '/guides/voice-cloning-consent-checklist.html', { waitUntil:'domcontentloaded' }); await settle();
  const article = await page.evaluate(() => ({ h1:document.querySelector('h1')?.textContent, ads:document.querySelectorAll('.ad-slot').length }));

  await page.goto(base + '/tools/voice-casting-scorecard.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-casting-clarity]').fill('5');
  await page.locator('[data-casting-emotion]').fill('4');
  await page.locator('[data-casting-form] button[type="submit"]').click();
  const quoteResult = await page.locator('[data-casting-result]').innerText();

  await page.goto(base + '/tools/narration-pacing-calculator.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-pacing-form] button[type="submit"]').click();
  const sopResult = await page.locator('[data-pacing-result]').innerText();

  await page.goto(base + '/tools/dubbing-cost-estimator.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-dubbing-form] button[type="submit"]').click();
  const dubbingResult = await page.locator('[data-dubbing-result]').innerText();

  await page.goto(base + '/tools/subtitle-cps-calculator.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-cps-form] button[type="submit"]').click();
  const cpsResult = await page.locator('[data-cps-result]').innerText();

  await page.goto(base + '/tools/voice-cloning-consent-builder.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-consent-form] button[type="submit"]').click();
  const consentResult = await page.locator('[data-consent-result]').innerText();

  await page.goto(base + '/tools/synthetic-voice-disclosure-builder.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.locator('[data-disclosure-form] button[type="submit"]').click();
  const disclosureResult = await page.locator('[data-disclosure-result]').innerText();

  await page.setViewportSize({ width:390, height:844 });
  await page.goto(base + '/index.html', { waitUntil:'domcontentloaded' }); await settle();
  await page.getByRole('button', { name:'Toggle navigation' }).click();
  const mobile = await page.evaluate(() => ({ overflow:document.documentElement.scrollWidth > window.innerWidth, nav:document.querySelector('[data-site-nav]')?.classList.contains('is-open') }));

  console.log(JSON.stringify({ home, category, article, quoteResult, sopResult, dubbingResult, cpsResult, consentResult, disclosureResult, mobile, errors }, null, 2));
  await browser.close(); server.close();
})().catch(error => { console.error(error); server.close(); process.exit(1); });
