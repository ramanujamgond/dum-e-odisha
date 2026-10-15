from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, zipfile
from PIL import Image
import xml.etree.ElementTree as ET

root=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.refs=[]; self.ids=set(); self.images=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ('src','href'):
            if key in a: self.refs.append(a[key])
        if tag=='img': self.images.append(a['src'])
errors=[]; refs=0; images=0
for name in ['brand-review.html','brand-audit.html','brand-history.html']:
    p=root/name; doc=Document(p.read_text())
    for ref in doc.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc: continue
        target=p.parent/unquote(u.path) if u.path else p
        refs+=1
        if not target.is_file(): errors.append(f'{name}: missing {ref}'); continue
        if u.fragment and target.suffix=='.html':
            if unquote(u.fragment) not in Document(target.read_text()).ids: errors.append(f'{name}: missing anchor {ref}')
    for ref in doc.images:
        target=p.parent/ref
        if target.suffix=='.svg': ET.parse(target)
        else:
            with Image.open(target) as im: im.verify()
        images+=1
current=(root/'brand-review.html').read_text()
for bad in ['src="selected/','src="dum-e-odisha/','Dum E Biryani Odisha']:
    if bad in current: errors.append(f'Superseded content in current guide: {bad}')
for p in [root/'docs/identity.json',root/'final-design/manifest.json',root/'research/final-design-prompts.json']:
    json.loads(p.read_text())
with zipfile.ZipFile(root/'final-design/dum-e-odisha-final-package.zip') as z:
    if z.testzip(): errors.append('ZIP corruption')
    package_files=z.namelist()
report={'revision':'06','local_references_checked':refs,'images_verified':images,'package_files':package_files,'errors':errors,'browser_render_checked':False,'browser_note':'Browser access previously blocked; no alternate observation attempted.','visual_review':['Colour name and word separation','Reverse E knockout','Hero and detail packaging spelling and hierarchy'],'excluded':'Black study has tinted tagline; retained only in process.'}
(root/'docs/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
