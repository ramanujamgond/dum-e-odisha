"""Build static, file://-friendly reading pages from the kit's source documents.

Supports the small Markdown subset used here; no network or third-party runtime.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit, unquote
import os
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
GROUPS = {
    'The identity': ['brand-guidelines', 'logo-system', 'visual-system', 'verbal-system', 'imagery-brief', 'localization-kit'],
    'Make & apply': ['application-kit', 'packaging-spec'],
    'Research & direction': ['public-research', 'strategy', 'creative-territories', 'brief', 'evidence-ledger'],
    'Project & handover': ['project-context', 'validation-report', 'handover-manifest', 'decision-log', 'project-overview'],
}
LABELS = {
    'localization-kit': 'Odia & Hindi explorations',
    'brand-guidelines': 'Brand guidelines', 'logo-system': 'Logo & usage',
    'visual-system': 'Colour & typography', 'verbal-system': 'Voice & copy',
    'imagery-brief': 'Illustration & provenance', 'application-kit': 'Editable applications',
    'packaging-spec': 'Packaging handoff', 'public-research': 'Public research',
    'strategy': 'Brand strategy', 'creative-territories': 'Creative directions',
    'brief': 'The brief', 'evidence-ledger': 'Evidence ledger',
    'project-context': 'Toolkit plan', 'validation-report': 'Checks & visual review',
    'handover-manifest': 'Handover', 'decision-log': 'Decisions & next steps',
    'project-overview': 'Project overview',
}
SOURCES = {p: p.with_suffix('.html') for p in (ROOT/'docs').glob('*.md')}
SOURCES[PROJECT/'README.md'] = ROOT/'docs/project-overview.html'


def href(value, source, output):
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        return value
    target = (source.parent / unquote(url.path)).resolve()
    destination = SOURCES.get(target, target)
    result = os.path.relpath(destination, output.parent)
    return result + ('#' + url.fragment if url.fragment else '')


def inline(value, source, output):
    # Protect links and code before applying emphasis, so markup cannot be injected.
    tokens = []
    def save(text):
        tokens.append(text)
        return f'\x00{len(tokens)-1}\x00'
    value = re.sub(r'`([^`]+)`', lambda m: save('<code>'+escape(m[1])+'</code>'), value)
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: save('<a href="'+escape(href(m[2],source,output),quote=True)+'">'+escape(m[1])+'</a>'), value)
    value = escape(value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', value)
    return re.sub(r'\x00(\d+)\x00', lambda m: tokens[int(m[1])], value)


def render(source, output):
    lines = source.read_text().splitlines()
    blocks, toc, ids = [], [], {}
    title = LABELS[output.stem]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line.startswith('```'):
            code = []; i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i]); i += 1
            blocks.append('<pre><code>'+escape('\n'.join(code))+'</code></pre>')
            i += 1; continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading:
            level, text = len(heading[1]), heading[2]
            if level == 1:
                title = text; i += 1; continue
            slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'section'
            ids[slug] = ids.get(slug, 0)+1
            if ids[slug] > 1: slug += '-'+str(ids[slug])
            blocks.append(f'<h{level} id="{slug}">'+inline(text,source,output)+f'</h{level}>')
            toc.append((slug,text)); i += 1; continue
        if i+1 < len(lines) and line.startswith('|') and re.match(r'^\s*\|[\s:|\-]+\|\s*$', lines[i+1]):
            rows = []
            def cells(row):
                return [x.strip() for x in row.strip().strip('|').split('|')]
            head = cells(line); i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(cells(lines[i])); i += 1
            table = '<div class="table-scroll" role="region" aria-label="'+escape(title,quote=True)+' table" tabindex="0"><table><thead><tr>'
            table += ''.join('<th scope="col">'+inline(x,source,output)+'</th>' for x in head)
            table += '</tr></thead><tbody>'
            for row in rows:
                table += '<tr>'+''.join('<td>'+inline(x,source,output)+'</td>' for x in row)+'</tr>'
            blocks.append(table+'</tbody></table></div>'); continue
        if re.match(r'^(?:[-*]|\d+\.)\s+',line):
            ordered = bool(re.match(r'^\d+\.',line)); tag = 'ol' if ordered else 'ul'; items=[]
            pattern = r'^\d+\.\s+' if ordered else r'^[-*]\s+'
            while i < len(lines) and re.match(pattern,lines[i].strip()):
                items.append(re.sub(pattern,'',lines[i].strip())); i += 1
            blocks.append('<'+tag+'>'+''.join('<li>'+inline(x,source,output)+'</li>' for x in items)+'</'+tag+'>'); continue
        paragraph = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||```|[-*]\s|\d+\.\s)',lines[i].strip()):
            paragraph.append(lines[i].strip()); i += 1
        blocks.append('<p>'+inline(' '.join(paragraph),source,output)+'</p>')
    return title, '\n'.join(blocks), toc


def sidebar(current):
    sections=[]
    for label, slugs in GROUPS.items():
        links=''.join(f'<a href="{slug}.html"'+(' aria-current="page"' if current==slug else '')+'>'+LABELS[slug]+'</a>' for slug in slugs)
        sections.append('<div class="nav-group"><h2>'+label+'</h2>'+links+'</div>')
    return '<nav class="doc-nav" aria-label="Brand library">'+''.join(sections)+'</nav>'


def shell(title, body, slug, toc=()):
    contents = ''
    if toc:
        contents='<nav class="contents" aria-label="On this page"><span>On this page</span>'+''.join('<a href="#'+key+'">'+escape(label)+'</a>' for key,label in toc)+'</nav>'
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+escape(title)+''' — Dum E Odisha</title><link rel="icon" href="../assets/logo/favicon.png"><link rel="stylesheet" href="../assets/documents.css"></head><body><a class="skip" href="#article">Skip to document</a><header class="document-header"><a class="brand" href="../index.html"><img src="../assets/logo/avatar.png" width="40" height="40" alt="">DUM E ODISHA</a><a href="../index.html#files">Back to the brand guide ↗</a></header><div class="reading-layout"><aside><a class="library-link" href="index.html">The brand library</a>'''+sidebar(slug)+'''</aside><main id="article"><div class="document-intro"><p class="eyebrow">The brand library / Review 02</p><h1>'''+escape(title)+'''</h1><p class="document-meta">17 October 2026 <span aria-hidden="true">·</span> Working identity</p></div>'''+contents+'''<article>'''+body+'''</article><footer class="document-footer"><a href="index.html">Browse the library ←</a><a href="../index.html#files">Return to the kit ↗</a></footer></main></div></body></html>'''


for source, output in SOURCES.items():
    title, content, toc = render(source,output)
    output.write_text(shell(title,content,output.stem,toc))

cards=[]
for label, slugs in GROUPS.items():
    cards.append('<section class="library-section"><h2>'+label+'</h2><div class="library-grid">'+''.join('<a class="library-card" href="'+slug+'.html"><span>'+LABELS[slug]+'</span><span aria-hidden="true">↗</span></a>' for slug in slugs)+'</div></section>')
(ROOT/'docs/index.html').write_text(shell('A home for the details.','<p class="lead">The identity, the thinking behind it, and the practical details—all in one place.</p>'+''.join(cards),'index'))
print(f'Built {len(SOURCES)} reading pages and the brand library index.')
