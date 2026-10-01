from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SITE = Path(r'C:\Users\syush\Documents\ChatGPT\廣告收入設定\site')

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for key in ('href', 'src'):
            if values.get(key):
                self.links.append(values[key])

broken = []
checked = 0
for source in SITE.rglob('*.html'):
    parser = Links()
    parser.feed(source.read_text(encoding='utf-8'))
    for raw in parser.links:
        parsed = urlparse(raw)
        if parsed.scheme or raw.startswith(('#', 'mailto:', 'tel:', 'data:')):
            continue
        target_text = parsed.path
        if not target_text:
            continue
        target = (source.parent / target_text).resolve() if not target_text.startswith('/') else (SITE / target_text.lstrip('/')).resolve()
        if target.is_dir():
            target = target / 'index.html'
        checked += 1
        if not target.exists():
            broken.append((source.relative_to(SITE), raw, target))

print(f'checked={checked} broken={len(broken)}')
for source, raw, target in broken:
    print(f'{source}: {raw} -> {target}')
if broken:
    raise SystemExit(1)
