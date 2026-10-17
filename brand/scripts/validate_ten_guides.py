from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from PIL import Image
import json, zipfile

R=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
    def __init__(self,s):
        super().__init__();self.refs=[];self.ids=set();self.images=[];self.feed(s)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if tag=='img':self.images.append(a)

manifest=json.loads((R/'ten-directions/manifest.json').read_text())
routes=manifest['routes'];errors=[];refs=0;images=0
assert len(routes)==10 and len({c['slug'] for c in routes})==10
assert len(manifest['files'])==20
assert sorted(c['n'] for c in routes)==list(range(1,11))
guides=[f'brand-concept-{c["n"]:02}-{c["slug"]}.html' for c in routes]
pages=['brand-review.html','brand-audit.html']+guides
for name in pages:
    p=R/name;doc=Doc(p.read_text())
    for ref in doc.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=p.parent/unquote(u.path) if u.path else p;refs+=1
        if not target.is_file():errors.append(f'{name}: missing {ref}');continue
        if u.fragment and target.suffix=='.html' and unquote(u.fragment) not in Doc(target.read_text()).ids:errors.append(f'{name}: missing anchor {ref}')
    for a in doc.images:
        if not a.get('alt'):errors.append(f'{name}: missing image description')
        with Image.open(p.parent/a['src']) as im:
            if (int(a['width']),int(a['height']))!=im.size:errors.append(f'{name}: wrong intrinsic dimensions')
            im.verify();images+=1
    if 'Dum E Biryani Odisha' in p.read_text():errors.append(f'{name}: incorrect brand name')
for c in routes:
    if len(c['palette'])<3:errors.append(f'{c["slug"]}: missing palette')
    for key in ['meaning','grammar','type','boundary']:
        if not c.get(key):errors.append(f'{c["slug"]}: missing {key}')
for f in manifest['files']:
    with Image.open(R/'ten-directions'/f['file']) as im:
        if im.format!=f['format'] or im.size!=(f['width'],f['height']):errors.append(f['file']+': manifest mismatch')
with zipfile.ZipFile(R/'ten-directions/dum-e-odisha-ten-brand-guides.zip') as z:
    if z.testzip():errors.append('Corrupt ZIP')
    names=set(z.namelist());zrefs=0
    for name in pages:
        doc=Doc(z.read(name).decode())
        for ref in doc.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            target=str(PurePosixPath(name).parent/unquote(u.path)) if u.path else name;zrefs+=1
            if target not in names:errors.append(f'Offline {name}: missing {target}')
            elif u.fragment and target.endswith('.html') and u.fragment not in Doc(z.read(target).decode()).ids:errors.append(f'Offline anchor {name}: {ref}')
report={'revision':'08','concept_count':10,'individual_guides':guides,'logo_count':10,'packaging_mockups':10,'new_routes':7,'retained_routes':3,'local_references_checked':refs,'images_verified':images,'offline_package_references_checked':zrefs,'errors':errors,'visual_review':'All seven new logo and packaging pairs reviewed, alongside three retained pairs from revision 07.','browser_render_checked':False,'geometry_status':'Golden-ratio-inspired; exact phi construction not verified.'}
(R/'docs/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
