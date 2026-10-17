from pathlib import Path
from PIL import Image
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'applications-complete'
for c in json.loads((R/'ten-directions/manifest.json').read_text())['routes'][:9]:
    kinds=['packaging-detail','wall','banner'];paths={k:next((D/f'{c["slug"]}-{k}{e}' for e in ['.jpg','.png'] if (D/f'{c["slug"]}-{k}{e}').exists()),None) for k in kinds}
    if not all(paths.values()):continue
    p=R/f'brand-concept-{c["n"]:02}-{c["slug"]}.html'; backup=p.with_name(p.stem+'-round09.html')
    if not backup.exists():shutil.copy2(p,backup)
    s=backup.read_text();sections=''
    for k in kinds:
        q=paths[k];im=Image.open(q);im.verify();w,h=im.size
        title={'packaging-detail':'The sharing-meal box','wall':'The restaurant wall','banner':'A banner in context'}[k]
        sections+=f'<section id="{k}"><h2>{title}</h2><img src="{q.relative_to(R)}" alt="{c["title"]} {k} mockup" width="{w}" height="{h}" loading="lazy"><p class="small">Nano Banana application concept; materials, venue and dimensions are illustrative.</p></section>'
    s=s.replace('<section id="system">',sections+'<section id="system">',1).replace('<a href="#packaging">Packaging</a>','<a href="#packaging">Packaging</a><a href="#packaging-detail">Meal box</a><a href="#wall">Wall</a><a href="#banner">Banner</a>',1)
    p.write_text(s)
print('Installed reviewed application scenes in guides 01–09.')
