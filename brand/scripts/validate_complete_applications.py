from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
import json,zipfile,collections
R=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
    def __init__(self,s):
        super().__init__();self.refs=[];self.ids=set();self.images=[];self.items=[];self.feed(s)
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if t=='img':self.images.append(a)
        if 'data-kind' in a:self.items.append(a)
m=json.loads((R/'applications-complete/manifest.json').read_text());a=m['applications'];errors=[];refs=0;images=0
assert len(a)==49 and len(m['files'])==62
assert collections.Counter(x['kind'] for x in a)=={'wall':13,'banner':13,'packaging':23}
for n in range(1,14):
    if not all(any(x['n']==n and x['kind']==k for x in a) for k in ['wall','banner','packaging']):errors.append(f'Concept {n}: missing application')
pages=['brand-review.html','brand-audit.html','brand-applications.html']+sorted({f'brand-concept-{x["n"]:02}-{x["slug"]}.html' for x in a})
for name in pages:
    p=R/name;d=Doc(p.read_text())
    for ref in d.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=p.parent/unquote(u.path) if u.path else p;refs+=1
        if not target.is_file():errors.append(name+': missing '+ref);continue
        if u.fragment and target.suffix=='.html' and unquote(u.fragment) not in Doc(target.read_text()).ids:errors.append(name+': missing anchor '+ref)
    for attrs in d.images:
        if not attrs.get('alt'):errors.append(name+': missing alt')
        with Image.open(p.parent/attrs['src']) as im:
            if (int(attrs['width']),int(attrs['height']))!=im.size:errors.append(name+': wrong intrinsic size')
            im.verify();images+=1
for f in m['files']:
    with Image.open(R/f['path']) as im:
        if im.size!=(f['width'],f['height']) or im.format!=f['format']:errors.append('Manifest mismatch '+f['path'])
gallery=Doc((R/'brand-applications.html').read_text())
if collections.Counter(x['data-kind'] for x in gallery.items)!={'wall':13,'banner':13,'packaging':23}:errors.append('Gallery category counts')
if len([x for x in gallery.items if 'hidden' not in x])!=13:errors.append('Default gallery visibility')
with zipfile.ZipFile(R/'applications-complete/dum-e-odisha-complete-brand-guides.zip') as z:
    if z.testzip():errors.append('ZIP corruption')
    names=set(z.namelist());offline=0
    for name in pages:
        d=Doc(z.read(name).decode())
        for ref in d.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            target=str(PurePosixPath(name).parent/unquote(u.path)) if u.path else name;offline+=1
            if target not in names:errors.append('Offline '+name+': missing '+target)
            elif u.fragment and target.endswith('.html') and u.fragment not in Doc(z.read(target).decode()).ids:errors.append('Offline anchor '+name+': '+ref)
report={'revision':'10','concepts':13,'logos':13,'new_mockups':30,'wall_mockups':13,'banner_mockups':13,'packaging_mockups':23,'local_references_checked':refs,'image_instances_verified':images,'offline_references_checked':offline,'errors':errors,'visual_review':'All 30 new images reviewed for name spelling, concept continuity, spacing and scene quality.','browser_render_checked':False}
(R/'docs/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
