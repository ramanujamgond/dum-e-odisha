"""Validate delivered references, canonical data, contrast, archive and checksums."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, re, sys

R=Path(__file__).resolve().parents[1]
PROJECT=R.parents[1]
errors=[]
class Doc(HTMLParser):
    def __init__(self,p):
        super().__init__();self.refs=[];self.ids=set();self.images=[];self.feed(p.read_text())
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ['src','href']:
            if key in a:self.refs.append(a[key])
        if t=='img':self.images.append(a)

refs=0
for p in [PROJECT/'index.html',*R.rglob('*.html')]:
    d=Doc(p)
    for im in d.images:
        if 'alt' not in im:errors.append(f'Missing alt: {p}')
    for ref in d.refs:
        u=urlsplit(ref)
        if not u.scheme and u.path.endswith('.md'):errors.append(f'Markdown exposed instead of reading page: {p.relative_to(PROJECT)} → {ref}')
        if u.scheme or u.netloc:continue
        refs+=1
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if not target.is_file():errors.append(f'Missing reference: {p.relative_to(PROJECT)} → {ref}')
        elif u.fragment and target.suffix=='.html' and u.fragment not in Doc(target).ids:errors.append(f'Missing anchor: {ref}')
for p in (R/'assets').glob('*.css'):
    for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',p.read_text()):
        if not ref.startswith('data:') and not (p.parent/ref).is_file():errors.append(f'Missing CSS asset: {ref}')
for p in R.rglob('*.json'):
    try:json.loads(p.read_text())
    except ValueError as exc:errors.append(f'Invalid JSON {p}: {exc}')
data=json.loads((R/'data/business-profile.json').read_text())
if data['name']!='Dum E Odisha' or data['instagram']['url']!='https://www.instagram.com/dum_e_odisha/':errors.append('Canonical owner data mismatch')
if data['phone']!='+917894265632' or data['city']!='Bhubaneswar' or not data['instagram']['profileContentVerified']:errors.append('First-party observed contact data mismatch')
for key in ['whatsapp','email','openingHours','orderingUrl','foodLicense']:
    if data[key] is not None:errors.append('Unverified operational field populated: '+key)
if data['menu']:errors.append('Unverified menu promoted')

def lum(c):
    v=[int(c[i:i+2],16)/255 for i in (1,3,5)]
    v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(x*y for x,y in zip(v,[.2126,.7152,.0722]))
colors={'chilli':'#852D26','cream':'#FFF6E7','saffron':'#E8A535','ink':'#29231F','leaf':'#4E5940','muted':'#69594A'}
ratios={}
for a,b in [('chilli','cream'),('ink','cream'),('ink','saffron'),('leaf','cream'),('muted','cream'),('saffron','cream')]:
    x,y=sorted([lum(colors[a]),lum(colors[b])]);ratios[a+'/'+b]=round((y+.05)/(x+.05),2)
for pair,val in ratios.items():
    if pair!='saffron/cream' and val<4.5:errors.append('Text contrast failed '+pair)

inventory=json.loads((PROJECT/'operations/relocation-verification.json').read_text())['sha256_manifest']
# The relocation snapshot includes Git internals. Commits, branch changes and
# configuring origin legitimately mutate these; preserve-check project files.
git_metadata=[rel for rel in inventory if rel=='.git' or rel.startswith('.git/')]
archive_inventory={rel:digest for rel,digest in inventory.items() if rel not in git_metadata}
archive_errors=[]
for rel,digest in archive_inventory.items():
    p=PROJECT/rel
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:archive_errors.append(rel)
if archive_errors:errors.append(f'Original archive changed: {archive_errors}')
original_v1=json.loads((PROJECT/'brand-system/review-v1/manifest.json').read_text())
for item in original_v1['files']:
    p=PROJECT/'brand-system/review-v1'/item['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:errors.append('Review 01 changed: '+item['path'])

manifest=R/'manifest.json'
def files():
    return [{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(R.rglob('*')) if p.is_file() and p!=manifest and p.name!='validation.json']
if '--refresh-manifest' in sys.argv:
    manifest.write_text(json.dumps({'brand':'Dum E Odisha','version':'review-02','status':'owner_review_pending','date':'2026-10-17','files':files()},indent=2)+'\n')
elif not manifest.exists():errors.append('Manifest missing; generate after finishing artifacts')
else:
    if json.loads(manifest.read_text())['files']!=files():errors.append('Review 02 manifest differs from current files')
report={'checkedAt':'2026-10-17','localReferences':refs,'contrastRatios':ratios,'preservedOriginalsChecked':len(archive_inventory),'relocationGitMetadataExcluded':len(git_metadata),'originalArchiveChanges':archive_errors,'review01ManifestFilesChecked':len(original_v1['files']),'errors':errors}
(R/'proofs/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
sys.exit(bool(errors))
