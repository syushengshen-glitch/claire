from __future__ import annotations

import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'multisite' / 'build_multisite.py'
spec = importlib.util.spec_from_file_location('build_multisite', MODULE_PATH)
bm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bm)
OUT_ROOT = ROOT / 'sites'
THEME_ROOT = ROOT / 'multisite' / 'themes'

import sys
sys.path.insert(0, str(ROOT / 'multisite'))
import career_content as content

SITE = next(item for item in bm.SITES if item['slug'] == 'career')
OUT = OUT_ROOT / 'career'
BASE_URL = bm.base_url(SITE)
REVIEWED = content.REVIEWED

TOOL_AT_A_GLANCE = {
    'rezi': {'price': 'Free plan; Pro $29/month; $149 lifetime option', 'best': 'Guided resume creation and keyword targeting', 'guide': 'best-ai-resume-builders'},
    'teal': {'price': 'Free Forever; Teal+ $13/week', 'best': 'Resume versions plus job tracking', 'guide': 'rezi-vs-teal'},
    'chatgpt': {'price': 'Free and paid plans; Plus listed at $20/month', 'best': 'Critique, rewriting and interview practice', 'guide': 'how-to-use-chatgpt-for-interview-practice'},
    'claude': {'price': 'Free plan; Pro $20/month billed monthly', 'best': 'Long-document review and narrative editing', 'guide': 'ai-resume-tailoring-without-fake-experience'},
    'grammarly': {'price': 'Free and paid individual plans', 'best': 'Grammar, clarity and consistency at the end', 'guide': 'ats-resume-checklist'},
}


def schema_website():
    return {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE['brand'], 'url': BASE_URL, 'description': SITE['description'], 'sameAs': 'https://github.com/syushengshen-glitch'}


def page(title, description, body, depth=0, path='index.html', schema=None, indexable=True):
    prefix = '../' if depth else ''
    canonical = BASE_URL + '/' if path == 'index.html' else f"{BASE_URL}/{path}"
    schema = schema or schema_website()
    robots = 'index,follow,max-image-preview:large' if indexable else 'noindex,nofollow'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{bm.esc(title)} | {bm.esc(SITE['brand'])}</title><meta name="description" content="{bm.esc(description)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{bm.esc(canonical)}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/styles.css"><style>:root{{--blue:{SITE['accent']};--coral:{SITE['accent2']};}}</style><script>window.SIGNALSHELF_ADSENSE_CLIENT="{bm.PUBLISHER}";</script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body class="theme-{SITE['slug']}">{bm.header(SITE, depth)}<main id="main">{body}</main>{bm.footer(SITE, depth)}<script src="{prefix}assets/app.js" defer></script></body></html>'''


def article_schema(meta, slug):
    return {'@context': 'https://schema.org', '@type': 'Article', 'headline': meta['title'], 'description': meta['description'], 'datePublished': '2026-11-13', 'dateModified': '2026-11-13', 'author': {'@type': 'Organization', 'name': content.AUTHOR}, 'publisher': {'@type': 'Organization', 'name': SITE['brand'], 'url': BASE_URL}, 'mainEntityOfPage': f"{BASE_URL}/guides/{slug}.html"}


def review_schema(meta, slug):
    return {'@context': 'https://schema.org', '@type': 'Review', 'name': meta['title'], 'description': meta['description'], 'datePublished': '2026-11-13', 'dateModified': '2026-11-13', 'author': {'@type': 'Organization', 'name': content.AUTHOR}, 'itemReviewed': {'@type': 'SoftwareApplication', 'name': bm.get_tool(slug)['name'], 'applicationCategory': 'BusinessApplication', 'url': bm.get_tool(slug)['url']}}


def toc_for(body_html):
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    if not headings:
        return ''
    links = ''.join(f'<li><a href="#{bm.esc(anchor)}">{bm.esc(re.sub(r"<[^>]+>", "", label))}</a></li>' for anchor, label in headings)
    return f'<div class="side-panel compact"><h2>On this page</h2><ol>{links}</ol></div>'


def render_article(slug, meta, body_html):
    toc = toc_for(body_html)
    body = f'''<article><header class="site-shell article-header"><nav class="breadcrumbs"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {bm.esc(meta['title'])}</nav><h1>{bm.esc(meta['title'])}</h1><p class="dek">{bm.esc(meta['dek'])}</p><p class="article-meta">By {bm.esc(meta['author'])} · Reviewed {bm.esc(meta['reviewed'])} · {bm.esc(meta['reading_time'])} · Advertising is labeled separately</p></header><div class="site-shell content-grid"><div class="content-card prose">{body_html}<div class="callout"><strong>Editorial note.</strong> This page uses official product information and a documented review method. It is not a paid endorsement or a guarantee of interviews, ATS compatibility or product performance.</div><p><a href="../editorial-policy.html">Read our editorial method</a> or <a href="../contact.html">report a correction</a>.</p></div><aside class="side-stack">{toc}<div class="side-panel"><h2>Review standard</h2><p>We separate documented features from editorial judgment, date the pricing checks and avoid claims that cannot be verified.</p><a href="../editorial-policy.html">How we review</a></div></aside></div></article>'''
    return page(meta['title'], meta['description'], body, 1, f"guides/{slug}.html", article_schema(meta, slug))


def render_tool(slug, meta, body_html):
    tool = bm.get_tool(slug)
    facts = TOOL_AT_A_GLANCE[slug]
    related = content.ARTICLE_META[facts['guide']]
    body = f'''<article><header class="site-shell article-header"><nav class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../directory.html">Directory</a> / {bm.esc(tool['name'])}</nav><h1>{bm.esc(meta['title'])}</h1><p class="dek">{bm.esc(meta['dek'])}</p><p class="article-meta">By {bm.esc(meta['author'])} · Reviewed {bm.esc(meta['reviewed'])} · {bm.esc(meta['reading_time'])}</p></header><div class="site-shell content-grid"><div class="content-card prose">{body_html}<div class="callout"><strong>Editorial note.</strong> This review describes publicly documented features and clearly labels limits. Confirm current pricing and plan terms with the vendor before purchasing.</div></div><aside class="side-stack"><div class="side-panel"><h2>At a glance</h2><p><strong>Best for:</strong> {bm.esc(facts['best'])}</p><p><strong>Price checked:</strong> {bm.esc(facts['price'])}</p><p><strong>Reviewed:</strong> {bm.esc(meta['reviewed'])}</p><a class="button" href="{bm.esc(tool['url'])}" target="_blank" rel="noopener">Open official site</a></div><div class="side-panel compact"><h2>Related guide</h2><p><a href="../guides/{bm.esc(facts['guide'])}.html">{bm.esc(related['title'])}</a></p></div><div class="side-panel"><h2>Correction policy</h2><p>Pricing and features change. Report an error through the public contact page and include the URL and source.</p><a href="../contact.html">Contact the editor</a></div></aside></div></article>'''
    return page(meta['title'], meta['description'], body, 1, f"tools/{slug}.html", review_schema(meta, slug))


def article_card(slug, prefix=''):
    meta = content.ARTICLE_META[slug]
    return f'''<article class="article-card"><p class="article-meta">{bm.esc(meta['cluster'])}</p><h3><a href="{prefix}guides/{bm.esc(slug)}.html">{bm.esc(meta['title'])}</a></h3><p>{bm.esc(meta['dek'])}</p><a href="{prefix}guides/{bm.esc(slug)}.html">Read the guide</a></article>'''


def build_home():
    featured = ['best-ai-resume-builders', 'rezi-vs-teal', 'ai-resume-tailoring-without-fake-experience']
    cards = ''.join(article_card(slug) for slug in featured)
    tool_rows = ''.join(bm.tool_row(SITE, bm.get_tool(slug)) for slug in SITE['tools'])
    body = f'''<section class="site-shell hero"><div class="hero-copy"><span class="hero-note">Evidence-first career tools and workflows</span><h1>Make AI improve your application, not invent it.</h1><p class="hero-intro">Practical reviews and job-search guides for students, career changers and job seekers. We focus on what a tool can actually help you finish, what it costs, where it fails and what still needs human review.</p><div class="tool-actions"><a class="button" href="guides/best-ai-resume-builders.html">Start with resume tools</a><a class="button secondary" href="directory.html">Compare the directory</a></div></div><div class="radar"><div class="radar-center">5 tools<br>6 guides</div><span class="radar-node n1">Resume tailoring</span><span class="radar-node n2">ATS checks</span><span class="radar-node n3">Interview practice</span><span class="radar-node n4">Privacy</span><span class="radar-node n5">Human review</span></div></section><section class="site-shell section"><div class="section-heading"><h2>Start with a real job-search problem</h2><p>Two or three focused guides are more useful than fifty versions of the same advice.</p></div><div class="article-grid">{cards}</div></section><section class="site-shell section"><div class="section-heading"><h2>Compare the five core tools</h2><p>Each review states the best-fit workflow, verified pricing information and the limits that matter before you subscribe.</p></div><div class="tool-list">{tool_rows}</div></section><section class="site-shell section"><div class="section-heading"><h2>What makes a useful review here</h2><p>We prioritize evidence and decision quality over feature volume.</p></div><div class="article-grid"><article class="article-card"><p class="article-meta">Evidence</p><h3>Official sources first</h3><p>Product claims are checked against the vendor's current site. We date pricing checks and link to the source used.</p></article><article class="article-card"><p class="article-meta">Limits</p><h3>Tradeoffs stay visible</h3><p>No tool is presented as a guaranteed interview machine. We explain where each product stops helping.</p></article><article class="article-card"><p class="article-meta">Human review</p><h3>You own the facts</h3><p>AI may improve the wording. It cannot supply experience, metrics or credentials you do not have.</p></article></div></section>'''
    return page('AI resume and job-search tools', SITE['description'], body)


def build_guides_index():
    cards = ''.join(article_card(slug, '../') for slug in content.ARTICLE_META)
    body = f'''<section class="site-shell page-hero"><h1>Six practical guides for a better job search</h1><p>Resume strategy, ATS checks, responsible AI use, interview practice and privacy.</p></section><section class="site-shell section"><div class="article-grid">{cards}</div></section><section class="site-shell section"><div class="content-card prose"><h2>How to use this library</h2><p>Start with the problem you need to solve, not with the tool you have heard about. If you are unsure where to begin, read the resume-builder comparison first, then use the ATS checklist to review the exported document.</p><p>All guides are reviewed on the same date and linked to the official sources used. We remove or consolidate pages when they no longer add a distinct answer.</p></div></section>'''
    return page('Career guides', 'Practical guides for AI-assisted resumes, ATS checks, interview practice, responsible tailoring and job-search privacy.', body, 1, 'guides/index.html', {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'CareerSignal Lab guides', 'url': f'{BASE_URL}/guides/index.html'})


def build_directory():
    rows = ''.join(bm.tool_row(SITE, bm.get_tool(slug)) for slug in SITE['tools'])
    table_rows = ''.join(f'''<tr><td><a href="tools/{slug}.html">{bm.esc(bm.get_tool(slug)['name'])}</a></td><td>{bm.esc(TOOL_AT_A_GLANCE[slug]['best'])}</td><td>{bm.esc(TOOL_AT_A_GLANCE[slug]['price'])}</td></tr>''' for slug in SITE['tools'])
    body = f'''<section class="site-shell page-hero"><h1>AI resume and job-search tools directory</h1><p>Five focused tools, compared by the workflow they improve and the limits you should verify.</p></section><section class="site-shell section"><div class="content-card prose"><h2>Quick comparison</h2><div class="table-wrap"><table><thead><tr><th>Tool</th><th>Best fit</th><th>Price checked November 13, 2026</th></tr></thead><tbody>{table_rows}</tbody></table></div><p>These are not rankings based on a single universal score. A resume builder can be the right choice for one applicant and unnecessary for another who already has a strong document. Choose the workflow that reduces correction work without hiding the evidence.</p></div></section><section class="site-shell section"><div class="tool-list">{rows}</div></section>'''
    return page('AI resume and job-search tools directory', 'Compare Rezi, Teal, ChatGPT, Claude and Grammarly by workflow, pricing, limits and best fit.', body, 0, 'directory.html', {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'CareerSignal Lab directory', 'url': f'{BASE_URL}/directory.html'})


def build_about():
    body = f'''<section class="site-shell page-hero"><h1>About CareerSignal Lab</h1><p>Practical, evidence-first guidance for using AI in a job search.</p></section><section class="site-shell section"><div class="content-card prose"><h2>Why this site exists</h2><p>CareerSignal Lab covers AI resume builders, job trackers, writing assistants and interview workflows for students, career changers and job seekers. The site is built around a simple rule: a tool should help you express real evidence more clearly, not manufacture a more impressive history.</p><h2>Who maintains it</h2><p>The site is maintained by an independent editorial project publishing under the CareerSignal Lab name. The public maintainer profile is available at <a href="https://github.com/syushengshen-glitch" target="_blank" rel="noopener">github.com/syushengshen-glitch</a>. We do not claim an employer relationship with any reviewed vendor, and we do not present a product as tested unless the page says what was tested and when.</p><h2>How reviews are made</h2><p>Reviews combine current official product information, documented pricing, clearly separated editorial judgment and a repeatable decision framework. We date price checks, link to sources, state limitations and avoid universal claims about ATS performance or interview outcomes.</p><h2>Corrections and contact</h2><p>Corrections are handled through the public issue tracker linked on the <a href="contact.html">contact page</a>. A useful correction includes the URL, the disputed sentence, the correct information and a current source.</p><h2>Advertising</h2><p>Advertising and editorial recommendations are kept separate. See the <a href="disclosure.html">advertising disclosure</a> for current commercial relationships and labeling rules.</p></div></section>'''
    return page('About CareerSignal Lab', 'How CareerSignal Lab researches, reviews and corrects career tools and workflows.', body, 0, 'about.html', {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About CareerSignal Lab', 'url': f'{BASE_URL}/about.html'})


def build_editorial():
    body = f'''<section class="site-shell page-hero"><h1>Editorial method</h1><p>How we decide what to publish, what to verify and what to remove.</p></section><section class="site-shell section"><div class="content-card prose"><h2>1. Start with a real decision</h2><p>A page should help a reader choose a workflow, check a resume, prepare for an interview or reduce a privacy risk. Pages that exist only to repeat a keyword or link to a vendor are not published.</p><h2>2. Use primary sources</h2><p>Product features, plan limits and prices are checked against the vendor's official pages. We link to the source and record the review date. When a feature cannot be verified, we describe it as a limit to verify rather than filling the gap with a guess.</p><h2>3. Separate evidence from judgment</h2><p>Documented product behavior is evidence. Advice about who should use the product is editorial judgment. We try to make the distinction obvious so readers can evaluate both.</p><h2>4. Keep the human review step</h2><p>AI tools may help with outlining, comparison or copy editing. They do not create experience. Every factual claim in a resume, interview answer or review must be traceable to a source or a real user-provided example.</p><h2>5. Review dates and corrections</h2><p>Pricing is checked when a page is reviewed and may change after publication. Corrections update the page and review date. Pages that no longer add a distinct answer are consolidated, removed or redirected instead of being kept as thin variants.</p><h2>6. Commercial independence</h2><p>Advertising is labeled. Affiliate relationships, if added, will be disclosed before the first affected link and will not determine the stated strengths or limitations of a tool. See the <a href="disclosure.html">advertising disclosure</a>.</p><h2>7. Privacy and sensitive data</h2><p>Guides that mention uploading resumes or interview material explain redaction and vendor-review steps. We do not ask readers to submit confidential employer information or another person's personal data.</p></div></section>'''
    return page('Editorial method', 'CareerSignal Lab editorial standards, source policy, AI disclosure, correction process and commercial independence.', body, 0, 'editorial-policy.html', {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Editorial method', 'url': f'{BASE_URL}/editorial-policy.html'})


def build_contact():
    body = f'''<section class="site-shell page-hero"><h1>Contact and corrections</h1><p>Use the public issue tracker for factual corrections, broken links and privacy requests.</p></section><section class="site-shell section"><div class="content-card prose"><h2>Corrections</h2><p>Open a public issue at <a href="https://github.com/syushengshen-glitch/claire/issues/new" target="_blank" rel="noopener">github.com/syushengshen-glitch/claire/issues/new</a>. Include the page URL, the sentence that needs correction and a current source. Do not include passwords, private candidate information or confidential employer records.</p><h2>Privacy and security</h2><p>For a privacy or security report, use <a href="https://github.com/syushengshen-glitch/claire/security/advisories/new" target="_blank" rel="noopener">the security advisory form</a>. Do not post sensitive information in a public issue.</p><h2>What to expect</h2><p>We review corrections against the cited source and update the page when the evidence supports a change. A correction may take time to appear in search results after publication.</p></div></section>'''
    return page('Contact and corrections', 'Report a factual correction, broken link, privacy concern or security issue to CareerSignal Lab.', body, 0, 'contact.html', {'@context': 'https://schema.org', '@type': 'ContactPage', 'name': 'Contact CareerSignal Lab', 'url': f'{BASE_URL}/contact.html'})


def build_disclosure():
    body = f'''<section class="site-shell page-hero"><h1>Advertising disclosure</h1><p>How commercial links and advertising are handled.</p></section><section class="site-shell section"><div class="content-card prose"><h2>Current status</h2><p>At the time of this review, CareerSignal Lab uses direct vendor links without affiliate tracking. If an affiliate relationship is added, the affected link will be disclosed before the first link and marked with <code>rel="sponsored"</code> where appropriate.</p><h2>Editorial independence</h2><p>Advertising and commercial relationships do not determine the stated strengths, limitations or recommendations of a product. A review may conclude that a free tool or a simpler workflow is the better choice.</p><h2>Advertising labels</h2><p>Advertising units are visually separated from editorial content and labeled. We do not place ads inside navigation, forms or screens that have no substantive publisher content.</p><h2>Questions</h2><p>If a disclosure is unclear, use the <a href="contact.html">contact page</a> and include the URL of the page you are reviewing.</p></div></section>'''
    return page('Advertising disclosure', 'CareerSignal Lab advertising, affiliate and editorial-independence disclosure.', body, 0, 'disclosure.html', {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Advertising disclosure', 'url': f'{BASE_URL}/disclosure.html'})


def build_privacy():
    body = f'''<section class="site-shell page-hero"><h1>Privacy and cookies</h1><p>What this site processes, how advertising consent works and how to report a concern.</p></section><section class="site-shell section"><div class="content-card prose"><h2>Hosting and basic access data</h2><p>CareerSignal Lab is hosted by Vercel. The hosting provider may process standard technical information such as an IP address, browser type, requested URL and timestamps to deliver and protect the site.</p><h2>Advertising</h2><p>The site may use Google AdSense after approval. Google and its partners may process cookies or device information in accordance with applicable consent choices and legal bases. Consent defaults are set to deny advertising storage, advertising user data and ad personalization until the consent mechanism applicable to your region updates them.</p><h2>Your choices</h2><p>Use the “Privacy choices” button in the footer to open the available consent controls or Google's ad settings. You can also use browser controls to block or delete cookies, though some site functions may change.</p><h2>External links and AI tools</h2><p>Links to Rezi, Teal, OpenAI, Anthropic, Grammarly and other services lead to third-party sites with their own privacy policies. If you upload a resume or interview notes to a third-party service, review that service's retention and training settings first. This site does not receive the contents of those uploads.</p><h2>Retention and contact</h2><p>This static site does not provide user accounts or store resume files. For a privacy question or correction, use the <a href="contact.html">contact page</a> and avoid posting sensitive information publicly.</p><p class="article-note">This page describes the current site configuration and is not legal advice. Privacy practices may change when hosting, advertising or analytics providers change.</p></div></section>'''
    return page('Privacy and cookies', 'CareerSignal Lab privacy notice for hosting, advertising, consent, external links and AI tools.', body, 0, 'privacy.html', {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Privacy and cookies', 'url': f'{BASE_URL}/privacy.html'})


def build_terms():
    body = f'''<section class="site-shell page-hero"><h1>Terms of use</h1><p>Terms for using this independent career-resource site.</p></section><section class="site-shell section"><div class="content-card prose"><h2>General information</h2><p>CareerSignal Lab publishes general research and workflow guidance. Product features, pricing, availability and policies can change without notice. Confirm current details with the vendor before purchasing or relying on a feature.</p><h2>No employment guarantee</h2><p>Nothing on this site guarantees an interview, job offer, ATS score, salary outcome or product result. Hiring decisions are made by employers and depend on factors outside this site's control.</p><h2>Acceptable use</h2><p>Do not scrape, republish or misrepresent the site content as your own. Do not use the contact forms to submit confidential credentials, another person's personal data or unlawful material.</p><h2>External services</h2><p>External links are provided for convenience. Their terms, privacy policies and content are controlled by their respective providers. A link does not imply an employer, partnership or endorsement relationship unless explicitly stated.</p><h2>Changes</h2><p>These terms may be updated as the site or its providers change. The current version is published on this page.</p></div></section>'''
    return page('Terms of use', 'Terms for using CareerSignal Lab and external links.', body, 0, 'terms.html', {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Terms of use', 'url': f'{BASE_URL}/terms.html'})


def build_not_found():
    body = '<section class="site-shell page-hero"><h1>Page not found</h1><p>The requested page may have been consolidated or removed.</p><p><a class="button" href="/index.html">Return home</a> <a class="button secondary" href="/guides/index.html">Browse guides</a></p></section>'
    return page('Page not found', 'The requested CareerSignal Lab page could not be found.', body, 0, '404.html', {'@context': 'https://schema.org', '@type': 'WebPage', 'name': 'Page not found'}, False)


def build_sitemap():
    paths = ['index.html', 'directory.html', 'guides/index.html', 'about.html', 'editorial-policy.html', 'contact.html', 'disclosure.html', 'privacy.html', 'terms.html']
    paths += [f'tools/{slug}.html' for slug in content.TOOL_META]
    paths += [f'guides/{slug}.html' for slug in content.ARTICLE_META]
    urls = ''.join(f'<url><loc>{bm.esc(BASE_URL + "/" if path == "index.html" else BASE_URL + "/" + path)}</loc><lastmod>2026-11-13</lastmod></url>' for path in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'


def main():
    bm.build_site(SITE)
    # 將 CareerSignal 主題接回基礎樣式，避免重建後版面退回通用樣式。
    css_path = OUT / 'assets' / 'styles.css'
    css_path.write_text(css_path.read_text(encoding='utf-8') + '\n' + (THEME_ROOT / 'career.css').read_text(encoding='utf-8'), encoding='utf-8')
    guides = OUT / 'guides'
    if guides.exists():
        shutil.rmtree(guides)
    guides.mkdir()
    (OUT / 'index.html').write_text(build_home(), encoding='utf-8')
    (OUT / 'directory.html').write_text(build_directory(), encoding='utf-8')
    (OUT / 'guides' / 'index.html').write_text(build_guides_index(), encoding='utf-8')
    for slug, meta in content.ARTICLE_META.items():
        (OUT / 'guides' / f'{slug}.html').write_text(render_article(slug, meta, content.ARTICLE_BODIES[slug]), encoding='utf-8')
    for slug, meta in content.TOOL_META.items():
        (OUT / 'tools' / f'{slug}.html').write_text(render_tool(slug, meta, content.TOOL_BODIES[slug]), encoding='utf-8')
    (OUT / 'about.html').write_text(build_about(), encoding='utf-8')
    (OUT / 'editorial-policy.html').write_text(build_editorial(), encoding='utf-8')
    (OUT / 'contact.html').write_text(build_contact(), encoding='utf-8')
    (OUT / 'disclosure.html').write_text(build_disclosure(), encoding='utf-8')
    (OUT / 'privacy.html').write_text(build_privacy(), encoding='utf-8')
    (OUT / 'terms.html').write_text(build_terms(), encoding='utf-8')
    (OUT / '404.html').write_text(build_not_found(), encoding='utf-8')
    (OUT / 'sitemap.xml').write_text(build_sitemap(), encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n', encoding='utf-8')
    vercel = {'cleanUrls': False, 'trailingSlash': False, 'headers': [{'source': '/(.*)', 'headers': [{'key': 'X-Content-Type-Options', 'value': 'nosniff'}, {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'}, {'key': 'Permissions-Policy', 'value': 'camera=(), microphone=(), geolocation=()'}]}]}
    (OUT / 'vercel.json').write_text(json.dumps(vercel, indent=2), encoding='utf-8')
    (OUT / 'site.webmanifest').write_text(json.dumps({'name': SITE['brand'], 'short_name': 'CareerSignal', 'start_url': '/', 'display': 'standalone', 'background_color': '#f5efe4', 'theme_color': SITE['accent']}, indent=2), encoding='utf-8')
    report = {'project': SITE['project'], 'domain': BASE_URL, 'guides': len(content.ARTICLE_META), 'tools': len(content.TOOL_META), 'reviewed': REVIEWED, 'sitemap_urls': len(re.findall(r'<url>', build_sitemap()))}
    (ROOT / 'multisite' / 'career-build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()


