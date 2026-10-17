from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from PIL import Image
import json, zipfile, xml.etree.ElementTree as ET

R=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
    def __init__(self,s):
        super().__init__();self.refs=[];self.ids=set();self.images=[];self.feed(s)
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ['href','src']:
            if k in a:self.refs.append(a[k])
        if t=='img':self.images.append(a)

pages=['brand-review.html','brand-audit.html','brand-history.html','brand-shared-handi.html','brand-garden-handi.html','brand-dum-host.html']
errors=[];refs=0;images=0
for name in pages:
    p=R/name;doc=Doc(p.read_text())
    for ref in doc.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=p.parent/unquote(u.path) if u.path else p;refs+=1
        if not target.is_file():errors.append(f'{name}: missing {ref}');continue
        if u.fragment and target.suffix=='.html' and unquote(u.fragment) not in Doc(target.read_text()).ids:errors.append(f'{name}: missing anchor {ref}')
    for a in doc.images:
        target=p.parent/a['src']
        if not a.get('alt'):errors.append(f'{name}: missing alt')
        if target.suffix=='.svg':ET.parse(target)
        else:
            with Image.open(target) as im:
                if name!='brand-history.html' and (int(a['width']),int(a['height']))!=im.size:errors.append(f'{name}: image dimensions')
                im.verify()
        images+=1
identity=json.loads((R/'docs/identity.json').read_text())
manifest=json.loads((R/'illustrative-concepts/manifest.json').read_text())
assert identity['revision']==manifest['revision']=='07'
with zipfile.ZipFile(R/'illustrative-concepts/dum-e-odisha-illustrative-concepts.zip') as z:
    if z.testzip():errors.append('ZIP corruption')
    package=z.namelist()
report={'revision':'07','pages_checked':pages,'local_references_checked':refs,'images_verified':images,'package_files':package,'errors':errors,'browser_render_checked':False,'visual_checks':'All three logo illustrations and packaging mockups reviewed for spelling, DUM/E gap, symbol and palette consistency.','delivery':'Concept studies, no final route selected; raster with opaque backgrounds.'}
(R/'docs/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
