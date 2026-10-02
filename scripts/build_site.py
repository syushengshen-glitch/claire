from __future__ import annotations

import argparse
import csv
import html
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SITE = BASE / 'site'
TODAY = 'October 1, 2026'

CATEGORIES = {
    'chat': 'Chat and assistants',
    'image': 'Image and design',
    'coding': 'Coding',
    'writing': 'Writing and SEO',
    'media': 'Video and audio',
    'productivity': 'Productivity',
    'business': 'Business',
}


def load_tools():
    tools = []
    for filename in ['tools_data_1.json', 'tools_data_2.json']:
        tools.extend(json.loads((Path(__file__).parent / filename).read_text(encoding='utf-8')))
    return tools


TOOLS = load_tools()


def esc(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def category_tools(category):
    return [tool for tool in TOOLS if tool['category'] == category]


def tool_by_slug(slug):
    return next(tool for tool in TOOLS if tool['slug'] == slug)


def ad_slot(kind, publisher):
    # 使用 Google Auto Ads，廣告位置由認證 CMP 與 AdSense 設定管理。
    return ''


def header(depth, current):
    prefix = '../' if depth else ''
    def current_attr(key):
        return ' aria-current="page"' if current == key else ''
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-shell header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="SignalShelf home"><span class="brand-mark" aria-hidden="true"><span></span></span><span>SignalShelf</span></a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Toggle navigation">Menu</button>
    <nav class="site-nav" data-site-nav aria-label="Primary navigation">
      <a href="{prefix}directory.html"{current_attr('directory')}>Directory</a>
      <a href="{prefix}guides/index.html"{current_attr('guides')}>Guides</a>
      <a href="{prefix}editorial-policy.html"{current_attr('method')}>Method</a>
      <a href="{prefix}about.html"{current_attr('about')}>About</a>
    </nav>
  </div>
</header>'''


def footer(depth):
    prefix = '../' if depth else ''
    return f'''<footer class="site-footer">
  <div class="site-shell">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true"><span></span></span><span>SignalShelf</span></a>
        <p>An editorial index of AI tools, built around practical work and clearly labeled advertising.</p>
      </div>
      <div><h2>Explore</h2><a href="{prefix}directory.html">Tool directory</a><a href="{prefix}guides/index.html">Practical guides</a><a href="{prefix}editorial-policy.html">Editorial method</a></div>
      <div><h2>Company</h2><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a><a href="{prefix}terms.html">Terms</a></div>
      <div><h2>Trust</h2><a href="{prefix}privacy.html">Privacy and cookies</a><a href="{prefix}disclosure.html">Affiliate disclosure</a></div>
    </div>
    <div class="footer-bottom"><span>© <span data-year>2026</span> SignalShelf. Independent editorial project.</span><span>Some links may become affiliate links after disclosure.</span><button class="text-button" type="button" data-manage-consent>Privacy choices</button></div>
  </div>
</footer>
'''


def page(title, description, body, depth=0, current='', canonical='', schema=None, publisher=None):
    prefix = '../' if depth else ''
    schema_html = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ''
    publisher_script = f'<script>window.SIGNALSHELF_ADSENSE_CLIENT={json.dumps(publisher)};</script>' if publisher else ''
    canonical_html = f'<link rel="canonical" href="{esc(canonical)}">' if canonical else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} | SignalShelf</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  {canonical_html}
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  {publisher_script}{schema_html}
</head>
<body>{header(depth, current)}<main id="main">{body}</main>{footer(depth)}<script src="{prefix}assets/app.js" defer></script></body>
</html>'''


def tool_row(tool, depth, featured=False):
    prefix = '../' if depth else ''
    tags = ''.join(f'<span class="tag">{esc(tag)}</span>' for tag in tool['tags'])
    featured_class = ' featured' if featured else ''
    search = ' '.join([tool['name'], tool['tagline'], tool['category'], *tool['tags']]).lower()
    return f'''<article class="tool-row{featured_class}" data-tool-row data-category="{esc(tool['category'])}" data-name="{esc(tool['name'])}" data-featured="{1 if tool.get('featured') else 0}" data-search="{esc(search)}">
  <div class="tool-mark" aria-hidden="true">{esc(tool['name'][0])}</div>
  <div class="tool-info"><h3><a href="{prefix}tools/{esc(tool['slug'])}.html">{esc(tool['name'])}</a></h3><p>{esc(tool['tagline'])}</p><div class="tool-meta">{tags}</div></div>
  <div class="tool-actions"><a class="button" href="{esc(tool['url'])}" target="_blank" rel="noopener">Visit site</a><a class="button secondary" href="{prefix}tools/{esc(tool['slug'])}.html">Read review</a></div>
</article>'''


def category_chips(active='all'):
    chips = [f'<button class="filter-chip" type="button" data-filter-category="all" aria-pressed="{str(active == "all").lower()}">All tools</button>']
    for key, label in CATEGORIES.items():
        chips.append(f'<button class="filter-chip" type="button" data-filter-category="{esc(key)}" aria-pressed="{str(active == key).lower()}">{esc(label)}</button>')
    return ''.join(chips)


def radar():
    nodes = ''.join(f'<span class="radar-node n{index}">{esc(label)}</span>' for index, label in enumerate(CATEGORIES.values(), 1))
    return f'''<div class="radar" aria-label="Seven AI tool categories"><div class="radar-sweep" aria-hidden="true"></div><div class="radar-center">32 tools<br>7 categories</div>{nodes}<p class="radar-caption">A live index for choosing the next tool, not a ranking of every product on the internet.</p></div>'''


def build_home(publisher, base_url):
    featured_slugs = ['chatgpt', 'github-copilot', 'runway', 'notion-ai', 'gamma', 'midjourney']
    featured = [tool_by_slug(slug) for slug in featured_slugs]
    rows = '\n'.join(tool_row(tool, 0, featured=(index == 0)) for index, tool in enumerate(featured))
    body = f'''<section class="site-shell hero">
  <div class="hero-copy"><span class="hero-note">Independent tool research for real work</span><h1>Find an AI tool you can actually keep using.</h1><p class="hero-intro">SignalShelf compares tools by the job they help you finish, the limits you should know, and the alternatives worth considering. No endless link dump.</p>
    <form class="search-panel" data-search-form data-search-target="directory.html"><label class="sr-only" for="hero-search">Search AI tools</label><input id="hero-search" name="q" type="search" placeholder="Search by task, tool, or category"><button type="submit">Search the index</button></form>
    <p class="popular-searches">Try: <a href="directory.html?q=coding">coding</a><a href="directory.html?q=free tier">free tools</a><a href="directory.html?q=video">video</a><a href="directory.html?q=meetings">meetings</a></p></div>{radar()}
</section>
<div class="site-shell signal-strip"><span><strong>32</strong> tools reviewed</span><span><strong>7</strong> practical categories</span><span>Last reviewed <strong>{TODAY}</strong></span><span>Pricing and limits are rechecked before major updates</span></div>
<section class="site-shell section"><div class="section-heading"><h2>Start with the work</h2><p>Ten guides cover the most common decisions across business, study, writing, coding, video, teams, freelancing, marketing, founding, and teaching.</p></div>
  <div class="home-layout"><div><div class="tool-list">{rows}</div><p style="margin-top:24px"><a class="text-link" href="directory.html">Browse all 32 tools</a></p></div>
  <aside class="side-stack"><div class="side-panel"><h2>How to choose</h2><ol><li>Name the finished task, not the category.</li><li>Test the free tier against your real input.</li><li>Check export, privacy, and usage limits.</li><li>Pick the least expensive tool that passes.</li></ol></div>{ad_slot('rail', publisher)}<div class="side-panel compact"><h2>Editorial rule</h2><p>Ad positions never change a tool's score, category, or placement. Sponsored inventory is labeled separately.</p></div></aside></div>
</section>{ad_slot('wide', publisher)}
<section class="site-shell section"><div class="section-heading"><h2>Guides that solve a real job</h2><p>Comparisons and workflows for small businesses, students, creators, developers, writers, and remote teams.</p></div>{guide_cards(0)}</section>'''
    schema = {'@context':'https://schema.org','@type':'WebSite','name':'SignalShelf','url':base_url.rstrip('/') + '/','description':'Independent AI tools directory with practical buying criteria and editorial guides.'}
    return page('AI tools directory with practical buying criteria', 'Browse 32 AI tools across chat, image, coding, writing, video, productivity, and business.', body, 0, '', base_url.rstrip('/') + '/index.html', schema, publisher)

def build_directory(publisher, base_url):
    rows = '\n'.join(tool_row(tool, 0) for tool in sorted(TOOLS, key=lambda tool: (not tool.get('featured'), tool['name'].lower())))
    body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Directory</nav><h1>The whole signal, minus the noise.</h1><p>Search 32 tools and filter by category. Every listing includes a practical use case, a pricing note, and a link to a deeper review.</p></section>
<section class="site-shell section" data-directory><div class="filter-bar"><label class="sr-only" for="directory-search">Search tools</label><div class="search-panel"><input id="directory-search" data-filter-search type="search" placeholder="Search by tool, task, or tag"><span class="button secondary" aria-hidden="true">Live filter</span></div><div class="filter-chips">{category_chips()}</div><div class="filter-meta"><span><strong data-result-count>32 tools</strong></span><label>Sort <select data-sort><option value="featured">Editor's starting point</option><option value="name">Name</option><option value="category">Category</option></select></label></div></div>
<div class="directory-layout"><div><div class="tool-list">{rows}</div><p class="empty-state" data-empty-state aria-hidden="true">No tool matches that search yet. Try a broader task such as “writing,” “video,” or “automation.”</p></div>
<aside class="side-stack">{ad_slot('rail', publisher)}<div class="side-panel"><h2>Pricing labels</h2><p><strong>Free tier</strong> means a usable no-cost entry point exists. <strong>Free credits</strong> means the free allowance is temporary or limited.</p></div><div class="side-panel compact"><h2>Last checked</h2><p>{TODAY}. Product packaging changes quickly, so confirm final pricing and commercial rights with the vendor.</p></div></aside></div></section>'''
    return page('AI tools directory', 'Search and filter 32 practical AI tools by category, free tier, use case, and workflow.', body, 0, 'directory', base_url.rstrip('/') + '/directory.html', publisher=publisher)


def build_tool_page(tool, publisher, base_url):
    alternatives = [item for item in category_tools(tool['category']) if item['slug'] != tool['slug']][:3]
    alt_html = ''.join(f'<li><a href="{esc(item["slug"])}.html">{esc(item["name"])}</a> — {esc(item["best_for"])}</li>' for item in alternatives)
    strengths = ''.join(f'<li>{esc(item)}</li>' for item in tool['strengths'])
    limits = ''.join(f'<li>{esc(item)}</li>' for item in tool['limits'])
    tags = ''.join(f'<span class="tag">{esc(tag)}</span>' for tag in tool['tags'])
    body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="../directory.html">Directory</a> / {esc(tool['name'])}</nav><div class="tool-profile"><div class="tool-mark" aria-hidden="true">{esc(tool['name'][0])}</div><div><h1>{esc(tool['name'])} review: what it is best for</h1><p>{esc(tool['tagline'])}</p><div class="tool-meta">{tags}</div></div></div></section>
<section class="site-shell section" style="padding-top:0"><div class="content-grid"><article class="content-card prose"><div class="callout"><strong>Quick verdict:</strong> {esc(tool['best_for'])} {esc(tool['pricing'])}</div><h2>What this tool does well</h2><ul>{strengths}</ul><h2>Limits to know before paying</h2><ul>{limits}</ul><h2>Where it fits in a workflow</h2><p>{esc(tool['name'])} is most useful when the surrounding process is already clear. Define the input, the expected output, and the review step before adding it to a team workflow. A tool that feels impressive in a demo but adds another approval loop is usually not worth the subscription.</p><p>Start with one recurring task. Measure time saved, correction effort, and the cost of the plan you would actually need. If those three numbers do not improve, keep the free tier or test a narrower alternative.</p>{ad_slot('wide', publisher)}<h2>Alternatives to consider</h2><ul>{alt_html}</ul><h2>Pricing and availability</h2><p>{esc(tool['pricing'])} Product availability, language support, and commercial terms can change by country and plan. Confirm the current details on the vendor's site before purchasing.</p><h2>Editorial note</h2><p>This review is based on official product information, the advertised use case, and the practical limits that buyers should check. It is not a paid placement. <a href="../disclosure.html">Read the disclosure policy</a>.</p><p><a class="button" href="{esc(tool['url'])}" target="_blank" rel="noopener">Open {esc(tool['name'])}</a> <button class="button secondary" type="button" data-copy-link>Copy link</button></p></article>
<aside class="side-stack"><div class="side-panel"><h2>At a glance</h2><div class="fact"><strong>Category</strong>{esc(CATEGORIES[tool['category']])}</div><div class="fact" style="margin-top:10px"><strong>Best for</strong>{esc(tool['best_for'])}</div><div class="fact" style="margin-top:10px"><strong>Pricing note</strong>{esc(tool['pricing'])}</div></div>{ad_slot('rail', publisher)}</aside></div></section>'''
    canonical = f'{base_url.rstrip("/")}/tools/{tool["slug"]}.html'
    schema = {'@context':'https://schema.org','@type':'WebPage','name':f'{tool["name"]} review','description':tool['tagline'],'url':canonical,'dateModified':'2026-10-01'}
    return page(f'{tool["name"]} review: pros, limits, pricing, and alternatives', tool['tagline'], body, 1, '', canonical, schema, publisher)


def build_category_page(key, label, publisher, base_url):
    tools = category_tools(key)
    rows = '\n'.join(tool_row(tool, 1) for tool in tools)
    body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="../directory.html">Directory</a> / {esc(label)}</nav><h1>{esc(label)} tools worth testing.</h1><p>Compare the practical strengths, limits, and pricing notes for {len(tools)} tools in this category.</p></section><section class="site-shell section" style="padding-top:0"><div class="tool-list">{rows}</div></section>'''
    canonical = f'{base_url.rstrip("/")}/category/{key}.html'
    return page(f'Best {label.lower()} AI tools', f'Compare {len(tools)} {label.lower()} AI tools by use case, strengths, limits, and pricing notes.', body, 1, '', canonical, publisher=publisher)


GUIDES = []
for filename in ['guide_articles_1.json', 'guide_articles_2.json']:
    GUIDES.extend(json.loads((Path(__file__).parent / filename).read_text(encoding='utf-8')))


def guide_cards(depth):
    prefix = '../' if depth else ''
    cards = [experiment_card(depth)] + extra_experiment_cards(depth)
    for guide in GUIDES:
        cards.append(f'''<article class="article-card"><div><h3><a href="{prefix}guides/{esc(guide['slug'])}.html">{esc(guide['title'])}</a></h3><p>{esc(guide['dek'])}</p></div><a href="{prefix}guides/{esc(guide['slug'])}.html">Read the guide</a></article>''')
    return f'<div class="article-grid">{"".join(cards)}</div>'


def experiment_card(depth):
    prefix = '../' if depth else ''
    return f'''<article class="article-card"><div><h3><a href="{prefix}guides/chatgpt-vs-gemini-editorial-plan-test.html">We gave ChatGPT and Gemini the same 7-day editorial planning task</a></h3><p>A first-hand browser test with the exact prompt, full response evidence, scoring, mistakes, and the link-validation lesson.</p></div><a href="{prefix}guides/chatgpt-vs-gemini-editorial-plan-test.html">Read the experiment</a></article>'''


def build_experiment_page(publisher, base_url):
    canonical = f'{base_url.rstrip("/")}/guides/chatgpt-vs-gemini-editorial-plan-test.html'
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': 'We gave ChatGPT and Gemini the same 7-day editorial planning task',
        'description': 'A first-hand comparison of ChatGPT and Gemini on the same AI content-planning prompt, including scoring, screenshots, and link accuracy.',
        'datePublished': '2026-10-01',
        'dateModified': '2026-10-01',
        'articleSection': 'AI experiments',
        'author': {'@type': 'Organization', 'name': 'SignalShelf Editorial Team'},
        'publisher': {'@type': 'Organization', 'name': 'SignalShelf'},
        'mainEntityOfPage': canonical
    }
    prompt_text = '''You are helping plan a 7-day editorial sprint for an English-language AI tools directory.

Audience: freelancers, small business owners, and remote teams.
Website pages available:
- ChatGPT, Claude, Gemini, Perplexity, Microsoft Copilot tool reviews
- Coding, Writing and SEO, Productivity, and Business category pages
- Guides about small business, freelancers, remote teams, and SEO writing

Create a 7-day content plan in a table with:
1. Day
2. Primary keyword
3. Search intent
4. Article title
5. Three questions the article must answer
6. Three relevant internal links
7. Facts that need verification

Rules:
- Do not invent search volume.
- Mark uncertain assumptions as [VERIFY].
- Prioritize long-tail topics over broad topics such as "best AI tools".
- Keep each article practical for the named audience.
- Return only the table and a short rationale.'''
    body = f'''<article>
  <header class="site-shell article-header">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / Experiment 001</nav>
    <h1>We gave ChatGPT and Gemini the same 7-day editorial planning task</h1>
    <p class="dek">This is a real browser test, not a synthetic comparison. Both tools received the same prompt, at the same time, with no paid features and no follow-up instructions.</p>
    <p class="article-meta">Tested October 1, 2026 · ChatGPT web and Google Gemini web (Flash) · One prompt · Both responses observed within 37 seconds</p>
  </header>
  <div class="site-shell content-grid">
    <div class="content-card prose">
      <div class="callout"><strong>Result:</strong> ChatGPT produced the more deployable plan for this specific website because its internal links used page names that already exist. Gemini produced more verification notes but invented several site paths.</div>

      <h2 id="why">Why we ran this test</h2>
      <p>AI tool reviews often claim that one assistant is better without showing the actual task. We wanted a narrower question: if both tools receive the same editorial brief, which response can a small content team use with the least correction?</p>
      <p>The test used an English-language AI tools directory as the context. This matters because a useful answer must understand the existing pages, avoid invented search volume, and propose topics that connect naturally to the site.</p>

      <h2 id="method">The test method</h2>
      <ul>
        <li>ChatGPT used the default web chat interface.</li>
        <li>Gemini used the Flash mode available in the web interface.</li>
        <li>Both tools received the same prompt in separate new conversations.</li>
        <li>No paid feature, file upload, custom instruction, or follow-up prompt was used.</li>
        <li>Both outputs were visible within 37 seconds of submission.</li>
        <li>Claude required authentication and Arena AI required reCAPTCHA, so neither was scored or represented as tested.</li>
      </ul>
      <p>This is a focused editorial-planning test, not a general benchmark of writing quality, reasoning, coding, or safety.</p>

      <h2 id="prompt">The exact prompt</h2>
      <pre><code>{esc(prompt_text)}</code></pre>

      <h2 id="results">What each tool produced</h2>
      <h3>ChatGPT</h3>
      <p>ChatGPT returned seven rows and a rationale. The plan used practical long-tail topics such as client-email writing, long-document summaries, competitor research, freelance writing comparisons, meeting notes, SEO workflows, and remote-team reporting.</p>
      <p>Its strongest feature was link context: it referred to existing page names such as the ChatGPT, Claude, Perplexity, Business, Productivity, Writing and SEO, freelancer, and remote-team pages. Those still need to be converted into exact URLs, but the content map is easier to validate.</p>
      <p><img src="../assets/experiments/001-chatgpt.png" alt="ChatGPT response to the shared 7-day editorial planning prompt" loading="lazy"></p>

      <h3>Gemini</h3>
      <p>Gemini returned a longer answer with more [VERIFY] flags. It surfaced useful questions around pricing, data retention, workspace administration, PII, and current product limits.</p>
      <p>Its material weakness was internal-link accuracy. It proposed paths such as <code>/categories/writing-and-seo</code>, <code>/guides/small-business</code>, <code>/guides/remote-teams</code>, <code>/guides/seo-writing</code>, and <code>/guides/freelancers</code>. Those are not the actual paths on this site, so the output would create broken links if published without review.</p>
      <p><img src="../assets/experiments/001-gemini.png" alt="Gemini response to the shared 7-day editorial planning prompt" loading="lazy"></p>

      <h2 id="score">How we scored the outputs</h2>
      <p>Each category is scored from 0 to 2. The scoring criteria were written before comparing the outputs.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Tool</th><th>Clarity</th><th>Specificity</th><th>Non-template</th><th>Internal links</th><th>Verification</th><th>Total</th></tr></thead>
        <tbody>
          <tr><td>ChatGPT</td><td>2</td><td>2</td><td>1</td><td>1</td><td>2</td><td>8/10</td></tr>
          <tr><td>Gemini</td><td>2</td><td>2</td><td>1</td><td>0</td><td>1</td><td>6/10</td></tr>
        </tbody>
      </table></div>
      <p>Gemini received a lower verification score because the incorrect internal paths create tangible editorial work. More words and more warnings do not compensate for links that do not exist.</p>

      <h2 id="lessons">What this changes for our workflow</h2>
      <ol>
        <li>Never trust generated internal links without checking the live sitemap and local page paths.</li>
        <li>Use a general assistant for a first content map, but keep the site structure in the prompt.</li>
        <li>Treat [VERIFY] as a task list, not evidence that the fact is correct.</li>
        <li>Do not write a tool review until the team has actually tested the tool or clearly labels the review as research-based.</li>
        <li>Score the output against the work that remains, not the confidence of the response.</li>
      </ol>

      <h2 id="verdict">Verdict</h2>
      <p>For this specific job, ChatGPT produced the more usable editorial map because its internal references were closer to the real site. Gemini produced a useful risk checklist and more detailed questions, but it would have introduced broken paths if copied directly.</p>
      <p>The practical recommendation is to use ChatGPT for the first structural draft and Gemini for a second-pass verification checklist. A human editor still has to validate every link, source, keyword assumption, and product claim.</p>

      <h2 id="sources">Sources and limits</h2>
      <p>The original prompt and full text outputs are stored in <code>content-lab/captures/</code>. Screenshots are from the browser sessions on October 1, 2026. Product interfaces, model names, limits, and outputs can change.</p>
      <ul>
        <li><a href="https://chatgpt.com/" target="_blank" rel="noopener">ChatGPT official site</a></li>
        <li><a href="https://gemini.google.com/" target="_blank" rel="noopener">Google Gemini official site</a></li>
        <li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener">Google Search Central: helpful, reliable, people-first content</a></li>
      </ul>
    </div>
    <aside class="side-stack">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#why">Why we tested</a></li><li><a href="#method">Method</a></li><li><a href="#prompt">Prompt</a></li><li><a href="#results">Results</a></li><li><a href="#score">Score</a></li><li><a href="#verdict">Verdict</a></li>
      </ol></nav>
      <div class="side-panel compact"><h2>Experiment rule</h2><p>If a tool could not be used, it is excluded from the score. It is never described as tested.</p></div>
    </aside>
  </div>
</article>'''
    return page('ChatGPT vs Gemini: the same 7-day editorial planning task', 'A first-hand ChatGPT vs Gemini test with the exact prompt, screenshots, scoring, and link-accuracy lessons.', body, 1, 'guides', canonical, schema, publisher)


EXTRA_EXPERIMENTS = json.loads((Path(__file__).parent / 'experiments_extra.json').read_text(encoding='utf-8'))


def extra_experiment_cards(depth):
    prefix = '../' if depth else ''
    cards = []
    for experiment in EXTRA_EXPERIMENTS:
        cards.append(f'''<article class="article-card"><div><h3><a href="{prefix}guides/{esc(experiment['slug'])}.html">{esc(experiment['title'])}</a></h3><p>{esc(experiment['dek'])}</p></div><a href="{prefix}guides/{esc(experiment['slug'])}.html">Read the experiment</a></article>''')
    return cards


def build_extra_experiment_page(experiment, publisher, base_url):
    canonical = f'{base_url.rstrip("/")}/guides/{experiment["slug"]}.html'
    score_keys = [key for key in experiment['scores'][0].keys() if key not in {'tool', 'total', 'note'}]
    score_headers = ''.join(f'<th>{esc(key.replace("_", " ").title())}</th>' for key in score_keys)
    score_rows = ''
    for score in experiment['scores']:
        values = ''.join(f'<td>{esc(score.get(key, ""))}</td>' for key in score_keys)
        score_rows += f'<tr><td>{esc(score["tool"])}</td>{values}<td>{esc(score["total"])}/10</td><td>{esc(score["note"])}</td></tr>'
    method_items = ''.join(f'<li>{esc(item)}</li>' for item in experiment['method'])
    findings = ''.join(f'<li>{esc(item)}</li>' for item in experiment['findings'])
    schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': experiment['title'],
        'description': experiment['dek'],
        'datePublished': '2026-10-02',
        'dateModified': '2026-10-02',
        'articleSection': 'AI experiments',
        'author': {'@type': 'Organization', 'name': 'SignalShelf Editorial Team'},
        'publisher': {'@type': 'Organization', 'name': 'SignalShelf'},
        'mainEntityOfPage': canonical
    }
    body = f'''<article>
  <header class="site-shell article-header">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / AI experiment</nav>
    <h1>{esc(experiment['title'])}</h1>
    <p class="dek">{esc(experiment['dek'])}</p>
    <p class="article-meta">Tested {esc(experiment['date'])} · {esc(experiment['tools'])} · One prompt · No paid features</p>
  </header>
  <div class="site-shell content-grid">
    <div class="content-card prose">
      <div class="callout"><strong>Result:</strong> {esc(experiment['summary'])}</div>
      <h2 id="method">Test method</h2>
      <p>{esc(experiment['task'])}</p>
      <ul>{method_items}</ul>
      <h2 id="prompt">The exact prompt</h2>
      <pre><code>{esc(experiment['prompt'])}</code></pre>
      <h2 id="results">What the tools produced</h2>
      <h3>ChatGPT</h3>
      <p><img src="../assets/experiments/{esc(experiment['screenshot_prefix'])}-chatgpt.png" alt="ChatGPT response to the shared test prompt" loading="lazy"></p>
      <h3>Gemini</h3>
      <p><img src="../assets/experiments/{esc(experiment['screenshot_prefix'])}-gemini.png" alt="Gemini response to the shared test prompt" loading="lazy"></p>
      <h2 id="score">Score</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Tool</th>{score_headers}<th>Total</th><th>Editorial note</th></tr></thead>
        <tbody>{score_rows}</tbody>
      </table></div>
      <h2 id="findings">What we found</h2>
      <ul>{findings}</ul>
      <h2 id="verdict">Verdict</h2>
      <p>{esc(experiment['verdict'])}</p>
      <h2 id="limits">Limits</h2>
      <p>This is a focused single-task test, not a general benchmark of writing quality, reasoning, coding, safety, or long-term reliability. Product interfaces, models, limits, and outputs can change.</p>
      <h2 id="sources">Sources</h2>
      <ul>
        <li><a href="https://chatgpt.com/" target="_blank" rel="noopener">ChatGPT official site</a></li>
        <li><a href="https://gemini.google.com/" target="_blank" rel="noopener">Google Gemini official site</a></li>
        <li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener">Google Search Central: helpful, reliable, people-first content</a></li>
      </ul>
    </div>
    <aside class="side-stack">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#method">Method</a></li><li><a href="#prompt">Prompt</a></li><li><a href="#results">Results</a></li><li><a href="#score">Score</a></li><li><a href="#verdict">Verdict</a></li>
      </ol></nav>
      <div class="side-panel compact"><h2>Evidence rule</h2><p>Excluded tools are not scored. Responses are saved before the article is written.</p></div>
    </aside>
  </div>
</article>'''
    return page(experiment['title'], experiment['dek'], body, 1, 'guides', canonical, schema, publisher)


def build_guides_index(publisher, base_url):
    body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Guides</nav><h1>Use AI for the job, not the novelty.</h1><p>Ten workflow guides cover common decisions across work, school, and creative projects. The newest entry is a first-hand ChatGPT vs Gemini editorial-planning experiment.</p></section><section class="site-shell section" style="padding-top:0">{guide_cards(1)}</section>{ad_slot('wide', publisher)}'''
    return page('Practical AI tool guides', 'Ten workflow-first guides for choosing and using AI tools at work, school, and in creative projects.', body, 1, 'guides', f'{base_url.rstrip("/")}/guides/index.html', publisher=publisher)


def build_guide_page(guide, publisher, base_url):
    picks = [{'tool': tool_by_slug(item['slug']), 'note': item['note']} for item in guide['picks']]
    pick_html = []
    for index, pick in enumerate(picks, 1):
        tool = pick['tool']
        pick_html.append(f'''<section class="pick"><h3 id="pick-{index}">{index}. <a href="../tools/{esc(tool['slug'])}.html">{esc(tool['name'])}</a></h3><p>{esc(pick['note'])}</p><p><strong>Relevant strength:</strong> {esc(tool['strengths'][0])}. <strong>Limit to check:</strong> {esc(tool['limits'][0])}.</p><p><a href="../tools/{esc(tool['slug'])}.html">Read the full {esc(tool['name'])} evaluation</a></p></section>''')
    toc = ''.join(f'<li><a href="#pick-{index + 1}">{esc(item["tool"]["name"])}</a></li>' for index, item in enumerate(picks))
    intro_html = ''.join(f'<p>{esc(paragraph)}</p>' for paragraph in guide['introduction'])
    factors_html = ''.join(f'<li>{esc(item)}</li>' for item in guide['decision_factors'])
    workflow_html = ''.join(f'<li>{esc(item)}</li>' for item in guide['workflow'])
    faq_html = ''.join(f'<h3>{esc(item["q"])}</h3><p>{esc(item["a"])}</p>' for item in guide['faq'])
    source_html = ''.join(f'<li><a href="{esc(item["tool"]["url"])}" target="_blank" rel="noopener">{esc(item["tool"]["name"])} official site</a></li>' for item in picks)
    source_html += '<li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener">Google Search Central: Creating helpful, reliable, people-first content</a></li>'
    source_html += '<li><a href="https://support.google.com/adsense/answer/48182" target="_blank" rel="noopener">Google AdSense Program policies</a></li>'
    canonical = f'{base_url.rstrip("/")}/guides/{guide["slug"]}.html'
    schema = {'@context':'https://schema.org','@type':'Article','headline':guide['title'],'description':guide['dek'],'datePublished':'2026-10-01','dateModified':'2026-10-01','articleSection':'AI tools','author':{'@type':'Organization','name':'SignalShelf Editorial Team'},'publisher':{'@type':'Organization','name':'SignalShelf'},'mainEntityOfPage':canonical}
    body = f'''<article><header class="site-shell article-header"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {esc(guide['title'])}</nav><h1>{esc(guide['title'])}</h1><p class="dek">{esc(guide['dek'])}</p><p class="article-meta">Reviewed {TODAY} · Research-based editorial guide · Advertising is labeled separately</p></header>
<div class="site-shell content-grid"><div class="content-card prose">{intro_html}<div class="callout"><strong>Decision rule:</strong> keep a tool only when it improves the finished result after corrections. A fast first draft is not a win if it creates more review work.</div><h2 id="how-to-choose">How to choose</h2><p>{esc(guide['focus'])} Start with one measurable job and use the same test material across every candidate.</p><ul>{factors_html}</ul>{ad_slot('wide', publisher)}<h2 id="shortlist">The shortlist</h2>{''.join(pick_html)}<h2 id="workflow">A workflow that stays under control</h2><ol>{workflow_html}</ol><h2 id="verdict">Verdict</h2><p>{esc(guide['verdict'])}</p><h2 id="faq">Frequently asked questions</h2>{faq_html}<h2 id="sources">Sources and research notes</h2><p>This guide was reviewed on {TODAY} using official product information and the policy sources below. Pricing, availability, feature names, and commercial terms can change; confirm current details with each vendor before purchase.</p><ul>{source_html}</ul></div>
<aside class="side-stack"><nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>{toc}<li><a href="#workflow">Workflow</a></li><li><a href="#verdict">Verdict</a></li><li><a href="#faq">FAQ</a></li><li><a href="#sources">Sources</a></li></ol></nav>{ad_slot('rail', publisher)}<div class="side-panel compact"><h2>Review method</h2><p>Tools are judged by the job they solve, limits to verify, export and privacy considerations, and the total correction cost.</p></div></aside></div></article>'''
    return page(guide['title'], guide['dek'], body, 1, 'guides', canonical, schema, publisher)


def linkify(value):
    escaped = esc(value)

    def replace_url(match):
        url = match.group(1)
        trailing = ''
        while url and url[-1] in '.,);':
            trailing = url[-1] + trailing
            url = url[:-1]
        return f'<a href="{esc(url)}" rel="noopener">{esc(url)}</a>{trailing}'

    return re.sub(r'(https?://[^\s<]+)', replace_url, escaped)


def build_simple_page(title, description, heading, paragraphs, depth, current, base_url, publisher, path):
    body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{'../' if depth else ''}index.html">Home</a> / {esc(heading)}</nav><h1>{esc(heading)}</h1><p>{esc(description)}</p></section><section class="site-shell section" style="padding-top:0"><div class="content-grid"><article class="content-card prose">{''.join(f'<p>{linkify(item)}</p>' for item in paragraphs)}</article><aside class="side-stack">{ad_slot('rail', publisher)}</aside></div></section>'''
    return page(title, description, body, depth, current, f'{base_url.rstrip("/")}/{path}', publisher=publisher)


def write_static_pages(publisher, base_url):
    pages = {
        'about.html': build_simple_page(
            'About SignalShelf',
            'SignalShelf is an independent AI tools directory focused on practical use, transparent limitations, and clearly separated advertising.',
            'About SignalShelf',
            [
                'SignalShelf helps readers compare AI products by the job they need to finish, the limitations they should verify, and the workflow around the tool. The directory is intentionally smaller and more structured than a general software marketplace.',
                'Every listing is reviewed against the same criteria: intended user, practical strength, material limitation, pricing note, export and privacy considerations, and a realistic alternative. Product claims should be confirmed with the vendor because plans, features, availability, and commercial terms change.',
                'The project uses public product information and editorial judgment. It does not claim that every tool has been purchased or benchmarked. When first-hand testing, screenshots, or expert review are added, the article should identify those materials and their date.',
                'Advertising may fund the site. Ads are labeled and kept separate from editorial placement. A commercial relationship does not change the inclusion criteria, category, or limitations shown on a page.',
                'Corrections and source-backed feedback are welcome through the monitored contact channel listed on the Contact page.'
            ], 0, 'about', base_url, publisher, 'about.html'
        ),
        'privacy.html': build_simple_page(
            'Privacy and cookies',
            'How SignalShelf handles local storage, hosting data, advertising consent, external links, and privacy requests.',
            'Privacy and cookies',
            [
                'Last updated: October 1, 2026. SignalShelf is an independent editorial website. The static site does not create user accounts and does not operate a server-side visitor database.',
                'The site uses Google Consent Mode. Advertising storage, user data, and personalization signals are set to denied by default. When a visitor is in a region that requires consent, Google-certified consent messaging collects and updates the visitor preference before personalized advertising is used. The site does not use analytics.',
                'SignalShelf is hosted by Vercel. Like most hosting providers, Vercel may process request information such as IP address, user agent, timestamps, and security logs to deliver and protect the service. Vercel privacy information is available at https://vercel.com/legal/privacy-policy.',
                'Google AdSense and its partners may use cookies or similar identifiers to measure and personalize advertising. Google Consent Mode is configured with advertising storage denied by default, and the Google-certified consent message manages choices where required by law. Google partner-site information is available at https://policies.google.com/technologies/partner-sites and advertising controls are available at https://adssettings.google.com/.',
                'External tool links lead to websites controlled by other companies. Those sites have their own privacy policies, cookies, accounts, and data practices. Review the destination policy before submitting personal or confidential information.',
                'Privacy and security requests can be submitted privately through https://github.com/syushengshen-glitch/claire/security/advisories/new. Include the requested action, the relevant page, and a safe way to respond.',
                'We may update this policy when the site adds advertising, analytics, forms, a custom domain, or a new service provider. The updated date at the top of this page will be revised when the policy changes.'
            ], 0, '', base_url, publisher, 'privacy.html'
        ),
        'terms.html': build_simple_page(
            'Terms of use',
            'Terms for using SignalShelf, including informational content, external links, acceptable use, and limitations of liability.',
            'Terms of use',
            [
                'Last updated: October 1, 2026. By using SignalShelf, you agree to these terms. If you do not agree, do not use the site.',
                'SignalShelf provides general information about AI products. Product features, prices, availability, and legal terms can change without notice. Confirm important details directly with the vendor before purchase or commercial use.',
                'The site is provided on an as-is and as-available basis. To the extent permitted by law, SignalShelf does not guarantee uninterrupted availability, completeness, accuracy, or suitability for a particular purpose and is not responsible for decisions made from the information.',
                'You may link to public pages and quote short excerpts with attribution. You may not scrape, republish, misrepresent, or mass-copy the site content, or use the site in a way that violates law, interferes with security, or infringes another person\'s rights.',
                'External links are provided for convenience. SignalShelf does not control third-party websites, products, security, or data practices and does not endorse every statement on a linked site.',
                'Advertising and affiliate relationships, when present, will be labeled and disclosed. Sponsored inventory must not be presented as an independent editorial recommendation.',
                'Questions about these terms can be submitted through the monitored contact channel listed on the Contact page.'
            ], 0, '', base_url, publisher, 'terms.html'
        ),
        'contact.html': build_simple_page(
            'Contact SignalShelf',
            'Monitored contact channels for corrections, privacy requests, partnerships, and editorial feedback.',
            'Contact',
            [
                'For corrections, open a correction request at https://github.com/syushengshen-glitch/claire/issues/new and include the page URL, the sentence you believe is inaccurate, a source, and the date you checked it.',
                'For privacy or security matters, use the private advisory form at https://github.com/syushengshen-glitch/claire/security/advisories/new. Do not post personal, confidential, or account information in a public issue.',
                'For partnerships, state the product, proposed placement, whether the relationship is paid, and the exact disclosure that would appear. Sponsored units must remain labeled and cannot be presented as editorial findings.',
                'General editorial feedback can also be submitted through the same public issue form. Include enough context for the request to be verified without sharing sensitive data.'
            ], 0, '', base_url, publisher, 'contact.html'
        ),
        'disclosure.html': build_simple_page(
            'Affiliate and advertising disclosure',
            'How SignalShelf labels affiliate links, sponsored placements, and advertising.',
            'Affiliate and advertising disclosure',
            [
                'Last updated: October 1, 2026. SignalShelf currently does not have active affiliate links, paid placements, or display advertising on the live site.',
                'If affiliate links are added, the affected page will disclose the relationship before the first affiliate link and the link will use rel="sponsored". Affiliate compensation will not change the stated limitations or editorial conclusion.',
                'If display advertising is enabled, advertising units will be labeled Advertisement and kept visually separate from editorial recommendations. The presence of an ad does not imply that SignalShelf reviewed or endorsed the advertiser.',
                'Paid partnerships must not change evaluation text, category placement, or a tool limitations section. Sponsored inventory will be identified as sponsored in the page copy.',
                'Questions about a commercial relationship can be submitted through the Contact page.'
            ], 0, '', base_url, publisher, 'disclosure.html'
        ),
        'editorial-policy.html': build_simple_page(
            'Editorial policy',
            'The criteria used to include, review, update, and correct tools in the SignalShelf directory.',
            'Editorial policy',
            [
                'Every listing starts with a defined job, audience, pricing note, practical strengths, and material limits. A product is not included merely because it has a large audience or an affiliate program.',
                'Reviews prioritize observable product information and clearly stated criteria. Claims about speed, quality, or cost should be dated and supported by a source, a test, or an explicit editorial judgment. The site does not claim that every tool was purchased or independently benchmarked.',
                'AI assistance may support research, organization, drafting, or coding. A human editor remains responsible for accuracy, usefulness, sources, originality, and the final publication decision. Unedited bulk AI content is not presented as original research.',
                'Corrections are welcome. When a material fact changes, update the page, the review date, and the internal link context rather than silently changing the conclusion. Significant corrections should identify what changed when that information helps readers.',
                'Advertising and commercial relationships are separated from editorial decisions. Products are not ranked higher because of an ad or partnership.'
            ], 0, 'method', base_url, publisher, 'editorial-policy.html'
        )
    }
    for filename, content in pages.items():
        (SITE / filename).write_text(content, encoding='utf-8')


def build_404(publisher):
    body = '''<section class="site-shell page-hero"><h1>That signal dropped.</h1><p>The page may have moved, or the tool may no longer be in the index.</p><p><a class="button" href="index.html">Return home</a></p></section>'''
    output = page('Page not found', 'The requested page could not be found.', body, publisher=publisher)
    output = output.replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"')
    (SITE / '404.html').write_text(output, encoding='utf-8')


def build_manifest():
    manifest = {'name':'SignalShelf','short_name':'SignalShelf','start_url':'/','display':'standalone','background_color':'#edf4f2','theme_color':'#15323b'}
    (SITE / 'site.webmanifest').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    favicon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#15323b"/><circle cx="32" cy="32" r="22" fill="none" stroke="#f1c75b" stroke-width="2"/><path d="M12 32h40M32 12v40" stroke="#edf4f2" stroke-width="2"/><circle cx="32" cy="32" r="6" fill="#f2684a"/></svg>'
    (SITE / 'favicon.svg').write_text(favicon, encoding='utf-8')


def build_seo_files(publisher, base_url):
    clean_base = base_url.rstrip('/')
    paths = ['index.html','directory.html','guides/index.html','about.html','privacy.html','terms.html','contact.html','disclosure.html','editorial-policy.html']
    paths += [f'tools/{tool["slug"]}.html' for tool in TOOLS]
    paths += [f'category/{key}.html' for key in CATEGORIES]
    paths += [f'guides/{guide["slug"]}.html' for guide in GUIDES]
    paths.append('guides/chatgpt-vs-gemini-editorial-plan-test.html')
    paths += [f'guides/{experiment["slug"]}.html' for experiment in EXTRA_EXPERIMENTS]
    rows = '\n'.join(f'  <url><loc>{esc(clean_base + "/" + path)}</loc><lastmod>2026-10-01</lastmod></url>' for path in paths)
    (SITE / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n', encoding='utf-8')
    (SITE / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {clean_base}/sitemap.xml\n', encoding='utf-8')
    if publisher:
        publisher_id = publisher.replace('ca-', '')
        ads = f'google.com, {publisher_id}, DIRECT, f08c47fec0942fa0\n'
    else:
        ads = '# Add your approved AdSense line here, for example:\n# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n'
    (SITE / 'ads.txt').write_text(ads, encoding='utf-8')


def build_article_plan():
    audiences = ['small business owners','freelancers','students','marketers','founders','teachers','developers','designers','writers','remote teams']
    tasks = ['writing','research','coding','image generation','video editing','customer support','sales outreach','project planning','data analysis','social media']
    rows = []
    index = 1
    for audience in audiences:
        for task in tasks:
            keyword = f'best ai tools for {audience} {task}'
            rows.append({'#':index,'priority':'P1' if index <= 30 else ('P2' if index <= 70 else 'P3'),'category':task,'audience':audience,'primary_keyword':keyword,'title':f'Best AI tools for {audience} who need help with {task}','slug':slugify(keyword),'search_intent':'commercial investigation','internal_links':'3 tool reviews + 1 category page','source_check':'Validate demand in Google Keyword Planner or Ahrefs','status':'planned'})
            index += 1
    out = BASE / 'docs' / '02-content-plan.csv'
    with out.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_all(publisher, base_url):
    SITE.mkdir(parents=True, exist_ok=True)
    for folder in ['tools', 'category', 'guides', '.well-known']:
        (SITE / folder).mkdir(parents=True, exist_ok=True)
    (SITE / 'index.html').write_text(build_home(publisher, base_url), encoding='utf-8')
    (SITE / 'directory.html').write_text(build_directory(publisher, base_url), encoding='utf-8')
    for tool in TOOLS:
        (SITE / 'tools' / f'{tool["slug"]}.html').write_text(build_tool_page(tool, publisher, base_url), encoding='utf-8')
    for key, label in CATEGORIES.items():
        (SITE / 'category' / f'{key}.html').write_text(build_category_page(key, label, publisher, base_url), encoding='utf-8')
    (SITE / 'guides' / 'index.html').write_text(build_guides_index(publisher, base_url), encoding='utf-8')
    for guide in GUIDES:
        (SITE / 'guides' / f'{guide["slug"]}.html').write_text(build_guide_page(guide, publisher, base_url), encoding='utf-8')
    (SITE / 'guides' / 'chatgpt-vs-gemini-editorial-plan-test.html').write_text(build_experiment_page(publisher, base_url), encoding='utf-8')
    for experiment in EXTRA_EXPERIMENTS:
        (SITE / 'guides' / f'{experiment["slug"]}.html').write_text(build_extra_experiment_page(experiment, publisher, base_url), encoding='utf-8')
    write_static_pages(publisher, base_url)
    build_404(publisher)
    build_manifest()
    build_seo_files(publisher, base_url)
    (SITE / '.well-known' / 'security.txt').write_text('Contact: https://github.com/syushengshen-glitch/claire/security/advisories/new\nExpires: 2027-10-01T00:00:00Z\nPreferred-Languages: en, zh\nCanonical: https://claire-mu.vercel.app/.well-known/security.txt\n', encoding='utf-8')
    build_article_plan()
    print(f'Built {len(TOOLS)} tool pages, {len(CATEGORIES)} category pages, {len(GUIDES)} guides, and 100 content-plan rows.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build the SignalShelf static site.')
    parser.add_argument('--adsense-publisher', default='', help='AdSense publisher ID, for example ca-pub-0000000000000000')
    parser.add_argument('--base-url', default='https://example.com', help='Canonical production URL')
    args = parser.parse_args()
    build_all(args.adsense_publisher.strip() or None, args.base_url.strip())


