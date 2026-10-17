from pathlib import Path
from PIL import Image
import json,re,zipfile,shutil
R=Path(__file__).resolve().parents[1];D=R/'applications-complete'
old=json.loads((R/'ten-directions/manifest.json').read_text()); expanded=json.loads((R/'expanded-directions/manifest.json').read_text());routes=old['routes']+expanded['added_routes']
for p in D.glob('*.png'):
    if Image.open(p).format=='JPEG':p.rename(p.with_suffix('.jpg'))
def url(c):return f'brand-concept-{c["n"]:02}-{c["slug"]}.html'
def title(c):return c.get('title',c.get('name'))
def asset(c,kind):
    folder=D if c['n']<=10 else R/'expanded-directions'
    for ext in ['.jpg','.png']:
        p=folder/f'{c["slug"]}-{kind}{ext}'
        if p.exists():return p
    raise FileNotFoundError(c['slug']+' '+kind)
def pic(p,alt):
    w,h=Image.open(p).size
    return f'<img src="{p.relative_to(R)}" alt="{alt}" width="{w}" height="{h}" loading="lazy">'
css=re.search(r'<style>(.*?)</style>',(R/'brand-review-round09.html').read_text(),re.S).group(1)
css+=' .application-catalogue{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}.application-catalogue h2{font-size:26px}.appgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}@media(max-width:750px){.application-catalogue,.appgrid{grid-template-columns:1fr}}'
def page(name,body,js=''):return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title><style>{css}</style></head><body><main>{body}</main>{js}</body></html>'
applications=[];guides=[];snapshot=(R/'brand-review-round09.html').read_text()
for c in routes:
    p=R/url(c);guides.append(p.name);backup=p.with_name(p.stem+'-round09.html')
    if not backup.exists():shutil.copy2(p,backup)
    snapshot=snapshot.replace(p.name,backup.name);text=backup.read_text()
    if c['n']<=10:
        body=''
        for kind,label,description in [('packaging-detail','The sharing-meal box','A second packaging application explores a rectangular meal box, supporting container and branded wrap.'),('wall','A wall with its own story','The original logo anchors a quiet field while larger illustration extends the identity around it.'),('banner','A banner that reads clearly','The full name leads, supported by the tagline and a separate category label.')]:
            q=asset(c,kind)
            body+=f'<section id="{kind}"><div class="eyebrow">Additional application</div><h2>{label}</h2><p>{description}</p><figure>{pic(q,title(c)+" "+kind+" concept")}<figcaption>Nano Banana concept mockup. Venue, materials, food appearance and dimensions are illustrative, not final production specifications.</figcaption></figure><p><a href="{q.relative_to(R)}" download>Download this mockup</a></p></section>'
        text=text.replace('<section id="system">',body+'<section id="system">',1).replace('<a href="#packaging">Packaging</a>','<a href="#packaging">Packaging</a><a href="#packaging-detail">Meal box</a><a href="#wall">Wall</a><a href="#banner">Banner</a>',1).replace('Revision 09','Revision 10')
    text=text.replace('<nav>','<nav><a href="brand-applications.html">All mockups</a>',1);p.write_text(text)
    if c['n']<=10:
        applications.append({'n':c['n'],'slug':c['slug'],'title':title(c),'kind':'packaging','label':'Takeaway family','path':f'ten-directions/{c["slug"]}-mockup.jpg','anchor':'packaging'})
        kinds=['packaging-detail','wall','banner']
    else:kinds=['packaging','wall','banner']
    for kind in kinds:applications.append({'n':c['n'],'slug':c['slug'],'title':title(c),'kind':'packaging' if kind=='packaging-detail' else kind,'label':{'packaging-detail':'Sharing-meal box','packaging':'Takeaway family','wall':'Feature wall','banner':'Promotional banner'}[kind],'path':str(asset(c,kind).relative_to(R)),'anchor':kind})
(R/'brand-review-round09.html').write_text(snapshot)
assert len(applications)==49
cards=''
for a in applications:
    hidden='' if a['kind']=='wall' else ' hidden'
    cards+=f'<article data-kind="{a["kind"]}"{hidden}><a href="{url(a)}#{a["anchor"]}">{pic(R/a["path"],a["title"]+" — "+a["label"])}</a><p class="eyebrow">{a["n"]:02} / {a["label"]}</p><h2>{a["title"]}</h2><p><a href="{url(a)}#{a["anchor"]}">Open brand guide →</a> · <a href="{a["path"]}" download>Download image</a></p></article>'
body='<nav><a href="brand-review.html">← All 13 identities</a><a href="brand-history.html">Earlier versions</a></nav><header><div class="eyebrow">Dum E Odisha / Application gallery / Revision 10</div><h1>One identity.<br>Every surface.</h1><p class="lead">All 13 concepts now have a wall design, a banner and takeaway packaging. The first ten also include a second sharing-meal packaging scene.</p><p>Compare 13 walls, 13 banners and 23 packaging scenes. Each is a separate identity route; keep its logo, palette and illustration language together.</p></header><div class="filters" aria-label="Application type"><button data-filter="wall" aria-pressed="true">Walls · 13</button><button data-filter="banner" aria-pressed="false">Banners · 13</button><button data-filter="packaging" aria-pressed="false">Packaging · 23</button><button data-filter="all" aria-pressed="false">All · 49</button></div><p id="application-count" class="small" aria-live="polite">Showing 13 wall mockups</p><div class="application-catalogue">'+cards+'</div><section><h2>Concepts, ready to compare.</h2><p>All new artwork was created with Nano Banana MCP. These scenes are illustrative applications, not photographs of an existing restaurant or confirmed manufacturing specifications.</p><a class="button" href="applications-complete/dum-e-odisha-complete-brand-guides.zip" download>Download all guides and mockups</a></section>'
js="""<script>document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{const f=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));let n=0;document.querySelectorAll('[data-kind]').forEach(c=>{c.hidden=f!=='all'&&c.dataset.kind!==f;if(!c.hidden)n++});document.getElementById('application-count').textContent='Showing '+n+' '+(f==='all'?'application':f)+' mockups';}));</script>"""
(R/'brand-applications.html').write_text(page('Dum E Odisha — Walls, banners and packaging',body,js))
main=(R/'brand-review-round09.html').read_text()
for c in routes:main=main.replace(url(c).replace('.html','-round09.html'),url(c))
main=main.replace('Revision 09','Revision 10').replace('Three earlier reference directions now join the existing ten identities, each with packaging, wall-design and banner mockups.','All thirteen identities now include packaging, wall-design and banner mockups. The first ten also include a second sharing-meal packaging scene.').replace('expanded-directions/dum-e-odisha-thirteen-guides.zip','applications-complete/dum-e-odisha-complete-brand-guides.zip').replace('<a href="#new-applications">Wall & banner mockups</a>','<a href="brand-applications.html">All 49 mockups</a>')
wallcards=''.join(f'<article><a href="{url(c)}#wall">{pic(asset(c,"wall"),title(c)+" wall design")}</a><h3>{c["n"]:02} · {title(c)}</h3><p><a href="{url(c)}#packaging">Packaging</a> · <a href="{url(c)}#wall">Wall</a> · <a href="{url(c)}#banner">Banner</a></p></article>' for c in routes)
section='<section id="new-applications"><div class="eyebrow">All 13 identities / Complete application collection</div><h2>Every concept, in context.</h2><p>Explore each direction as a feature wall, a banner and takeaway packaging. Ten additional sharing-meal boxes extend the first ten routes.</p><p><a class="button" href="brand-applications.html">Compare all 49 mockups →</a></p><div class="appgrid">'+wallcards+'</div></section>'
main=re.sub(r'<section id="new-applications">.*?</section>',section,main,count=1,flags=re.S).replace('brand-review-round08.html">Previous ten-concept collection','brand-review-round09.html">Previous collection and applications')
(R/'brand-review.html').write_text(main)
audit=(R/'brand-audit-round09.html').read_text().replace('Research / Revision 09','Research / Revision 10')
note='<section><h2>Applications completed for every route.</h2><p>Revision 10 adds walls, banners and sharing-meal boxes to each of the first ten identities. The full collection now has 13 wall scenes, 13 banners and 23 packaging scenes.</p><p><a href="brand-applications.html">Compare all applications</a> · <a href="applications-complete/generation-briefs.json">New generation briefs</a></p><p>Source logos remain the references. All scenes are concepts; production artwork and real material proofs are a separate stage.</p></section>'
audit=audit.replace('<section><h2>What stays consistent</h2>',note+'<section><h2>What stays consistent</h2>',1);(R/'brand-audit.html').write_text(audit)
h=R/'brand-history.html';s=h.read_text()
if 'id="round09"' not in s:
    s=s.replace('<section id="round08">','<section id="round09"><h2>Revision 09 — first wall and banner examples</h2><p>The earlier collection had application sets for concepts 11–13. Revision 10 extends walls and banners to every identity.</p><a href="brand-review-round09.html">Open the earlier collection</a></section><section id="round08">',1);h.write_text(s)
manifest={'brand_name':'Dum E Odisha','revision':'10','status':'13 alternative concepts; no final route selected','concepts':13,'logo_count':13,'packaging_mockups':23,'wall_mockups':13,'banner_mockups':13,'new_images':30,'applications':applications,'files':expanded['files'].copy()}
for c in old['routes']:
    for kind in ['wall','banner','packaging-detail']:
        p=asset(c,kind);im=Image.open(p);im.verify();manifest['files'].append({'file':p.name,'path':str(p.relative_to(R)),'width':im.width,'height':im.height,'format':im.format})
assert len(manifest['files'])==62
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'docs/identity.json').write_text(json.dumps({'brand_name':'Dum E Odisha','revision':'10','status':manifest['status'],'tagline':'Flavour in Every Layer.','concept_manifest':'applications-complete/manifest.json','previous_identity':'docs/identity-round09.json','guide':'brand-review.html','applications':'brand-applications.html'},indent=2)+'\n')
pages=['brand-review.html','brand-audit.html','brand-applications.html']+guides
with zipfile.ZipFile(D/'dum-e-odisha-complete-brand-guides.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in manifest['files']:z.write(R/f['path'],f['path'])
    for p in [D/'manifest.json',D/'generation-briefs.json',R/'expanded-directions/briefs.json']:z.write(p,str(p.relative_to(R)))
    for n in ['ten-directions-research.md','illustrative-directions-research.md','ten-logo-briefs.json','ten-mockup-briefs.json','addition-mockup-briefs.json']:z.write(R/'research'/n,'research/'+n)
    for c in expanded['added_routes']:z.write(R/f'concepts/{c["source"]}.png',f'concepts/{c["source"]}.png')
    for name in pages:
        text=(R/name).read_text();text=re.sub(r'<a\b[^>]*href="brand-(?:history|review-round0[789]|audit-round07)\.html"[^>]*>.*?</a>','',text,flags=re.S);text=re.sub(r'<a\b[^>]*href="applications-complete/dum-e-odisha-complete-brand-guides\.zip"[^>]*>.*?</a>','',text,flags=re.S);z.writestr(name,text)
    z.writestr('README.txt','DUM E ODISHA — Complete application collection\nOpen brand-review.html for 13 guides, or brand-applications.html to compare mockups.\n13 logos; 13 wall scenes; 13 banners; 23 packaging scenes.\nAll new visual artwork generated through Nano Banana MCP.\nRaster concepts, not vector masters, fabrication specifications or press artwork.\nEarlier source artwork retains historical naming only as a reference. Use the corrected logos for new work.\n')
print('Completed all 13 guides, 49-mockup gallery and offline package.')
