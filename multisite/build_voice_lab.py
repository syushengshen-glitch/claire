from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sites' / 'voice'
SOURCE_ASSETS = ROOT / 'site' / 'assets'
CONTENT = json.loads((ROOT / 'multisite' / 'voice-content.json').read_text(encoding='utf-8'))
PUBLISHER = 'ca-pub-1837836558769995'
TODAY = 'October 28, 2026'
LAST_MODIFIED = '2026-10-28'
BRAND = CONTENT['brand']
BASE_URL = 'https://signalstack-voice-lab.vercel.app'
CATEGORIES = CONTENT['categories']
ARTICLES = CONTENT['articles']


def esc(value):
    return html.escape(str(value), quote=True)


def category_by_slug(slug):
    return next(item for item in CATEGORIES if item['slug'] == slug)


def article_by_slug(slug):
    return next(item for item in ARTICLES if item['slug'] == slug)


def category_articles(slug):
    return [item for item in ARTICLES if item['category'] == slug]


def ad_slot(kind):
    # 保留廣告位；通過 AdSense 審查前只顯示清楚的 Advertisement 標籤。
    return f'<div class="ad-slot ad-{esc(kind)}" role="complementary" aria-label="Advertisement"><span class="ad-label">Advertisement</span><div class="ad-space">Reserved ad space</div></div>'


def header(depth=0, current=''):
    prefix = '../' if depth else ''
    def attr(key):
        return ' aria-current="page"' if current == key else ''
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="site-shell header-inner">
  <a class="brand" href="{prefix}index.html"><span class="brand-mark"><span></span></span><span>{esc(BRAND)}</span></a>
  <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Toggle navigation">Menu</button>
  <nav class="site-nav" data-site-nav>
    <a href="{prefix}categories/index.html"{attr('categories')}>Categories</a>
    <a href="{prefix}guides/index.html"{attr('guides')}>Guides</a>
    <a href="{prefix}tools/index.html"{attr('tools')}>Tools</a>
    <a href="{prefix}editorial-policy.html"{attr('method')}>Method</a>
  </nav>
</div></header>'''


def footer(depth=0):
    prefix = '../' if depth else ''
    return f'''<footer class="site-footer"><div class="site-shell"><div class="footer-grid">
  <div><a class="brand" href="{prefix}index.html"><span class="brand-mark"><span></span></span><span>{esc(BRAND)}</span></a><p>{esc(CONTENT['description'])}</p></div>
  <div><h2>Explore</h2><a href="{prefix}categories/index.html">Categories</a><a href="{prefix}guides/index.html">Guides</a><a href="{prefix}tools/index.html">Tools &amp; templates</a></div>
  <div><h2>Trust</h2><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a><a href="{prefix}privacy.html">Privacy</a><a href="{prefix}terms.html">Terms</a></div>
</div><div class="footer-bottom"><span>&copy; <span data-year>2026</span> {esc(BRAND)}. Independent operations publication.</span><button class="text-button" type="button" data-manage-consent>Privacy choices</button></div></div></footer>'''


def page(title, description, body, depth=0, current='', path=''):
    prefix = '../' if depth else ''
    canonical = f'{BASE_URL}/{path}' if path else BASE_URL + '/'
    schema = {'@context':'https://schema.org','@type':'WebSite','name':BRAND,'url':BASE_URL,'description':CONTENT['description']}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | {esc(BRAND)}</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="{esc(BRAND)} Editorial Team"><link rel="canonical" href="{esc(canonical)}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/styles.css"><link rel="stylesheet" href="{prefix}assets/voice-theme.css">
<script>window.SIGNALSHELF_ADSENSE_CLIENT="{PUBLISHER}";</script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body class="theme-voice">{header(depth, current)}<main id="main">{body}</main>{footer(depth)}<script src="{prefix}assets/app.js" defer></script></body></html>'''


def article_card(article, depth=0):
    prefix = '../' if depth else ''
    category = category_by_slug(article['category'])
    return f'''<article class="article-card"><div><span class="pill">{esc(category['name'])}</span><h3><a href="{prefix}guides/{esc(article['slug'])}.html">{esc(article['title'])}</a></h3><p>{esc(article['dek'])}</p></div><a href="{prefix}guides/{esc(article['slug'])}.html">Read the guide</a></article>'''


def category_card(category, depth=0):
    prefix = '../' if depth else ''
    count = len(category_articles(category['slug']))
    return f'''<article class="article-card category-card"><div><h3><a href="{prefix}categories/{esc(category['slug'])}.html">{esc(category['name'])}</a></h3><p>{esc(category['blurb'])}</p></div><a href="{prefix}categories/{esc(category['slug'])}.html">{count} guides</a></article>'''


def render_article(article):
    category = category_by_slug(article['category'])
    sections = ''.join(f'<h2>{esc(item["h"])}</h2><p>{esc(item["p"])}</p>' for item in article['sections'])
    checklist = ''.join(f'<li>{esc(item)}</li>' for item in article['checklist'])
    mistakes = ''.join(f'<li>{esc(item)}</li>' for item in article['mistakes'])
    faq = ''.join(f'<h3>{esc(item["q"])}</h3><p>{esc(item["a"])}</p>' for item in article['faq'])
    example_lines = ''.join(f'<p>{esc(line)}</p>' for line in article['example']['lines'])
    related = ''.join(f'<li><a href="{esc(article_by_slug(slug)["slug"])}.html">{esc(article_by_slug(slug)["title"])}</a></li>' for slug in article['related'])
    tool = article.get('tool')
    tool_link = f'<p><a class="button" href="../tools/{esc(tool)}.html">Open the related template</a></p>' if tool else ''
    body = f'''<article><header class="site-shell article-header"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {esc(article['title'])}</nav><span class="pill">{esc(category['name'])}</span><h1>{esc(article['title'])}</h1><p class="dek">{esc(article['dek'])}</p><p class="article-meta">Reviewed {TODAY} · Practical operations guide · Advertising is labeled separately</p></header>
<div class="site-shell content-grid"><div class="content-card prose"><div class="callout"><strong>Quick answer:</strong> {esc(article['quick_answer'])}</div><h2>The problem</h2><p>{esc(article['problem'])}</p>{sections}{ad_slot('inline')}<h2>Example</h2><div class="example-box"><h3>{esc(article['example']['title'])}</h3>{example_lines}</div><h2>Checklist</h2><ul class="checklist">{checklist}</ul><h2>Mistakes to avoid</h2><ul>{mistakes}</ul><h2>FAQ</h2>{faq}<h2>Related guides</h2><ul>{related}</ul>{tool_link}<div class="note"><strong>Scope note</strong><p>This is voice-production and rights guidance, not legal advice. Adapt consent, licensing, and disclosure templates to your jurisdiction, contracts, and platform rules.</p></div></div>
<aside class="side-stack"><div class="side-panel"><h2>Category</h2><p><a href="../categories/{esc(category['slug'])}.html">{esc(category['name'])}</a></p><p>{esc(category['blurb'])}</p></div>{ad_slot('rail')}<div class="side-panel compact"><h2>Use the template</h2><p>Open the related tool page to copy or calculate the template described in this guide.</p></div></aside></div></article>'''
    return page(article['title'], article['dek'], body, 1, 'guides', f'guides/{article["slug"]}.html')




RESOURCE_TITLES = {
    'voice-casting-scorecard': 'Voice casting scorecard',
    'voice-audition-builder': 'Voice audition script builder',
    'accent-casting-brief': 'Accent and representation casting brief',
    'narration-pacing-calculator': 'Narration pacing calculator',
    'pronunciation-guide-builder': 'Pronunciation guide builder',
    'voice-script-template': 'Voice production script template',
    'dubbing-vs-subtitles-decision': 'Dubbing vs subtitles decision guide',
    'localization-qc-scorecard': 'Localization QC scorecard',
    'dubbing-cost-estimator': 'Dubbing cost estimator',
    'audio-cleanup-checklist': 'Voice cleanup checklist',
    'loudness-delivery-checklist': 'Loudness delivery checklist',
    'subtitle-cps-calculator': 'Subtitle reading-speed calculator',
    'voice-cloning-consent-builder': 'Voice cloning consent builder',
    'synthetic-voice-disclosure-builder': 'Synthetic voice disclosure builder',
    'licensed-audio-checklist': 'Licensed audio checklist'
}
INTERACTIVE = {'voice-casting-scorecard','narration-pacing-calculator','dubbing-cost-estimator','subtitle-cps-calculator','voice-cloning-consent-builder','synthetic-voice-disclosure-builder'}
TOOL_ORDER = sorted(RESOURCE_TITLES.keys())


def tool_link_article(slug):
    return next((item for item in ARTICLES if item.get('tool') == slug), ARTICLES[0])


def render_tool(slug):
    article = tool_link_article(slug)
    category = category_by_slug(article['category'])
    title = RESOURCE_TITLES[slug]
    interactive_forms = {
        'voice-casting-scorecard': '''<form class="tool-form" data-casting-form><div class="field-grid"><label>Clarity (0-5)<input type="range" min="0" max="5" value="3" data-casting-clarity></label><label>Emotional fit (0-5)<input type="range" min="0" max="5" value="3" data-casting-emotion></label><label>Accent and language fit (0-5)<input type="range" min="0" max="5" value="3" data-casting-accent></label><label>Pronunciation accuracy (0-5)<input type="range" min="0" max="5" value="3" data-casting-pronunciation></label><label>Editability and consistency (0-5)<input type="range" min="0" max="5" value="3" data-casting-editability></label></div><button class="button" type="submit">Score this voice</button></form><div class="calculator-result" data-casting-result aria-live="polite"><p>Move the sliders and score the voice.</p></div>''',
        'narration-pacing-calculator': '''<form class="tool-form" data-pacing-form><div class="field-grid"><label>Word count<input type="number" min="0" value="340" data-pacing-words></label><label>Words per minute<input type="number" min="60" value="145" data-pacing-wpm></label><label>Number of sections<input type="number" min="0" value="4" data-pacing-sections></label><label>Average pause per section (seconds)<input type="number" min="0" step="0.1" value="2" data-pacing-pause></label></div><button class="button" type="submit">Estimate runtime</button></form><div class="calculator-result" data-pacing-result aria-live="polite"><p>Enter the script details to estimate runtime.</p></div>''',
        'dubbing-cost-estimator': '''<form class="tool-form" data-dubbing-form><div class="field-grid"><label>Approved runtime (minutes)<input type="number" min="0" value="18" data-dubbing-minutes></label><label>Number of languages<input type="number" min="1" value="3" data-dubbing-languages></label><label>Dubbing rate per minute<input type="number" min="0" value="35" data-dubbing-rate></label><label>Adaptation and QC buffer %<input type="number" min="0" value="35" data-dubbing-buffer></label></div><button class="button" type="submit">Estimate budget</button></form><div class="calculator-result" data-dubbing-result aria-live="polite"><p>Enter the runtime and rate to estimate the budget.</p></div>''',
        'subtitle-cps-calculator': '''<form class="tool-form" data-cps-form><div class="field-grid"><label>Characters in the caption<input type="number" min="0" value="84" data-cps-characters></label><label>Caption duration (seconds)<input type="number" min="0" step="0.1" value="4.5" data-cps-duration></label></div><button class="button" type="submit">Calculate reading speed</button></form><div class="calculator-result" data-cps-result aria-live="polite"><p>Enter caption length and timing.</p></div>''',
        'voice-cloning-consent-builder': '''<form class="tool-form" data-consent-form><div class="field-grid"><label>Voice owner<input type="text" value="Alex Chen" data-consent-owner></label><label>Project or brand<input type="text" value="Internal training videos" data-consent-project></label><label>Permitted uses<textarea rows="2" data-consent-permitted>Internal training videos; approved social clips</textarea></label><label>Excluded uses<textarea rows="2" data-consent-excluded>Political, adult, medical, financial, endorsements</textarea></label><label>Territory<input type="text" value="Taiwan" data-consent-territory></label><label>Duration<input type="text" value="12 months" data-consent-duration></label><label>Review date<input type="text" value="2027-10-28" data-consent-review></label></div><button class="button" type="submit">Build consent draft</button></form><div class="calculator-result" data-consent-result aria-live="polite"><p>Fill the fields to generate a consent draft.</p></div>''',
        'synthetic-voice-disclosure-builder': '''<form class="tool-form" data-disclosure-form><div class="field-grid"><label>Content type<input type="text" value="Product explainer video" data-disclosure-content></label><label>Voice type<select data-disclosure-type><option value="synthetic">Synthetic voice</option><option value="cloned">Cloned human voice</option><option value="mixed">Mixed human and synthetic</option></select></label><label>Placement<select data-disclosure-placement><option value="start">Start of audio</option><option value="end">End of audio</option><option value="both">Start and end</option><option value="visual">On-screen label only</option></select></label></div><button class="button" type="submit">Build disclosure</button></form><div class="calculator-result" data-disclosure-result aria-live="polite"><p>Fill the fields to generate a disclosure.</p></div>'''
    }
    form = interactive_forms.get(slug, '')
    interactive = slug in INTERACTIVE
    resource_intro = f'This template supports the guide <a href="../guides/{esc(article["slug"])}.html">{esc(article["title"])}</a>. Use it as a working draft, then adapt the wording and fields to your own contracts, client process, and jurisdiction.'
    fields = ''.join(f'<li>{esc(item)}</li>' for item in article['checklist'])
    mistakes = ''.join(f'<li>{esc(item)}</li>' for item in article['mistakes'])
    example_lines = ''.join(f'<p>{esc(line)}</p>' for line in article['example']['lines'])
    body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Tools</a> / {esc(title)}</nav><span class="pill">{esc(category['name'])}</span><h1>{esc(title)}</h1><p>{esc(article['dek'])}</p></section>
<section class="site-shell section" style="padding-top:0"><div class="content-grid"><article class="content-card prose"><p>{resource_intro}</p>{ad_slot('inline')}{form}<h2>How to use this page</h2><ol><li>Open the source guide and read the context first.</li><li>Copy the template or run the calculator with one real, non-sensitive example.</li><li>Check the output against the checklist below.</li><li>Save the final version in your own document or project tool.</li></ol><h2>Checklist</h2><ul class="checklist">{fields}</ul><h2>Example wording</h2><div class="example-box"><h3>{esc(article['example']['title'])}</h3>{example_lines}</div><h2>Do not skip</h2><ul>{mistakes}</ul><div class="note"><strong>Scope note</strong><p>This page is a production and rights template, not legal advice. Review consent, licensing, and disclosure wording with a qualified professional where the risk is material.</p></div></article><aside class="side-stack"><div class="side-panel"><h2>Related guide</h2><p><a href="../guides/{esc(article['slug'])}.html">{esc(article['title'])}</a></p></div>{ad_slot('rail')}<div class="side-panel compact"><h2>Copy only what you need</h2><p>The templates are starting points. Remove fields that do not match your process.</p></div></aside></div></section><script src="../assets/voice-tools.js" defer></script>'''
    return page(title, article['dek'], body, 1, 'tools', f'tools/{slug}.html')


def build_home():
    featured = ARTICLES[:6]
    cards = ''.join(article_card(item) for item in featured)
    category_cards = ''.join(category_card(item) for item in CATEGORIES)
    tool_cards = ''.join(f'<article class="article-card"><h3><a href="tools/{esc(slug)}.html">{esc(RESOURCE_TITLES[slug])}</a></h3><p>{esc(tool_link_article(slug)["dek"])}</p></article>' for slug in TOOL_ORDER[:6])
    body = f'''<section class="site-shell hero"><div class="hero-copy"><span class="hero-note">Original voice and audio research</span><h1>Make voice work sound credible, clear, and properly licensed.</h1><p class="hero-intro">VoiceSignal Lab publishes original guides, templates, and calculators for voice casting, narration, dubbing, audio cleanup, and consent.</p><p><a class="button" href="guides/index.html">Start with the guides</a> <a class="button secondary" href="tools/index.html">Open the tools</a></p></div><div class="radar"><div class="radar-center">15<br>guides</div><span class="radar-node n1">Casting</span><span class="radar-node n2">Narration</span><span class="radar-node n3">Dubbing</span><span class="radar-node n4">Audio</span><span class="radar-node n5">Rights</span><p class="radar-caption">Every guide points to a usable template or calculator.</p></div></section>
<div class="site-shell signal-strip"><span><strong>15</strong> original guides</span><span><strong>15</strong> templates and calculators</span><span><strong>5</strong> voice-workflow categories</span><span>Reviewed <strong>{TODAY}</strong></span></div>
<section class="site-shell section"><div class="section-heading"><h2>Start with a category</h2><p>Choose the voice or audio problem that needs a defensible workflow.</p></div><div class="article-grid">{category_cards}</div></section>
<section class="site-shell section"><div class="section-heading"><h2>Featured guides</h2><p>Specific methods, documented limits, and a usable template for each job.</p></div><div class="article-grid">{cards}</div></section>
{ad_slot('wide')}
<section class="site-shell section"><div class="section-heading"><h2>Tools and templates</h2><p>Casting, pacing, dubbing, cleanup, consent, and disclosure tools you can use on a real project.</p></div><div class="article-grid">{tool_cards}</div></section>'''
    return page('Practical voice, narration, dubbing, and audio workflow research', CONTENT['description'], body, 0, '', 'index.html')


def build_categories_index():
    cards = ''.join(category_card(item, 1) for item in CATEGORIES)
    body = f'<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Categories</nav><h1>Five voice-workflow categories.</h1><p>Every category solves a recurring voice or audio problem with original guides and templates.</p></section><section class="site-shell section" style="padding-top:0"><div class="article-grid">{cards}</div>{ad_slot("wide")}</section>'
    return page('Categories', 'Browse VoiceSignal Lab guides by casting, narration, dubbing, audio editing, and consent.', body, 1, 'categories', 'categories/index.html')


def build_category_page(category):
    items = category_articles(category['slug'])
    cards = ''.join(article_card(item, 1) for item in items)
    body = f'<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Categories</a> / {esc(category["name"])}</nav><h1>{esc(category["name"])}</h1><p>{esc(category["blurb"])}</p></section><section class="site-shell section" style="padding-top:0"><div class="article-grid">{cards}</div>{ad_slot("wide")}</section>'
    return page(category['name'], category['blurb'], body, 1, 'categories', f'categories/{category["slug"]}.html')


def build_guides_index():
    cards = ''.join(article_card(item, 1) for item in ARTICLES)
    body = f'<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Guides</nav><h1>Fifteen guides for voice work that has to survive the edit.</h1><p>Casting, narration, dubbing, audio cleanup, and consent, in the order most voice projects need them.</p></section><section class="site-shell section" style="padding-top:0">{ad_slot("wide")}<div class="article-grid">{cards}</div></section>'
    return page('Voice and audio guides', 'Fifteen practical guides for voice casting, narration, dubbing, audio editing, and rights.', body, 1, 'guides', 'guides/index.html')


def build_tools_index():
    cards = ''.join(f'<article class="article-card"><h3><a href="{esc(slug)}.html">{esc(RESOURCE_TITLES[slug])}</a></h3><p>{esc(tool_link_article(slug)["dek"])}</p><p class="article-meta">{"Interactive calculator" if slug in INTERACTIVE else "Copy-ready template"}</p></article>' for slug in TOOL_ORDER)
    body = f'<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> / Tools</nav><h1>Voice and audio tools.</h1><p>Use one real, non-sensitive example. Interactive pages run in your browser and do not send your inputs anywhere.</p></section><section class="site-shell section" style="padding-top:0">{ad_slot("wide")}<div class="article-grid">{cards}</div></section>'
    return page('Voice and audio tools', 'Casting, pacing, dubbing, consent, and subtitle calculators and templates.', body, 1, 'tools', 'tools/index.html')


def build_legal_pages():
    pages = {
        'about.html': ('About VoiceSignal Lab', 'An independent publication about voice selection, narration, dubbing, audio cleanup, and synthetic-media rights.', [
            'VoiceSignal Lab publishes practical guides, templates, and calculators for producers, marketers, educators, and creators. The site focuses on voice casting, narration preparation, dubbing and localization, audio cleanup, and the consent and disclosure rules around synthetic speech.',
            'Every guide states the problem, gives a step-by-step method, includes an example, and links to a usable template or calculator. Legal and platform details are general information, not advice for a specific situation.',
            'AI tools may support research, organization, or drafting. The final page is reviewed for usefulness, structure, links, and clarity. We do not claim that every voice or localization workflow has been tested in every jurisdiction or platform.',
            'Corrections and source-backed feedback are welcome through the contact page. Synthetic voice rights and platform disclosure rules should be verified before publication.'
        ]),
        'contact.html': ('Contact VoiceSignal Lab', 'Use these channels for corrections, privacy requests, and editorial feedback.', [
            'Corrections: use the public issue form at https://github.com/syushengshen-glitch/claire/issues/new. Include the page URL and the source that supports the correction.',
            'Privacy and security: use https://github.com/syushengshen-glitch/claire/security/advisories/new. Do not post personal or confidential information publicly.',
            'Advertising and partnership questions: use the same public issue form and state the product, placement, and whether the relationship is paid. Sponsored content must be labeled.'
        ]),
        'privacy.html': ('Privacy and cookies', 'How this site handles hosting data, advertising consent, and external links.', [
            'Last updated: October 28, 2026. This is a static publication with no user accounts and no server-side visitor database.',
            'The site uses Google Consent Mode. Advertising storage, user data, and personalization are set to denied by default. Google-certified consent messaging manages choices where required by law.',
            'VoiceSignal Lab is hosted by Vercel, which may process request information such as IP address, user agent, timestamps, and security logs to deliver and protect the service.',
            'Google AdSense and its partners may use cookies or similar identifiers after consent or under an applicable legal basis. Partner-site information is available at https://policies.google.com/technologies/partner-sites.',
            'The interactive tools run in your browser. Voice, project, consent, and audio values you enter are not stored or transmitted by this site.',
            'External links lead to websites controlled by other companies with their own privacy policies. Review the destination before submitting personal information.'
        ]),
        'terms.html': ('Terms of use', 'Terms for using VoiceSignal Lab, including information limits and acceptable use.', [
            'Last updated: October 28, 2026. By using this site, you agree to these terms.',
            'The site provides general voice-production and rights information. It is not legal advice. Consent, licensing, and disclosure templates must be adapted to your jurisdiction, contracts, and platform rules.',
            'The site is provided on an as-is and as-available basis. We do not guarantee completeness, accuracy, or suitability for a particular purpose.',
            'You may link to public pages and quote short excerpts with attribution. You may not scrape, republish, or misrepresent the content.',
            'External links are provided for convenience. We do not control third-party products, security, or data practices.'
        ]),
        'disclosure.html': ('Advertising disclosure', 'How advertising and commercial relationships are labeled.', [
            'Last updated: October 28, 2026. Advertising units are labeled Advertisement and kept separate from editorial recommendations.',
            'The site is configured for Google AdSense Auto Ads. Advertising is controlled by Google account approval and may not appear on every page or in every region.',
            'Affiliate links, if added, will be disclosed before the first link and marked rel="sponsored". A commercial relationship will not change a template, warning, or editorial conclusion.',
            'Sponsored inventory must be identified as sponsored and cannot be presented as an independent editorial finding.'
        ]),
        'editorial-policy.html': ('Editorial policy', 'How guides, templates, calculators, and corrections are produced.', [
            'Every guide starts with a specific voice or audio problem, a target reader, a quick answer, a step-by-step method, an example, a checklist, common mistakes, and a related tool.',
            'Calculators use formulas that are explained on the page. They are decision aids, not guarantees. Users must replace the default numbers with their own real assumptions.',
            'AI assistance may support research, organization, or drafting. A human editor remains responsible for accuracy, usefulness, originality, links, and the final publication decision.',
            'Corrections update the page and the review date. A source-backed correction path is available on the contact page.',
            'Advertising is separated from editorial decisions. No advertiser receives a better placement, a softer warning, or a changed conclusion.'
        ])
    }
    outputs = {}
    for filename, (title, description, paragraphs) in pages.items():
        current = 'method' if filename == 'editorial-policy.html' else ''
        body = f'<section class="site-shell page-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / {esc(title)}</nav><h1>{esc(title)}</h1><p>{esc(description)}</p></section><section class="site-shell section" style="padding-top:0"><div class="content-grid"><article class="content-card prose">{"".join(f"<p>{esc(p)}</p>" for p in paragraphs)}</article>{ad_slot("rail")}</div></section>'
        outputs[filename] = page(title, description, body, 0, current, filename)
    return outputs


def build_all():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    for folder in ['assets','categories','guides','tools']:
        (OUT / folder).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_ASSETS / 'styles.css', OUT / 'assets' / 'styles.css')
    shutil.copyfile(SOURCE_ASSETS / 'app.js', OUT / 'assets' / 'app.js')
    (OUT / 'assets' / 'voice-theme.css').write_text((ROOT / 'multisite' / 'themes' / 'voice.css').read_text(encoding='utf-8'), encoding='utf-8')
    (OUT / 'assets' / 'voice-tools.js').write_text((ROOT / 'multisite' / 'themes' / 'voice-tools.js').read_text(encoding='utf-8'), encoding='utf-8')
    (OUT / 'index.html').write_text(build_home(), encoding='utf-8')
    (OUT / 'categories' / 'index.html').write_text(build_categories_index(), encoding='utf-8')
    for category in CATEGORIES:
        (OUT / 'categories' / f'{category["slug"]}.html').write_text(build_category_page(category), encoding='utf-8')
    (OUT / 'guides' / 'index.html').write_text(build_guides_index(), encoding='utf-8')
    for article in ARTICLES:
        (OUT / 'guides' / f'{article["slug"]}.html').write_text(render_article(article), encoding='utf-8')
    (OUT / 'tools' / 'index.html').write_text(build_tools_index(), encoding='utf-8')
    for slug in TOOL_ORDER:
        (OUT / 'tools' / f'{slug}.html').write_text(render_tool(slug), encoding='utf-8')
    for filename, content in build_legal_pages().items():
        (OUT / filename).write_text(content, encoding='utf-8')
    (OUT / '404.html').write_text(page('Page not found', 'The requested page could not be found.', '<section class="site-shell page-hero"><h1>Page not found</h1><p><a class="button" href="index.html">Return home</a></p></section>', 0, '', '404.html'), encoding='utf-8')
    (OUT / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#26124d"/><path d="M18 42V20h10c7 0 11 3 11 9 0 4-2 7-6 8l7 5h-8l-6-5h-2v5h-6zm6-10h4c3 0 5-1 5-3s-2-3-5-3h-4v6z" fill="#55d6be"/></svg>', encoding='utf-8')
    (OUT / 'site.webmanifest').write_text(json.dumps({'name':BRAND,'short_name':BRAND,'start_url':'/','display':'standalone','background_color':'#f7f5ff','theme_color':'#26124d'}, indent=2), encoding='utf-8')
    (OUT / 'ads.txt').write_text('google.com, pub-1837836558769995, DIRECT, f08c47fec0942fa0\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n', encoding='utf-8')
    (OUT / 'vercel.json').write_text(json.dumps({'cleanUrls':True,'trailingSlash':False,'headers':[{'source':'/(.*)','headers':[{'key':'X-Content-Type-Options','value':'nosniff'},{'key':'Referrer-Policy','value':'strict-origin-when-cross-origin'}]}]}, indent=2), encoding='utf-8')
    paths = ['index.html','categories/index.html','guides/index.html','tools/index.html','about.html','contact.html','privacy.html','terms.html','disclosure.html','editorial-policy.html']
    paths += [f'categories/{item["slug"]}.html' for item in CATEGORIES]
    paths += [f'guides/{item["slug"]}.html' for item in ARTICLES]
    paths += [f'tools/{slug}.html' for slug in TOOL_ORDER]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{esc(BASE_URL + "/" + path)}</loc><lastmod>{LAST_MODIFIED}</lastmod></url>' for path in paths) + '</urlset>'
    (OUT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(json.dumps({'site':BRAND,'pages':len(paths),'articles':len(ARTICLES),'tools':len(TOOL_ORDER),'categories':len(CATEGORIES)}, indent=2))


if __name__ == '__main__':
    build_all()
