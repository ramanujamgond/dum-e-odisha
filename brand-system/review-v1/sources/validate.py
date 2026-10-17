from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
class Doc(HTMLParser):
 def __init__(self,s):super().__init__();self.refs=[];self.ids=set();self.images=[];self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('src','href'):
   if k in a:self.refs.append(a[k])
  if t=='img':self.images.append(a)
def links(p):
 errors=[];d=Doc(p.read_text())
 for ref in d.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  q=(p.parent/unquote(u.path)).resolve() if u.path else p
  if not q.is_file():errors.append(f'{p.name}: missing {ref}')
  elif u.fragment and q.suffix=='.html' and u.fragment not in Doc(q.read_text()).ids:errors.append(f'{p.name}: missing anchor {ref}')
 for im in d.images:
  if not im.get('alt'):errors.append(f'{p.name}: missing alt')
 return len(d.refs),errors
def lum(c):
 v=[int(c[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
 return sum(a*b for a,b in zip(v,(.2126,.7152,.0722)))
colors={'chilli':'#852D26','cream':'#FFF6E7','saffron':'#E8A535','ink':'#29231F'}
ratios={f'{a}/{b}':round((max(lum(colors[a]),lum(colors[b]))+.05)/(min(lum(colors[a]),lum(colors[b]))+.05),2) for a,b in [('chilli','cream'),('ink','cream'),('ink','saffron'),('saffron','cream')]}
errors=[];refs=0
for p in [R/'index.html',R.parents[1]/'index.html']:
 n,e=links(p);refs+=n;errors+=e
svgs=list(R.rglob('*.svg'))
for p in svgs:
 root=ET.parse(p).getroot()
 if any(x.tag.endswith('image') for x in root.iter()):errors.append(f'embedded raster in {p}')
 if p.parent.name=='logo' and any(x.tag.endswith('text') for x in root.iter()):errors.append(f'font dependency in logo {p}')
manifest=R/'manifest.json'
if manifest.exists():
 for f in json.loads(manifest.read_text())['files']:
  p=R/f['path']
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:errors.append('checksum mismatch '+f['path'])
print(json.dumps({'local_references':refs,'svg_files':len(svgs),'contrast_ratios':ratios,'errors':errors},indent=2))
raise SystemExit(bool(errors))
