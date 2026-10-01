from __future__ import annotations
import importlib.util, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'multisite' / 'build_multisite.py'
spec = importlib.util.spec_from_file_location('build_multisite', MODULE_PATH)
bm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bm)
OUT_ROOT = ROOT / 'sites'
PACK_ROOT = ROOT / 'multisite' / 'article-packs'
THEME_ROOT = ROOT / 'multisite' / 'themes'


def render_article(site, article):
    picks = [bm.get_tool(slug) for slug in article['picks']]
    intro = article.get('intro', article['focus'])
    workflow = article.get('workflow', [])
    faq = article.get('faq', [])
    pick_html = ''.join(
        f'<h3><a href="../tools/{bm.esc(tool["slug"])}.html">{bm.esc(tool["name"])}</a></h3>'
        f'<p>{bm.esc(tool["tagline"])} Best for: {bm.esc(tool["best_for"])}. Watch for: {bm.esc(tool["limits"][0])}.</p>'
        for tool in picks
    )
    workflow_html = ''.join(f'<li>{bm.esc(item)}</li>' for item in workflow)
    faq_html = ''.join(f'<h3>{bm.esc(item["q"])}</h3><p>{bm.esc(item["a"])}</p>' for item in faq)
    sources = ''.join(f'<li><a href="{bm.esc(tool["url"])}" target="_blank" rel="noopener">{bm.esc(tool["name"])} official site</a></li>' for tool in picks)
    body = f'''<article><header class="site-shell article-header"><nav class="breadcrumbs"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {bm.esc(article['title'])}</nav><h1>{bm.esc(article['title'])}</h1><p class="dek">{bm.esc(article['dek'])}</p><p class="article-meta">Reviewed {bm.TODAY} · {bm.esc(site['brand'])} · Research-based guide · Advertising is labeled separately</p></header><div class="site-shell content-grid"><div class="content-card prose"><p>{bm.esc(intro)}</p><div class="callout"><strong>Decision rule:</strong> keep a tool only when it improves the finished result after corrections.</div><h2>How to choose</h2><p>Use the same real task for every candidate. Record setup time, first usable result, correction time, privacy and export limits, total cost, and the person responsible for final approval.</p><h2>The shortlist</h2>{pick_html}<h2>Recommended workflow</h2><ol>{workflow_html}</ol><h2>What still needs human review</h2><p>Verify product details, pricing, rights, sources, links, and any customer or career claim before publishing. AI output is treated as a draft, not evidence.</p><h2>Verdict</h2><p>{bm.esc(article.get('verdict', article['focus']))}</p><h2>FAQ</h2>{faq_html}<h2>Sources</h2><ul>{sources}<li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener">Google Search Central: helpful content guidance</a></li></ul></div><aside class="side-stack"><div class="side-panel compact"><h2>Review note</h2><p>This page is a research-based draft. Add your own screenshots, test results, and first-hand observations where possible.</p></div></aside></div></article>'''
    return bm.page(site, article['title'], article['dek'], body, 1, f"guides/{article['slug']}.html")


def build_priority_site(site):
    articles = json.loads((PACK_ROOT / f"{site['slug']}.json").read_text(encoding='utf-8'))
    base = bm.build_site(site)
    out = OUT_ROOT / site['slug']
    guides = out / 'guides'
    shutil.rmtree(guides)
    guides.mkdir()
    cards = ''.join(
        f'<article class="article-card" data-cluster="{bm.esc(article.get("cluster","guide"))}"><h3><a href="{bm.esc(article["slug"])}.html">{bm.esc(article["title"])}</a></h3><p>{bm.esc(article["dek"])}</p><p class="article-meta">{bm.esc(article.get("cluster","guide"))}</p></article>'
        for article in articles
    )
    intro = f'<section class="site-shell page-hero"><h1>50 practical guides for {bm.esc(site["audience"])}</h1><p>{bm.esc(site["description"])}</p></section>'
    guide_index = intro + f'<section class="site-shell section"><div class="article-grid">{cards}</div></section>'
    (guides / 'index.html').write_text(bm.page(site, f"{site['topic']} guides", site['description'], guide_index, 1, 'guides/index.html'), encoding='utf-8')
    for article in articles:
        (guides / f"{article['slug']}.html").write_text(render_article(site, article), encoding='utf-8')

    tools = [bm.get_tool(slug) for slug in site['tools']]
    pages = ['index.html','directory.html','guides/index.html','about.html','privacy.html','terms.html','contact.html','disclosure.html','editorial-policy.html']
    pages += [f'tools/{tool["slug"]}.html' for tool in tools]
    pages += [f'guides/{article["slug"]}.html' for article in articles]
    base_url = bm.base_url(site)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{bm.esc(base_url + "/" + path)}</loc><lastmod>2026-10-01</lastmod></url>' for path in pages) + '</urlset>'
    (out / 'sitemap.xml').write_text(sitemap, encoding='utf-8')

    theme = (THEME_ROOT / f"{site['slug']}.css").read_text(encoding='utf-8')
    css_path = out / 'assets' / 'styles.css'
    css_path.write_text(css_path.read_text(encoding='utf-8') + '\n' + theme, encoding='utf-8')
    home_path = out / 'index.html'
    home = home_path.read_text(encoding='utf-8')
    home = home.replace('Starter articles for this niche. Add original tests and screenshots before publication.', f'50 practical guides and article briefs for {bm.esc(site["audience"])}.')
    home_path.write_text(home, encoding='utf-8')
    return {**base, 'articles':len(articles)}

results = []
for slug in ['coding','career']:
    site = next(item for item in bm.SITES if item['slug'] == slug)
    results.append(build_priority_site(site))
(ROOT / 'multisite' / 'priority-build-report.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
