const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('C:/Users/syush/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

const root = path.resolve(__dirname, '../site');
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
  await new Promise(resolve => server.listen(4173, '127.0.0.1', resolve));
  const browser = await chromium.launch({ headless:true, executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport:{ width:1440, height:1000 }, deviceScaleFactor:1 });
  const errors = [];
  const settle = () => page.waitForTimeout(600);
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('pageerror', error => errors.push(error.message));

  await page.goto('http://127.0.0.1:4173/', { waitUntil:'domcontentloaded' });
  await settle();
  await page.screenshot({ path:`${docs}/site-home.png`, fullPage:true });
  const home = await page.evaluate(() => ({ title:document.title, h1:document.querySelector('h1')?.textContent, overflow:document.documentElement.scrollWidth > window.innerWidth }));

  await page.goto('http://127.0.0.1:4173/directory.html', { waitUntil:'domcontentloaded' });
  await settle();
  const allCount = await page.locator('[data-tool-row]:visible').count();
  await page.getByRole('button', { name:'Coding' }).click();
  const codingCount = await page.locator('[data-tool-row]:visible').count();
  await page.locator('[data-filter-search]').fill('video');
  await page.getByRole('button', { name:'All tools' }).click();
  const videoCount = await page.locator('[data-tool-row]:visible').count();
  await page.screenshot({ path:`${docs}/site-directory.png`, fullPage:true });

  await page.goto('http://127.0.0.1:4173/tools/chatgpt.html', { waitUntil:'domcontentloaded' });
  await settle();
  const toolTitle = await page.locator('h1').first().textContent();
  await page.goto('http://127.0.0.1:4173/guides/best-ai-tools-for-small-business.html', { waitUntil:'domcontentloaded' });
  await settle();
  const guideTitle = await page.locator('h1').first().textContent();
  await page.goto('http://127.0.0.1:4173/guides/chatgpt-vs-gemini-editorial-plan-test.html', { waitUntil:'domcontentloaded' });
  await settle();
  const experimentTitle = await page.locator('h1').first().textContent();
  const experimentImages = await page.locator('.content-card img').count();

  await page.goto('http://127.0.0.1:4173/research/evidence-audit.html', { waitUntil:'domcontentloaded' });
  await settle();
  const auditTitle = await page.locator('h1').first().textContent();
  const auditMetrics = await page.locator('.metric-grid > div').count();

  await page.goto('http://127.0.0.1:4173/research/cost-calculator.html', { waitUntil:'domcontentloaded' });
  await settle();
  await page.locator('[data-cost-tasks]').fill('10');
  await page.locator('[data-cost-subscription]').fill('30');
  await page.locator('[data-cost-form] button[type="submit"]').click();
  const costResult = await page.locator('[data-cost-result]').innerText();

  await page.goto('http://127.0.0.1:4173/research/evaluation-scorecard.html', { waitUntil:'domcontentloaded' });
  await settle();
  const sliders = page.locator('[data-score]');
  for (let index = 0; index < await sliders.count(); index += 1) {
    await sliders.nth(index).fill('4');
  }
  await page.locator('[data-scorecard-form] button[type="submit"]').click();
  const scoreResult = await page.locator('[data-scorecard-result]').innerText();

  await page.setViewportSize({ width:390, height:844 });
  await page.goto('http://127.0.0.1:4173/', { waitUntil:'domcontentloaded' });
  await settle();
  await page.getByRole('button', { name:'Toggle navigation' }).click();
  const mobileNavOpen = await page.locator('[data-site-nav]').evaluate(element => element.classList.contains('is-open'));
  const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  await page.screenshot({ path:`${docs}/site-mobile.png`, fullPage:true });

  console.log(JSON.stringify({ home, allCount, codingCount, videoCount, toolTitle, guideTitle, experimentTitle, experimentImages, auditTitle, auditMetrics, costResult, scoreResult, mobileNavOpen, mobileOverflow, errors }, null, 2));
  await browser.close();
  server.close();
})().catch(error => { console.error(error); server.close(); process.exit(1); });


