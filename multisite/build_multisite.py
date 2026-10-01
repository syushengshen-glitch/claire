from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT_DIR = ROOT / 'scripts'
SOURCE_SITE = ROOT / 'site'
OUT_ROOT = ROOT / 'sites'
PUBLISHER = 'ca-pub-1837836558769995'
TODAY = 'October 1, 2026'

SOURCE_TOOLS = []
for filename in ['tools_data_1.json', 'tools_data_2.json']:
    SOURCE_TOOLS.extend(json.loads((SOURCE_SCRIPT_DIR / filename).read_text(encoding='utf-8')))
TOOL_MAP = {tool['slug']: tool for tool in SOURCE_TOOLS}

CUSTOM_TOOLS = {
    'rezi': {
        'name':'Rezi','slug':'rezi','category':'career','featured':True,
        'tagline':'AI resume builder focused on job-description matching and ATS-friendly structure.',
        'best_for':'Job seekers who want to tailor a resume to a specific posting.',
        'pricing':'Free tier available; paid plans vary.',
        'strengths':['Job-description matching','ATS-focused formatting','Guided resume sections'],
        'limits':['AI suggestions still need factual review','Templates can feel standardized','Advanced exports may require payment'],
        'tags':['Free tier','Resume','ATS'],'url':'https://www.rezi.ai/'
    },
    'teal': {
        'name':'Teal','slug':'teal','category':'career','featured':False,
        'tagline':'Job-search platform with resume tailoring, tracking, and keyword feedback.',
        'best_for':'Candidates managing several applications and versions of a resume.',
        'pricing':'Free tier available; premium plans vary.',
        'strengths':['Application tracking','Keyword feedback','Resume version management'],
        'limits':['Not every suggestion is relevant','Premium features may be needed','Requires careful privacy review'],
        'tags':['Free tier','Career','Tracking'],'url':'https://www.tealhq.com/'
    },
    'tidio-lyro': {
        'name':'Tidio Lyro','slug':'tidio-lyro','category':'chatbot','featured':False,
        'tagline':'AI customer-service chatbot for common questions and human handoff.',
        'best_for':'Small websites that need a lightweight support bot.',
        'pricing':'Free tier available; paid plans vary.',
        'strengths':['Quick website setup','FAQ automation','Human takeover workflow'],
        'limits':['Quality depends on knowledge base','Conversation limits vary by plan','Advanced automation costs more'],
        'tags':['Free tier','Support','Chatbot'],'url':'https://www.tidio.com/'
    },
    'chatbase': {
        'name':'Chatbase','slug':'chatbase','category':'chatbot','featured':True,
        'tagline':'Custom chatbot builder trained on website and document content.',
        'best_for':'Teams that want a branded support or lead-generation chatbot.',
        'pricing':'Free tier may be limited; paid plans vary.',
        'strengths':['Custom knowledge sources','Embeddable widget','Analytics for conversations'],
        'limits':['Needs clean source content','Usage limits depend on plan','Requires ongoing answer review'],
        'tags':['Chatbot','Support','Custom'],'url':'https://www.chatbase.co/'
    }
}

SITES = [
    {
        'slug':'coding','project':'signalstack-coding-lab','brand':'CodeSignal Lab','topic':'AI coding agents and developer tools','accent':'#2457d6','accent2':'#f2684a',
        'tagline':'Compare AI coding agents by the work they can actually finish.','description':'An independent index of AI coding agents, editor assistants, code review tools, and developer workflows.','audience':'developers, technical founders, and beginner programmers',
        'trends':[('opencode','+90%'),('ollama','+90%')],
        'tools':['cursor','github-copilot','windsurf','replit','coderabbit'],
        'articles':[
            {'slug':'best-ai-coding-agents-for-beginners','title':'Best AI coding agents for beginners','dek':'A practical shortlist for learning without copy-paste debt.','picks':['replit','github-copilot','cursor'],'focus':'Ship a small project while understanding the code.'},
            {'slug':'copilot-vs-cursor-for-small-teams','title':'GitHub Copilot vs Cursor for small teams','dek':'Where each assistant fits in a small engineering workflow.','picks':['github-copilot','cursor','coderabbit'],'focus':'Choose the assistant with the least review overhead.'},
            {'slug':'review-ai-generated-code','title':'How to review AI-generated code','dek':'A practical checklist for tests, security, and maintainability.','picks':['coderabbit','github-copilot','windsurf'],'focus':'Make every generated change reviewable before it ships.'}
        ]
    },
    {
        'slug':'voice','project':'signalstack-voice-lab','brand':'VoiceSignal Lab','topic':'AI voice, dubbing, and narration tools','accent':'#8b3fd1','accent2':'#f4c95d',
        'tagline':'Find the right voice workflow without losing control of consent or quality.','description':'A research index for AI voice generation, narration, dubbing, and audio editing tools.','audience':'creators, educators, and media teams',
        'trends':[('fish audio','+1,400%'),('kokoro voices','Breakout')],
        'tools':['elevenlabs','descript','synthesia','canva-magic-studio','runway'],
        'articles':[
            {'slug':'best-ai-voice-generators','title':'Best AI voice generators for creators','dek':'Narration, dubbing, and voice-consent questions to check first.','picks':['elevenlabs','descript','canva-magic-studio'],'focus':'Produce clear narration while keeping voice rights visible.'},
            {'slug':'elevenlabs-vs-descript-voice-workflows','title':'ElevenLabs vs Descript for voice workflows','dek':'Generation, editing, and podcast production compared by workflow.','picks':['elevenlabs','descript','synthesia'],'focus':'Choose based on whether the bottleneck is voice creation or editing.'},
            {'slug':'ai-dubbing-checklist','title':'AI dubbing checklist before publishing','dek':'Pronunciation, consent, disclosure, and quality checks.','picks':['elevenlabs','synthesia','runway'],'focus':'Review synthetic voice and video before it reaches an audience.'}
        ]
    },
    {
        'slug':'support','project':'signalstack-support-lab','brand':'SupportSignal Lab','topic':'AI customer support and service automation','accent':'#0f766e','accent2':'#f97316',
        'tagline':'Compare support automation without hiding the human handoff.','description':'A practical directory for AI customer support, knowledge-base, and service automation tools.','audience':'support leaders and small business owners',
        'trends':[('otter ai','+750%'),('microsoft teams ai meeting notes','+50%')],
        'tools':['intercom-fin','zapier-ai','notion-ai','fathom','otter-ai'],
        'articles':[
            {'slug':'best-ai-customer-support-tools','title':'Best AI customer support tools','dek':'A shortlist for FAQs, routing, summaries, and human escalation.','picks':['intercom-fin','zapier-ai','notion-ai'],'focus':'Resolve repetitive questions without losing a clear escalation path.'},
            {'slug':'reduce-support-response-time','title':'How to reduce support response time with AI','dek':'A workflow for triage, drafting, and escalation.','picks':['zapier-ai','intercom-fin','fathom'],'focus':'Reduce response time without automating customer commitments.'},
            {'slug':'human-handoff-policy-for-ai-support','title':'Human handoff policy for AI support','dek':'Rules for sensitive questions, refunds, and account issues.','picks':['intercom-fin','notion-ai','otter-ai'],'focus':'Document when an AI agent must stop and hand the conversation to a person.'}
        ]
    },
    {
        'slug':'meetings','project':'signalstack-meeting-lab','brand':'MeetingSignal Lab','topic':'AI meeting notes and meeting assistants','accent':'#2f6f4e','accent2':'#f1c75b',
        'tagline':'Turn meetings into searchable decisions without recording everything.','description':'An index of AI meeting note takers, transcription tools, and follow-up workflows.','audience':'remote teams, consultants, and managers',
        'trends':[('read ai meeting notes in teams','+300%'),('microsoft teams ai meeting notes','+50%')],
        'tools':['fathom','otter-ai','descript','notion-ai','clickup-ai'],
        'articles':[
            {'slug':'best-ai-meeting-note-tools','title':'Best AI meeting note tools for remote teams','dek':'Compare transcription, summaries, action items, and privacy controls.','picks':['fathom','otter-ai','descript'],'focus':'Capture decisions and owners with the least manual work.'},
            {'slug':'fathom-vs-otter-ai','title':'Fathom vs Otter.ai for meeting notes','dek':'Where each tool fits in a recurring meeting workflow.','picks':['fathom','otter-ai','notion-ai'],'focus':'Choose based on follow-up, integrations, and collaboration needs.'},
            {'slug':'ai-meeting-notes-privacy-checklist','title':'AI meeting notes privacy checklist','dek':'Consent, retention, access, and sensitive-topic rules.','picks':['notion-ai','fathom','clickup-ai'],'focus':'Record only what serves a clear team purpose.'}
        ]
    },
    {
        'slug':'websites','project':'signalstack-website-lab','brand':'WebSignal Lab','topic':'AI website builders and no-code launch tools','accent':'#8b5cf6','accent2':'#22c55e',
        'tagline':'Build and launch a useful site without adding a toolchain you cannot maintain.','description':'A directory of AI website builders, launch tools, and no-code workflows for small teams.','audience':'founders, consultants, and creators',
        'trends':[('figma ai website builder','+550%'),('best time to visit maldives','+600%')],
        'tools':['replit','chatgpt','claude','canva-magic-studio','notion-ai'],
        'articles':[
            {'slug':'best-ai-website-builders','title':'Best AI website builders for small teams','dek':'Pick based on hosting, editing, SEO, and ownership.','picks':['replit','canva-magic-studio','chatgpt'],'focus':'Launch a maintainable first version without locking in the wrong stack.'},
            {'slug':'figma-ai-vs-wix-ai-website-builders','title':'Figma AI vs Wix AI website builders','dek':'A comparison of design control and no-code speed.','picks':['chatgpt','claude','canva-magic-studio'],'focus':'Choose the workflow that matches your design and hosting needs.'},
            {'slug':'ai-website-launch-checklist','title':'AI website launch checklist','dek':'Analytics, privacy, SEO, and ownership before launch.','picks':['notion-ai','replit','claude'],'focus':'Do not publish an AI-generated site without a review and maintenance plan.'}
        ]
    },
    {
        'slug':'images','project':'signalstack-image-lab','brand':'ImageSignal Lab','topic':'AI image editing and visual production','accent':'#e11d48','accent2':'#f59e0b',
        'tagline':'Edit faster while keeping image rights, quality, and brand control visible.','description':'A directory of AI image editors, background removers, design assistants, and visual production tools.','audience':'designers, marketers, and creators',
        'trends':[('bg remover','Breakout'),('fooocus','Breakout'),('ai image describer','Breakout')],
        'tools':['midjourney','adobe-firefly','leonardo-ai','ideogram','canva-magic-studio'],
        'articles':[
            {'slug':'best-ai-image-editors','title':'Best AI image editors for creators','dek':'Compare editing, generation, text rendering, and rights checks.','picks':['adobe-firefly','canva-magic-studio','midjourney'],'focus':'Choose a tool that fits the final asset, not only the first generated draft.'},
            {'slug':'remove-background-tools-compared','title':'AI background removers compared','dek':'Quality, edges, export, and commercial-use questions.','picks':['adobe-firefly','canva-magic-studio','ideogram'],'focus':'Judge the result at the edges, not only on the preview.'},
            {'slug':'ai-image-editing-rights-checklist','title':'AI image editing rights checklist','dek':'Check model terms, source ownership, and disclosure before publishing.','picks':['midjourney','leonardo-ai','adobe-firefly'],'focus':'Document the rights and limitations behind every published visual.'}
        ]
    },
    {
        'slug':'career','project':'signalstack-career-lab','brand':'CareerSignal Lab','topic':'AI resume and job-search tools','accent':'#0369a1','accent2':'#f97316',
        'tagline':'Use AI to tailor applications without inventing experience.','description':'A practical index of AI resume builders, job trackers, editing tools, and career workflows.','audience':'students, career changers, and job seekers',
        'trends':[('ai resume builder based on job description','+200%'),('rezi','+110%')],
        'tools':['rezi','teal','chatgpt','claude','grammarly'],
        'articles':[
            {'slug':'best-ai-resume-builders','title':'Best AI resume builders for job seekers','dek':'Compare ATS formatting, job matching, and editing control.','picks':['rezi','teal','grammarly'],'focus':'Tailor the resume without losing factual accuracy.'},
            {'slug':'rezi-vs-teal','title':'Rezi vs Teal for resume tailoring','dek':'Where each tool helps during a multi-application search.','picks':['rezi','teal','chatgpt'],'focus':'Choose based on whether you need formatting or application tracking.'},
            {'slug':'ai-resume-tailoring-without-fake-experience','title':'AI resume tailoring without fake experience','dek':'A human-review workflow for keywords, evidence, and ethics.','picks':['chatgpt','claude','grammarly'],'focus':'Use AI to clarify real experience, not to invent it.'}
        ]
    },
    {
        'slug':'visual','project':'signalstack-visual-lab','brand':'VisualSignal Lab','topic':'AI visual and video generation models','accent':'#7c3aed','accent2':'#06b6d4',
        'tagline':'Explore generative image and video models with the rights questions attached.','description':'A comparison index for AI image generators, video models, and visual production workflows.','audience':'creators, agencies, and product teams',
        'trends':[('nano banana','+2,400%'),('kling ai','+1,500%'),('sora ai','+650%')],
        'tools':['midjourney','ideogram','leonardo-ai','runway','synthesia'],
        'articles':[
            {'slug':'best-ai-visual-generators','title':'Best AI visual generators for image and video','dek':'A workflow-first comparison of aesthetics, controls, and rights.','picks':['midjourney','runway','ideogram'],'focus':'Match the generator to the final format and review process.'},
            {'slug':'sora-vs-kling-ai','title':'Sora vs Kling AI for AI video generation','dek':'Compare continuity, controls, export, and commercial terms.','picks':['runway','synthesia','leonardo-ai'],'focus':'Do not compare generated clips without checking rights and consistency.'},
            {'slug':'ai-video-rights-and-disclosure','title':'AI video rights and disclosure checklist','dek':'Voice, likeness, synthetic media, and platform rules.','picks':['runway','synthesia','midjourney'],'focus':'Publish synthetic media only with clear rights and disclosure.'}
        ]
    },
    {
        'slug':'seo','project':'signalstack-seo-lab','brand':'SearchSignal Lab','topic':'AI SEO content and optimization tools','accent':'#0f766e','accent2':'#facc15',
        'tagline':'Use AI for research and structure while keeping editorial judgment human.','description':'A directory of AI SEO writing, research, optimization, and editorial workflow tools.','audience':'content marketers, SEO writers, and small publishers',
        'trends':[('uploadarticle.com','Breakout'),('opencode','+90%')],
        'tools':['surfer-seo','jasper','copy-ai','grammarly','chatgpt'],
        'articles':[
            {'slug':'best-ai-seo-content-tools','title':'Best AI SEO content tools','dek':'Compare briefs, drafting, editing, and on-page optimization.','picks':['surfer-seo','jasper','grammarly'],'focus':'Keep search intent and original evidence ahead of keyword score.'},
            {'slug':'surfer-seo-vs-frase','title':'Surfer SEO vs Frase for content briefs','dek':'A workflow comparison for briefs, research, and editing.','picks':['surfer-seo','copy-ai','chatgpt'],'focus':'Choose the brief workflow that leaves the least manual cleanup.'},
            {'slug':'human-review-workflow-for-ai-seo-content','title':'Human review workflow for AI SEO content','dek':'Sources, originality, links, and corrections before publishing.','picks':['chatgpt','grammarly','surfer-seo'],'focus':'AI may assist the draft, but a person owns the final answer.'}
        ]
    },
    {
        'slug':'chatbot','project':'signalstack-chatbot-lab','brand':'BotSignal Lab','topic':'AI chatbot builders and customer automation','accent':'#4338ca','accent2':'#f97316',
        'tagline':'Build a useful support bot without hiding the escalation path.','description':'A comparison index for AI chatbot builders, knowledge-base agents, and customer-service automation.','audience':'support teams, SaaS founders, and agencies',
        'trends':[('chatbot','+800%'),('otter ai','+750%')],
        'tools':['chatbase','tidio-lyro','intercom-fin','zapier-ai','notion-ai'],
        'articles':[
            {'slug':'best-ai-chatbot-builders','title':'Best AI chatbot builders for small teams','dek':'Compare knowledge sources, handoff, analytics, and pricing.','picks':['chatbase','tidio-lyro','intercom-fin'],'focus':'Choose a bot that knows when to stop.'},
            {'slug':'chatbase-vs-botpress','title':'Chatbase vs Botpress for support bots','dek':'No-code speed compared with deeper automation control.','picks':['chatbase','tidio-lyro','zapier-ai'],'focus':'Pick the level of control your team can maintain.'},
            {'slug':'ai-chatbot-escalation-checklist','title':'AI chatbot escalation checklist','dek':'Sensitive questions, failed answers, refunds, and human ownership.','picks':['intercom-fin','chatbase','notion-ai'],'focus':'Define exactly when a person must take over.'}
        ]
    }
]

def esc(value):
    return html.escape(str(value), quote=True)


def base_url(site):
    return f"https://{site['project']}.vercel.app"


def get_tool(slug):
    return CUSTOM_TOOLS.get(slug) or TOOL_MAP[slug]


def header(site, depth=0, current=''):
    prefix = '../' if depth else ''
    return f'''<header class="site-header"><div class="site-shell header-inner"><a class="brand" href="{prefix}index.html"><span class="brand-mark"><span></span></span><span>{esc(site['brand'])}</span></a><button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Toggle navigation">Menu</button><nav class="site-nav" data-site-nav><a href="{prefix}directory.html">Directory</a><a href="{prefix}guides/index.html">Guides</a><a href="{prefix}editorial-policy.html">Method</a><a href="{prefix}about.html">About</a></nav></div></header>'''


def footer(site, depth=0):
    prefix = '../' if depth else ''
    return f'''<footer class="site-footer"><div class="site-shell"><div class="footer-grid"><div><a class="brand" href="{prefix}index.html"><span class="brand-mark"><span></span></span><span>{esc(site['brand'])}</span></a><p>{esc(site['description'])}</p></div><div><h2>Explore</h2><a href="{prefix}directory.html">Directory</a><a href="{prefix}guides/index.html">Guides</a><a href="{prefix}editorial-policy.html">Editorial method</a></div><div><h2>Trust</h2><a href="{prefix}about.html">About</a><a href="{prefix}contact.html">Contact</a><a href="{prefix}privacy.html">Privacy</a><a href="{prefix}terms.html">Terms</a></div></div><div class="footer-bottom"><span>© <span data-year>2026</span> {esc(site['brand'])}.</span><button class="text-button" type="button" data-manage-consent>Privacy choices</button></div></div></footer>'''


def page(site, title, description, body, depth=0, path=''):
    prefix = '../' if depth else ''
    canonical = f"{base_url(site)}/{path}" if path else base_url(site) + '/'
    schema = {'@context':'https://schema.org','@type':'WebSite','name':site['brand'],'url':base_url(site),'description':site['description']}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | {esc(site['brand'])}</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{esc(canonical)}"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/styles.css"><style>:root{{--blue:{site['accent']};--coral:{site['accent2']};}}</style><script>window.SIGNALSHELF_ADSENSE_CLIENT="{PUBLISHER}";</script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body class="theme-{site['slug']}">{header(site, depth)}<main id="main">{body}</main>{footer(site, depth)}<script src="{prefix}assets/app.js" defer></script></body></html>'''


def tool_row(site, tool, depth=0):
    prefix = '../' if depth else ''
    tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in tool['tags'])
    return f'''<article class="tool-row"><div class="tool-mark">{esc(tool['name'][0])}</div><div class="tool-info"><h3><a href="{prefix}tools/{esc(tool['slug'])}.html">{esc(tool['name'])}</a></h3><p>{esc(tool['tagline'])}</p><div class="tool-meta">{tags}</div></div><div class="tool-actions"><a class="button" href="{esc(tool['url'])}" target="_blank" rel="noopener">Visit site</a><a class="button secondary" href="{prefix}tools/{esc(tool['slug'])}.html">Read review</a></div></article>'''


def build_article(site, article):
    picks = [get_tool(slug) for slug in article['picks']]
    body = f'''<article><header class="site-shell article-header"><nav class="breadcrumbs"><a href="../index.html">Home</a> / <a href="index.html">Guides</a> / {esc(article['title'])}</nav><h1>{esc(article['title'])}</h1><p class="dek">{esc(article['dek'])}</p><p class="article-meta">Reviewed {TODAY} · {esc(site['brand'])} · Advertising is labeled separately</p></header><div class="site-shell content-grid"><div class="content-card prose"><p>{esc(article['focus'])} This guide uses the same shortlist criteria across every tool: the job it solves, the limits a buyer should verify, export and privacy considerations, and the total correction cost.</p><h2>How to choose</h2><p>Start with one real task and test every candidate using the same input. Record setup time, first usable result, correction time, cost, export limits, and the person responsible for approval.</p><div class="callout"><strong>Decision rule:</strong> keep a tool only when it improves the finished result after corrections.</div><h2>The shortlist</h2>{''.join(f'<h3><a href="../tools/{esc(tool["slug"])}.html">{esc(tool["name"])}</a></h3><p>{esc(tool["tagline"])} Best for: {esc(tool["best_for"])}. Watch for: {esc(tool["limits"][0])}.</p>' for tool in picks)}<h2>Workflow</h2><ol><li>Define the output and the reviewer.</li><li>Give the tool real, non-sensitive examples.</li><li>Verify facts, links, rights, and customer commitments.</li><li>Publish only after a human editor approves the result.</li></ol><h2>Verdict</h2><p>{esc(article['focus'])} The best choice is the smallest stack that improves the final output without hiding the review step.</p><h2>Sources</h2><ul>{''.join(f'<li><a href="{esc(tool["url"])}" target="_blank" rel="noopener">{esc(tool["name"])} official site</a></li>' for tool in picks)}<li><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content" target="_blank" rel="noopener">Google Search Central: helpful content guidance</a></li></ul></div><aside class="side-stack"><div class="side-panel compact"><h2>Experiment rule</h2><p>This starter article still needs first-hand screenshots and test results before it should be used as an original review.</p></div></aside></div></article>'''
    return page(site, article['title'], article['dek'], body, 1, f"guides/{article['slug']}.html")


def build_site(site):
    out = OUT_ROOT / site['slug']
    if out.exists():
        shutil.rmtree(out)
    (out / 'assets').mkdir(parents=True)
    (out / 'tools').mkdir()
    (out / 'guides').mkdir()
    shutil.copy2(SOURCE_SITE / 'assets' / 'styles.css', out / 'assets' / 'styles.css')
    shutil.copy2(SOURCE_SITE / 'assets' / 'app.js', out / 'assets' / 'app.js')
    shutil.copy2(SOURCE_SITE / 'favicon.svg', out / 'favicon.svg')
    tools = [get_tool(slug) for slug in site['tools']]
    rows = ''.join(tool_row(site, tool, 0) for tool in tools)
    articles = ''.join(f'<article class="article-card"><h3><a href="guides/{esc(a["slug"])}.html">{esc(a["title"])}</a></h3><p>{esc(a["dek"])}</p><a href="guides/{esc(a["slug"])}.html">Read the guide</a></article>' for a in site['articles'])
    trends = ', '.join(f'{q} {change}' for q, change in site['trends'])
    home = f'''<section class="site-shell hero"><div class="hero-copy"><span class="hero-note">Google Trends seed: {esc(trends)}</span><h1>{esc(site['tagline'])}</h1><p class="hero-intro">{esc(site['description'])} Built for {esc(site['audience'])}.</p><form class="search-panel" data-search-form data-search-target="directory.html"><label class="sr-only" for="hero-search">Search tools</label><input id="hero-search" name="q" type="search" placeholder="Search this niche"><button type="submit">Search directory</button></form></div><div class="radar"><div class="radar-center">{len(tools)} tools<br>1 niche</div><span class="radar-node n1">{esc(site['topic'])}</span><span class="radar-node n2">Use cases</span><span class="radar-node n3">Limits</span><span class="radar-node n4">Pricing</span><span class="radar-node n5">Workflows</span></div></section><section class="site-shell section"><div class="section-heading"><h2>Start with the work</h2><p>Each guide links a practical workflow to tools, limits, and approval questions.</p></div><div class="tool-list">{rows}</div></section><section class="site-shell section"><div class="section-heading"><h2>Guides</h2><p>Starter articles for this niche. Add original tests and screenshots before publication.</p></div><div class="article-grid">{articles}</div></section>'''
    (out / 'index.html').write_text(page(site, site['brand'], site['description'], home, 0, ''), encoding='utf-8')
    directory = f'''<section class="site-shell page-hero"><h1>{esc(site['topic'])}</h1><p>{esc(site['description'])}</p></section><section class="site-shell section"><div class="tool-list">{rows}</div></section>'''
    (out / 'directory.html').write_text(page(site, f"{site['topic']} directory", site['description'], directory, 0, 'directory.html'), encoding='utf-8')
    for tool in tools:
        strengths = ''.join(f'<li>{esc(x)}</li>' for x in tool['strengths'])
        limits = ''.join(f'<li>{esc(x)}</li>' for x in tool['limits'])
        body = f'''<section class="site-shell page-hero"><nav class="breadcrumbs"><a href="../index.html">Home</a> / <a href="../directory.html">Directory</a> / {esc(tool['name'])}</nav><h1>{esc(tool['name'])} review</h1><p>{esc(tool['tagline'])}</p></section><section class="site-shell section"><div class="content-grid"><article class="content-card prose"><div class="callout"><strong>Best for:</strong> {esc(tool['best_for'])}</div><h2>Strengths</h2><ul>{strengths}</ul><h2>Limits to verify</h2><ul>{limits}</ul><h2>Fit in this niche</h2><p>Test {esc(tool['name'])} on one real {esc(site['topic'].lower())} task. Record correction time, export limits, pricing, privacy, and commercial terms before adding it to a workflow.</p><p><a class="button" href="{esc(tool['url'])}" target="_blank" rel="noopener">Open {esc(tool['name'])}</a></p><h2>Sources</h2><p>Reviewed {TODAY}. Confirm current features and pricing on the official site.</p></article><aside class="side-stack"><div class="side-panel"><h2>At a glance</h2><p><strong>Pricing:</strong> {esc(tool['pricing'])}</p><p><strong>Tags:</strong> {esc(', '.join(tool['tags']))}</p></div></aside></div></section>'''
        (out / 'tools' / f"{tool['slug']}.html").write_text(page(site, f"{tool['name']} review", tool['tagline'], body, 1, f"tools/{tool['slug']}.html"), encoding='utf-8')
    guide_cards = ''.join(f'<article class="article-card"><h3><a href="{esc(a["slug"])}.html">{esc(a["title"])}</a></h3><p>{esc(a["dek"])}</p></article>' for a in site['articles'])
    (out / 'guides' / 'index.html').write_text(page(site, f"{site['topic']} guides", f"Workflow guides for {site['audience']}.", f'<section class="site-shell page-hero"><h1>Guides for {esc(site["audience"])}</h1><p>{esc(site["description"])}</p></section><section class="site-shell section"><div class="article-grid">{guide_cards}</div></section>', 1, 'guides/index.html'), encoding='utf-8')
    for article in site['articles']:
        (out / 'guides' / f"{article['slug']}.html").write_text(build_article(site, article), encoding='utf-8')
    about = f'<section class="site-shell page-hero"><h1>About {esc(site["brand"])}</h1><p>{esc(site["description"])}</p></section><section class="site-shell section"><div class="content-card prose"><p>This independent directory covers {esc(site["topic"])} for {esc(site["audience"])}.</p><p>Listings prioritize practical strengths, material limits, pricing notes, and review steps. Confirm current product details with each vendor.</p><p>Advertising is labeled and kept separate from editorial recommendations.</p></div></section>'
    (out / 'about.html').write_text(page(site, f"About {site['brand']}", site['description'], about, 0, 'about.html'), encoding='utf-8')
    legal_pages = {
        'privacy.html': ('Privacy and cookies','How this site handles hosting data, AdSense consent, and external links.', ['This site uses Google Consent Mode with advertising storage, user data, and personalization denied by default. Google-certified consent messaging manages choices where required by law.','The site is hosted by Vercel and may use Google AdSense. Google and its partners may process cookies and device information after consent or under applicable legal bases.','External tool links have their own privacy policies. Review the destination before submitting personal information.']),
        'terms.html': ('Terms of use','Terms for using this independent directory.', ['Information is provided for general research. Product features, pricing, and availability can change without notice.','Do not scrape, republish, or misrepresent the site content. External links are provided for convenience.','Confirm current terms with each vendor before purchase or commercial use.']),
        'contact.html': ('Contact','Public and private contact channels for corrections and privacy requests.', ['Corrections: use the public issue form at https://github.com/syushengshen-glitch/claire/issues/new.','Privacy and security: use https://github.com/syushengshen-glitch/claire/security/advisories/new. Do not post sensitive information publicly.']),
        'disclosure.html': ('Advertising disclosure','How advertising and affiliate relationships are labeled.', ['Advertising units are labeled and kept separate from editorial recommendations.','Affiliate links, if added, will be disclosed before the first link and marked rel="sponsored".','Commercial relationships do not change the stated tool limits or editorial conclusions.']),
        'editorial-policy.html': ('Editorial policy','How listings and guides are reviewed and corrected.', ['Every listing starts with a defined job, audience, pricing note, strengths, and limits.','AI assistance may support research or drafting, but a human remains responsible for accuracy and publication.','Corrections should update the page, review date, and internal links.'])
    }
    for filename, (title, desc, paragraphs) in legal_pages.items():
        body = f'<section class="site-shell page-hero"><h1>{esc(title)}</h1><p>{esc(desc)}</p></section><section class="site-shell section"><div class="content-card prose">{"".join(f"<p>{esc(p)}</p>" for p in paragraphs)}</div></section>'
        (out / filename).write_text(page(site, title, desc, body, 0, filename), encoding='utf-8')
    (out / '404.html').write_text(page(site, 'Page not found', 'The requested page could not be found.', '<section class="site-shell page-hero"><h1>Page not found</h1><p><a class="button" href="index.html">Return home</a></p></section>', 0, '404.html'), encoding='utf-8')
    paths = ['index.html','directory.html','guides/index.html','about.html','privacy.html','terms.html','contact.html','disclosure.html','editorial-policy.html'] + [f'tools/{t["slug"]}.html' for t in tools] + [f'guides/{a["slug"]}.html' for a in site['articles']]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{esc(base_url(site) + "/" + p)}</loc><lastmod>2026-10-01</lastmod></url>' for p in paths) + '</urlset>'
    (out / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (out / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {base_url(site)}/sitemap.xml\n', encoding='utf-8')
    (out / 'ads.txt').write_text(f'google.com, pub-1837836558769995, DIRECT, f08c47fec0942fa0\n', encoding='utf-8')
    (out / 'vercel.json').write_text(json.dumps({'cleanUrls':True,'trailingSlash':False,'headers':[{'source':'/(.*)','headers':[{'key':'X-Content-Type-Options','value':'nosniff'},{'key':'Referrer-Policy','value':'strict-origin-when-cross-origin'}]}]}, indent=2), encoding='utf-8')
    (out / 'site.webmanifest').write_text(json.dumps({'name':site['brand'],'short_name':site['brand'],'start_url':'/','display':'standalone','background_color':'#edf4f2','theme_color':site['accent']}, indent=2), encoding='utf-8')
    return {'slug':site['slug'],'project':site['project'],'domain':f"{site['project']}.vercel.app",'pages':len(paths)+6,'tools':len(tools),'articles':len(site['articles'])}

def main():
    results = [build_site(site) for site in SITES]
    report = {'publisher':PUBLISHER,'built':results}
    (ROOT / 'multisite' / 'build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

