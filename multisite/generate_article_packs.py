from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'multisite' / 'article-packs'
OUT.mkdir(parents=True, exist_ok=True)

def slugify(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')

CODING = [
('Best AI coding agents for beginners','beginner developers','Choose an agent that explains code and keeps changes reviewable.','getting started'),
('GitHub Copilot vs Cursor for small teams','small engineering teams','Compare inline assistance with an AI-first editor workflow.','tool comparison'),
('How to review AI-generated code','developers','Use tests, diffs, security checks, and ownership before merging.','code review'),
('Cursor vs Windsurf for multi-file edits','developers','Compare project context, agent control, and review overhead.','tool comparison'),
('GitHub Copilot code review checklist','reviewers','Build a repeatable checklist for AI-assisted pull requests.','code review'),
('How to debug code with AI without wasting time','developers','Turn vague errors into reproducible test cases before asking for fixes.','debugging'),
('Best AI tools for writing unit tests','test engineers','Use AI for test ideas while keeping assertions meaningful.','testing'),
('How to review AI-generated SQL safely','data developers','Check joins, filters, permissions, performance, and destructive operations.','security'),
('AI coding assistant privacy checklist','engineering leaders','Review code sharing, retention, training, and access controls.','security'),
('Best AI tools for legacy code refactoring','senior developers','Modernize code in small, tested steps instead of large rewrites.','refactoring'),
('How to use AI for codebase onboarding','new developers','Map architecture, conventions, entry points, and risky areas.','onboarding'),
('How to write better prompts for coding agents','developers','Provide constraints, examples, acceptance criteria, and file context.','prompting'),
('Best AI tools for frontend development','frontend developers','Compare component generation, accessibility, styling, and review.','frontend'),
('Best AI tools for backend development','backend developers','Compare API, database, authentication, and test workflows.','backend'),
('How to use AI for API documentation','API teams','Generate a first draft without losing examples and version history.','documentation'),
('AI-assisted accessibility testing for developers','frontend teams','Combine automated checks with keyboard and screen-reader review.','accessibility'),
('Best AI tools for JavaScript debugging','JavaScript developers','Compare editor, browser, and code-review workflows.','debugging'),
('Best AI tools for Python developers','Python developers','Compare notebook, script, package, and test workflows.','python'),
('AI coding agent security risks to check','security engineers','Review secrets, prompt injection, dependencies, and generated commands.','security'),
('How to use AI for pull request summaries','developers','Write useful summaries that preserve decisions and risk.','collaboration'),
('Best AI tools for CI/CD troubleshooting','DevOps engineers','Investigate failing pipelines without hiding root causes.','devops'),
('AI coding tools for solo founders','technical founders','Ship small features while preserving maintainability and tests.','founders'),
('Best AI tools for learning algorithms','computer science students','Use explanations, examples, and complexity analysis without copying answers.','education'),
('How to use AI to understand an unfamiliar repository','developers','Create a map of files, dependencies, tests, and change boundaries.','onboarding'),
('Best AI coding tools for TypeScript','TypeScript developers','Compare type-aware suggestions, refactors, and test generation.','typescript'),
('How to use AI for database migrations','backend teams','Plan reversible migrations with backups, checks, and rollback criteria.','database'),
('Best AI tools for software testing','QA engineers','Compare test planning, generation, maintenance, and triage.','testing'),
('How to use AI for performance optimization','engineers','Measure first, then test one hypothesis at a time.','performance'),
('AI tools for technical writing and docs','technical writers','Use AI for structure and consistency while preserving accuracy.','documentation'),
('Best AI tools for code refactoring','software engineers','Compare safe refactoring, diff review, and regression testing.','refactoring'),
('How to use AI for regex and parsing tasks','developers','Build examples first and test edge cases before shipping.','utility'),
('Best AI tools for API development','backend developers','Compare schema design, implementation, tests, and documentation.','api'),
('How to use AI to review authentication code','security teams','Check session handling, secrets, permissions, and failure modes.','security'),
('Best AI tools for mobile app development','mobile developers','Compare UI generation, platform APIs, testing, and store constraints.','mobile'),
('How to use AI for game development prototypes','game developers','Prototype mechanics quickly while separating throwaway code.','gamedev'),
('Best AI tools for data engineering','data engineers','Compare SQL, pipeline, validation, and orchestration support.','data'),
('How to use AI for infrastructure as code','platform engineers','Review generated Terraform and cloud changes before apply.','devops'),
('Best AI tools for open-source maintainers','maintainers','Use AI for triage and summaries without automating trust.','open-source'),
('How to use AI for release notes','product engineers','Convert merged changes into accurate, user-facing notes.','documentation'),
('Best AI tools for code migration projects','engineering teams','Plan migrations by dependency, test coverage, and rollback risk.','migration'),
('How to use AI for monorepo development','platform teams','Manage context, ownership, and affected-project changes.','monorepo'),
('Best AI tools for CLI development','developer-tool teams','Compare command design, tests, documentation, and packaging.','cli'),
('How to use AI for architecture reviews','staff engineers','Use AI to surface tradeoffs, not to make the decision.','architecture'),
('Best AI coding agents for data privacy','privacy-conscious teams','Compare controls for code retention, training, and access.','privacy'),
('How to evaluate an AI coding assistant','engineering leaders','Score completion, correction time, review risk, and total cost.','evaluation'),
('Best AI tools for test data generation','QA teams','Create realistic synthetic data without copying production records.','testing'),
('How to use AI for incident summaries','incident responders','Reconstruct the timeline and preserve unresolved uncertainty.','incident-response'),
('Best AI tools for frontend accessibility reviews','accessibility teams','Combine AI checks with manual testing and assistive technology.','accessibility'),
('How to use AI for legacy documentation','technical writers','Recover knowledge in small, source-linked increments.','documentation'),
('AI coding agent metrics every team should track','engineering managers','Measure accepted changes, correction time, escaped bugs, and cost.','metrics'),
]

CAREER = [
('Best AI resume builders for job seekers','job seekers','Compare ATS formatting, job matching, exports, and editing control.','resume'),
('Rezi vs Teal for resume tailoring','job seekers','Compare formatting, tracking, keyword feedback, and workflow.','tool comparison'),
('AI resume tailoring without fake experience','career changers','Use AI to clarify real evidence instead of inventing achievements.','ethics'),
('Best AI cover letter workflows','applicants','Build a specific letter without repeating the resume.','cover letter'),
('ATS resume checklist','job seekers','Check structure, keywords, dates, and file format before applying.','ats'),
('How to use ChatGPT for interview practice','interview candidates','Create realistic questions and feedback without memorizing scripts.','interviews'),
('STAR interview answers with AI feedback','job seekers','Strengthen evidence, scope, action, and measurable outcome.','interviews'),
('Best AI tools for LinkedIn profile optimization','professionals','Improve clarity and discoverability without keyword stuffing.','linkedin'),
('How to write recruiter outreach with AI','job seekers','Personalize the message and keep it short enough to read.','outreach'),
('Best AI tools for salary negotiation preparation','job seekers','Prepare evidence, ranges, questions, and fallback positions.','negotiation'),
('How to compare job offers with AI','candidates','Compare compensation, growth, flexibility, risk, and values.','offers'),
('AI tools for career change research','career changers','Map transferable skills, target roles, and evidence gaps.','career change'),
('Best AI tools for internship applications','students','Tailor examples, deadlines, and follow-ups without exaggeration.','students'),
('How new graduates can use AI to find a job','new graduates','Build a focused search system and track each application.','students'),
('How to explain an employment gap','job seekers','Prepare a concise, factual explanation and future focus.','career gaps'),
('Best AI tools for laid-off professionals','job seekers','Organize a search, rebuild confidence, and prioritize applications.','layoffs'),
('How to return to work after a career break','returning professionals','Package current skills, refresh evidence, and choose realistic targets.','career break'),
('AI job search privacy checklist','privacy-conscious candidates','Protect personal data, resumes, references, and account information.','privacy'),
('Best AI tools for remote job applications','remote job seekers','Look for evidence of remote operations, time zones, and async work.','remote work'),
('How to research a company before an interview','candidates','Combine financial, product, customer, and employee signals.','research'),
('Best AI tools for technical interview preparation','developers','Practice explanations, tests, tradeoffs, and debugging aloud.','technical interviews'),
('How to use AI for product manager interview prep','product managers','Practice prioritization, metrics, stakeholder, and strategy questions.','product roles'),
('Best AI tools for data analyst job applications','data analysts','Show analysis process, business impact, and tool evidence.','data roles'),
('How to build a portfolio with AI assistance','creators','Use AI for structure and feedback while keeping work authentic.','portfolio'),
('Best AI tools for UX portfolio case studies','designers','Improve problem framing, decisions, evidence, and outcomes.','design'),
('How to write a career summary with AI','professionals','Turn experience into a concise positioning statement.','resume'),
('AI tools for networking follow-ups','professionals','Create timely, specific follow-ups that do not sound automated.','networking'),
('How to prepare questions for interviewers','candidates','Ask questions that reveal expectations, constraints, and team health.','interviews'),
('Best AI tools for behavioral interview practice','job seekers','Practice clear stories and receive structured feedback.','interviews'),
('How to negotiate a remote work offer','job seekers','Discuss location, travel, time zones, equipment, and performance.','negotiation'),
('AI tools for personal branding without exaggeration','professionals','Clarify positioning, proof, audience, and content themes.','branding'),
('How to create a 30-60-90 day plan with AI','candidates','Show priorities, learning goals, and early value.','interview presentations'),
('Best AI tools for sales job interviews','sales candidates','Prepare pipeline stories, metrics, role plays, and account plans.','sales roles'),
('How to use AI for marketing job applications','marketers','Tailor campaign evidence to channel, audience, and business result.','marketing roles'),
('Best AI tools for teacher career transitions','teachers','Translate instructional, communication, and planning skills honestly.','career change'),
('How to use AI for freelancer proposals','freelancers','Build scoped proposals with assumptions and exclusions.','freelancing'),
('AI tools for consulting case interview practice','consulting candidates','Practice structure, quantitative reasoning, and communication.','consulting'),
('How to build a referral request with AI','job seekers','Make the ask specific, low-effort, and easy to decline.','referrals'),
('Best AI tools for job application tracking','job seekers','Track versions, deadlines, contacts, and follow-ups.','tracking'),
('How to use AI to prepare for a panel interview','candidates','Coordinate concise answers for several interviewer perspectives.','interviews'),
('AI tools for public sector job applications','public sector candidates','Translate experience into structured selection criteria.','public sector'),
('How to prepare a teaching portfolio with AI','teachers','Organize philosophy, evidence, lesson design, and reflection.','education roles'),
('Best AI tools for academic CVs','researchers','Organize publications, grants, teaching, and service.','academic'),
('How to use AI for interview rejection feedback','job seekers','Find patterns, choose improvements, and avoid overreacting to one result.','job search'),
('AI tools for international job applications','international candidates','Adapt language, work authorization, and cultural context carefully.','international'),
('How to write a promotion case with AI','employees','Assemble scope, outcomes, evidence, and stakeholder support.','promotion'),
('Best AI tools for management interview preparation','managers','Practice people, conflict, strategy, and execution scenarios.','management'),
('AI career planning checklist for 90 days','professionals','Set evidence, network, learning, and application milestones.','planning'),
('How to audit your resume with AI','job seekers','Find contradictions, weak verbs, missing metrics, and outdated skills.','resume audit'),
('AI job search metrics to track weekly','job seekers','Measure qualified roles, applications, responses, interviews, and feedback.','metrics'),
]

def make_articles(items, tools, audience_default, workflow, faq):
    output = []
    for index, (title, audience, angle, cluster) in enumerate(items):
        selected = [tools[(index + offset) % len(tools)] for offset in range(3)]
        output.append({
            'slug': slugify(title),
            'title': title,
            'dek': angle,
            'focus': angle,
            'picks': selected,
            'cluster': cluster,
            'intro': f'{title} is a practical guide for {audience}. It focuses on decisions that affect the final result: setup time, correction effort, privacy, export control, cost, and the human review step. Product details should be checked against each vendor before publication.',
            'workflow': workflow,
            'verdict': f'For {audience}, start with one narrow task and compare the shortlisted tools using the same evidence. Keep the smallest workflow that improves the final result after corrections.',
            'faq': faq,
            'audience': audience
        })
    return output

coding_tools = ['cursor','github-copilot','windsurf','replit','coderabbit']
career_tools = ['rezi','teal','chatgpt','claude','grammarly']
coding_workflow = [
    'Define the behavior, constraints, and tests before asking the tool to change code.',
    'Give the agent the smallest relevant code and file context.',
    'Review the diff, run tests, and inspect security-sensitive changes.',
    'Commit a small reversible change and document anything still uncertain.'
]
career_workflow = [
    'Collect factual examples from your real experience and target role.',
    'Use AI to organize and clarify those examples, not to invent achievements.',
    'Check privacy, spelling, dates, metrics, and claims before submitting.',
    'Track the version, result, and feedback so the next application improves.'
]
coding_faq = [
    {'q':'Can AI-generated code be used in production?','a':'Only after tests, security review, dependency checks, and human understanding. AI output should be treated as an unreviewed draft.'},
    {'q':'Should teams share private code with an AI tool?','a':'Only when the tool and plan meet the organization policy for retention, training, access, and sensitive data.'},
    {'q':'What is the best way to measure an AI coding assistant?','a':'Track completion time, correction effort, review findings, escaped bugs, and total cost rather than only suggestion acceptance.'}
]
career_faq = [
    {'q':'Can AI write my resume?','a':'AI can organize and edit your evidence, but it should not invent experience, metrics, skills, or credentials.'},
    {'q':'Should I use the same resume for every job?','a':'Start from one master resume, then tailor the summary, evidence order, and keywords honestly for each role.'},
    {'q':'What should I remove before using an AI job tool?','a':'Remove unnecessary personal identifiers, references, private employer information, and any data the tool does not need.'}
]

(OUT / 'coding.json').write_text(json.dumps(make_articles(CODING, coding_tools, 'developers', coding_workflow, coding_faq), ensure_ascii=False, indent=2), encoding='utf-8')
(OUT / 'career.json').write_text(json.dumps(make_articles(CAREER, career_tools, 'job seekers', career_workflow, career_faq), ensure_ascii=False, indent=2), encoding='utf-8')
print('generated', len(CODING), len(CAREER))
