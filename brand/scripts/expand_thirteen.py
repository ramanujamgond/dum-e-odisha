from pathlib import Path
from PIL import Image
import re, json, html, zipfile, shutil

R=Path(__file__).resolve().parents[1];D=R/'expanded-directions'
for p in D.glob('*.png'):
    if Image.open(p).format=='JPEG':p.rename(p.with_suffix('.jpg'))
new=json.loads((D/'briefs.json').read_text())
old=json.loads((R/'ten-directions/manifest.json').read_text())
css=re.search(r'<style>(.*?)</style>',(R/'brand-review-round08.html').read_text(),re.S).group(1)
css+=' .appnav{display:flex;gap:20px;flex-wrap:wrap;margin:24px 0}.appgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.appgrid h3{font-size:18px}@media(max-width:750px){.appgrid{grid-template-columns:1fr}}'
def asset(c,kind):
    for suffix in ['.jpg','.png']:
        p=D/f'{c["slug"]}-{kind}{suffix}'
        if p.exists():return p
    raise FileNotFoundError(c['slug']+' '+kind)
def img(c,kind,alt):
    p=asset(c,kind);w,h=Image.open(p).size
    return f'<img src="expanded-directions/{p.name}" width="{w}" height="{h}" alt="{html.escape(alt)}" loading="lazy">'
def url(c):return f'brand-concept-{c["n"]:02}-{c["slug"]}.html'
def page(title,body):return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body><main>{body}</main></body></html>'
for c in new:
    palette=''.join(f'<article><div class="swatch" style="background:{color}"></div><strong>{name}</strong><br><code>{color}</code><p>{role}</p></article>' for name,color,role in c['palette'])
    applications=''
    for kind,title,description in [('packaging','Takeaway packaging','A carrier, container and supporting details apply this route to the meal.'),('wall','The restaurant wall','The mark anchors a larger illustrated interior. Extend the graphic language onto a feature wall while leaving space around the name.'),('banner','A banner in the street','A clear brand mark and tagline form a simple promotional hierarchy. The banner is an application concept, with no unconfirmed menu or price promises.')]:
        applications+=f'<section id="{kind}"><div class="eyebrow">Application / {kind}</div><h2>{title}</h2><p>{description}</p><figure>{img(c,kind,c["name"]+" "+kind+" mockup for Dum E Odisha")}<figcaption>Nano Banana visual concept. Venue, materials, dimensions and any food shown are illustrative.</figcaption></figure><p><a href="expanded-directions/{asset(c,kind).name}" download>Download this {kind} mockup</a></p></section>'
    b=f'''<nav><a href="brand-review.html">← All 13 concepts</a><a href="#packaging">Packaging</a><a href="#wall">Wall design</a><a href="#banner">Banner</a><a href="brand-history.html">History</a></nav><header><div class="eyebrow">Dum E Odisha / Concept {c['n']:02} of 13 / Added from your reference</div><h1>{c['name']}</h1><p class="lead">The original visual idea, refined for the correct brand name and a complete set of applications.</p></header><div class="grid"><figure>{img(c,'logo',c['name']+' corrected Dum E Odisha logo')}</figure><div><h2>The meaning in the mark.</h2><p>{c['meaning']}</p><p><strong>Name:</strong> Dum E Odisha<br><strong>Tagline:</strong> Flavour in Every Layer.</p><p>The earlier reference used Biryani as part of the logo. This addition keeps the correct full brand name and clear spacing between Dum and E. Biryani remains category copy outside the name.</p><p><a class="button" href="expanded-directions/{asset(c,'logo').name}" download>Download the updated logo</a></p><p class="small"><a href="concepts/{c['source']}.png">View the unchanged historical source</a></p></div></div><section><h2>Colour & typography.</h2><div class="palette">{palette}</div><p>Preserve the source’s warm expressive lettering; use a simple sans-serif for menu details, prices and supporting information. The logo is generated artwork, not a claim to an exact font family.</p><p class="small">Palette values are targets; generated raster tones vary. Exact inks need production artwork and physical proofs.</p></section><section><h2>A consistent visual language.</h2><p>{c['grammar']}</p><div class="panel"><h3>Working rules</h3><ul><li>Keep Dum and E separate and Odisha part of the full name.</li><li>Preserve the symbol, lettering proportions and palette together.</li><li>Leave at least a capital D height of clear space around the visible logo.</li><li>Use larger supporting graphics on separate panels; keep the name on a quiet field.</li><li>Use the tagline only where readable. Prepare a simplified small-format and one-ink master after selecting a route.</li></ul></div><nav class="appnav" aria-label="Applications"><a href="#packaging">Takeaway packaging ↓</a><a href="#wall">Feature wall ↓</a><a href="#banner">Banner ↓</a></nav></section>{applications}<section><h2>Delivery notes.</h2><p>These additions reinterpret your earlier Nano Banana concepts; they do not replace the ten existing routes. The original versions remain in history.</p><p>All new artwork and mockups were generated through Nano Banana MCP. High-resolution raster studies with opaque backgrounds; editable vector masters, fabrication dimensions, print separations and final production artwork are not included.</p></section><footer><a href="brand-review.html#new-applications">← Compare all 13 and see the new applications</a></footer>'''
    (R/url(c)).write_text(page('Dum E Odisha — '+c['name'],b))
# Preserve the previous ten-guide pages before updating their navigation.
snapshot=(R/'brand-review-round08.html').read_text()
old_pages=[]
for c in old['routes']:
    name=url(c);old_pages.append(name);p=R/name
    backup=p.with_name(p.stem+'-round08.html')
    if not backup.exists():shutil.copy2(p,backup)
    snapshot=snapshot.replace(name,backup.name)
    text=p.read_text().replace('All 10 concepts','All 13 concepts').replace('Back to all 10','Back to all 13').replace('of 10 / Revision 08','of 13 / Revision 09')
    if c['n']==10:
        text=text.replace('brand-concept-01-saura-harvest.html">Next: Harvest &amp; Hearth','brand-concept-11-aroma-paisley.html">Next: The Aroma Paisley').replace('brand-concept-01-saura-harvest.html">Next: Harvest & Hearth','brand-concept-11-aroma-paisley.html">Next: The Aroma Paisley')
    p.write_text(text)
(R/'brand-review-round08.html').write_text(snapshot)
main=(R/'brand-review-round08.html').read_text()
# Current collection links point to current guide pages, not snapshot copies.
for name in old_pages:main=main.replace(name.replace('.html','-round08.html'),name)
cards=''.join(f'<article data-group="modern" data-added="true"><a href="{url(c)}">{img(c,"logo",c["name"]+" newly added concept")}</a><p class="eyebrow">{c["n"]:02} / Reference addition</p><h2>{c["name"]}</h2><p>{c["meaning"]}</p><a class="button" href="{url(c)}">Open guide & three mockups →</a></article>' for c in new)
main=main.replace('</div></section><section id="compare">',cards+'</div></section><section id="compare">',1)
main=main.replace('Ten logos and brand guides','Thirteen logos and brand guides').replace('Ten stories.','Thirteen stories.').replace('10 distinct identities','13 distinct identities').replace('Ten concepts','Thirteen concepts').replace('ten different logos','thirteen different logos').replace('All 10</button>','All 13</button>').replace('Modern approaches · 4','Modern approaches · 7').replace('Showing all 10 concepts','Showing all 13 concepts').replace('Revision 08','Revision 09')
main=main.replace('Seven new directions join the three developed illustrated identities.','Three earlier reference directions now join the existing ten identities, each with packaging, wall-design and banner mockups.')
main=main.replace('ten-directions/dum-e-odisha-ten-brand-guides.zip','expanded-directions/dum-e-odisha-thirteen-guides.zip').replace('Download all 10 brand guides & assets','Download all 13 guides & assets')
main=main.replace('</div><p id="concept-count"','<button data-filter="added" aria-pressed="false">New reference additions · 3</button></div><p id="concept-count"',1)
main=main.replace("c.hidden=f!=='all'&&c.dataset.group!==f;","c.hidden=f==='added'?c.dataset.added!=='true':f!=='all'&&c.dataset.group!==f;")
rows=''.join(f'<tr><td>{c["n"]:02} · {c["name"]}</td><td>{c["meaning"]}</td></tr>' for c in new)
main=main.replace('</table><p>These are separate identity routes.',rows+'</table><p>These are separate identity routes.',1)
appcards=''.join(f'<article><a href="{url(c)}#wall">{img(c,"wall",c["name"]+" restaurant wall design")}</a><h3>{c["name"]}</h3><p><a href="{url(c)}#packaging">Packaging</a> · <a href="{url(c)}#wall">Wall</a> · <a href="{url(c)}#banner">Banner</a></p></article>' for c in new)
section='<section id="new-applications"><div class="eyebrow">Three additions / Nine new application scenes</div><h2>Beyond the logo.</h2><p>See each added direction across takeaway packaging, a restaurant feature wall and a freestanding banner. The same visual idea carries through each setting.</p><div class="appgrid">'+appcards+'</div></section>'
main=main.replace('<section id="compare">',section+'<section id="compare">',1)
main=main.replace('<a href="#compare">Compare the approaches</a>','<a href="#compare">Compare the approaches</a><a href="#new-applications">Wall & banner mockups</a>')
main=main.replace('</style>',css[css.index(' .appnav{'):]+'</style>',1)
main=main.replace('<a href="brand-review-round07.html">Previous three-concept collection</a>','<a href="brand-review-round08.html">Previous ten-concept collection</a>')
(R/'brand-review.html').write_text(main)
audit=(R/'brand-audit-round08.html').read_text().replace('Ten brand guides','Thirteen brand guides').replace('Explore all 10','Explore all 13').replace('Research / Revision 08','Research / Revision 09').replace('Research for ten identities','Research for thirteen identities')
addition='<section><h2>Three reference additions.</h2><p>Aroma Paisley, the original hands-and-handi direction (now called Generous Handi), and Dum Club have been added as concepts 11–13. Their source artworks are preserved, with the public name corrected to Dum E Odisha and clear Dum/E spacing.</p><p>Each addition has a packaging scene, a restaurant feature wall and a banner mockup. These are concept settings, not an existing venue or fabrication specification.</p><p><a href="expanded-directions/briefs.json">Logo briefs</a> · <a href="research/addition-mockup-briefs.json">Application briefs</a> · <a href="brand-review.html#new-applications">View applications</a></p></section>'
audit=audit.replace('<section><h2>What stays consistent</h2>',addition+'<section><h2>What stays consistent</h2>',1)
(R/'brand-audit.html').write_text(audit)
history=R/'brand-history.html';text=history.read_text()
if 'id="round08"' not in text:
    text=text.replace('<section id="round07">','<section id="round08"><h2>Revision 08 — the ten-concept collection</h2><p>The ten directions are retained unchanged as visual identities. Revision 09 adds three earlier reference directions and nine application scenes.</p><a href="brand-review-round08.html">Open the previous ten-guide collection</a></section><section id="round07">',1);history.write_text(text)
manifest={'brand_name':'Dum E Odisha','revision':'09','status':'13 alternative concepts; no final route selected','tagline':'Flavour in Every Layer.','previous_manifest':'ten-directions/manifest.json','added_routes':new,'total_concepts':13,'logo_count':13,'packaging_mockups':13,'wall_mockups':3,'banner_mockups':3,'files':[]}
for f in old['files']:manifest['files'].append(dict(f,path='ten-directions/'+f['file']))
for c in new:
    for kind in ['logo','packaging','wall','banner']:
        p=asset(c,kind);im=Image.open(p);im.verify()
        manifest['files'].append({'file':p.name,'path':'expanded-directions/'+p.name,'width':im.width,'height':im.height,'format':im.format})
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'docs/identity.json').write_text(json.dumps({'brand_name':'Dum E Odisha','revision':'09','status':manifest['status'],'tagline':manifest['tagline'],'concept_manifest':'expanded-directions/manifest.json','previous_identity':'docs/identity-round08.json','guide':'brand-review.html'},indent=2)+'\n')
pages=['brand-review.html','brand-audit.html']+old_pages+[url(c) for c in new]
with zipfile.ZipFile(D/'dum-e-odisha-thirteen-guides.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in manifest['files']:z.write(R/f['path'],f['path'])
    z.write(D/'manifest.json','expanded-directions/manifest.json')
    z.write(D/'briefs.json','expanded-directions/briefs.json')
    for name in ['ten-directions-research.md','illustrative-directions-research.md','ten-logo-briefs.json','ten-mockup-briefs.json','addition-mockup-briefs.json']:z.write(R/'research'/name,'research/'+name)
    for c in new:z.write(R/f'concepts/{c["source"]}.png',f'concepts/{c["source"]}.png')
    for name in pages:
        text=(R/name).read_text()
        text=re.sub(r'<a\b[^>]*href="brand-(?:history|review-round0[78]|audit-round07)\.html"[^>]*>.*?</a>','',text,flags=re.S)
        text=re.sub(r'<a\b[^>]*href="expanded-directions/dum-e-odisha-thirteen-guides\.zip"[^>]*>.*?</a>','',text,flags=re.S)
        z.writestr(name,text)
    z.writestr('README.txt','DUM E ODISHA — 13 identity concepts\nOpen brand-review.html for the collection.\n13 individual brand guides, 13 logos, 13 packaging mockups, 3 wall concepts and 3 banner scenes.\nAll new visuals created with Nano Banana MCP. Raster concepts, not vector masters or fabrication specifications.\nHistorical source artwork uses earlier naming and is supplied only for reference. Use corrected logo assets for new work.\n')
print('Built 13-guide collection, 9 new application scenes and complete offline package.')
