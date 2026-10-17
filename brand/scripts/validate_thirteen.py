from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from PIL import Image
import json, zipfile
R=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
    def __init__(self,s):
        super().__init__();self.refs=[];self.ids=set();self.images=[];self.cards=[];self.feed(s)
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if t=='img':self.images.append(a)
        if 'data-group' in a:self.cards.append(a)
old=json.loads((R/'ten-directions/manifest.json').read_text())
m=json.loads((R/'expanded-directions/manifest.json').read_text())
routes=old['routes']+m['added_routes']
assert len(routes)==13 and sorted(c['n'] for c in routes)==list(range(1,14))
assert len(m['files'])==32
pages=['brand-review.html','brand-audit.html']+[f'brand-concept-{c["n"]:02}-{c["slug"]}.html' for c in routes]
errors=[];refs=0;images=0
main=Doc((R/'brand-review.html').read_text())
if len(main.cards)!=13:errors.append('Collection card count is not 13')
if sum(x.get('data-added')=='true' for x in main.cards)!=3:errors.append('New filter count is not 3')
for name in pages:
    p=R/name;d=Doc(p.read_text())
    for ref in d.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=p.parent/unquote(u.path) if u.path else p;refs+=1
        if not target.is_file():errors.append(name+': missing '+ref);continue
        if u.fragment and target.suffix=='.html' and unquote(u.fragment) not in Doc(target.read_text()).ids:errors.append(name+': missing anchor '+ref)
    for a in d.images:
        if not a.get('alt'):errors.append(name+': missing alt')
        with Image.open(p.parent/a['src']) as im:
            if (int(a['width']),int(a['height']))!=im.size:errors.append(name+': wrong dimensions')
            im.verify();images+=1
for f in m['files']:
    with Image.open(R/f['path']) as im:
        if im.size!=(f['width'],f['height']) or im.format!=f['format']:errors.append('Asset manifest mismatch: '+f['path'])
with zipfile.ZipFile(R/'expanded-directions/dum-e-odisha-thirteen-guides.zip') as z:
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
report={'revision':'09','concepts':13,'logos':13,'packaging_mockups':13,'wall_mockups':3,'banner_mockups':3,'local_references_checked':refs,'image_instances_verified':images,'offline_references_checked':offline,'errors':errors,'visual_review':'Three corrected logos and nine application scenes inspected for spelling, Dum/E separation, brand continuity and visible mockup quality.','browser_render_checked':False}
(R/'docs/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
