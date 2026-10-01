from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(r'C:\Users\syush\.codex\worktrees\1ea4\廣告收入設定\sites')

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        for key in ('href','src'):
            if values.get(key): self.links.append(values[key])

broken=[]; checked=0
for source in ROOT.rglob('*.html'):
    parser=Links(); parser.feed(source.read_text(encoding='utf-8'))
    for raw in parser.links:
        parsed=urlparse(raw)
        if parsed.scheme or raw.startswith(('#','mailto:','tel:','data:')): continue
        target=(source.parent / parsed.path).resolve()
        if target.is_dir(): target=target/'index.html'
        checked+=1
        if not target.exists(): broken.append((source.relative_to(ROOT),raw,target))
print(f'checked={checked} broken={len(broken)} sites={len([p for p in ROOT.iterdir() if p.is_dir()])}')
for row in broken[:100]: print(row)
if broken: raise SystemExit(1)
