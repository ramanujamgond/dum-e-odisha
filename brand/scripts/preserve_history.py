from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
old=(r/'brand-review-round02.html').read_text()
previous=(r/'brand-review-round03.html').read_text()
cards=re.findall(r'<article data-kind="[^"]+">.*?</article>',previous,re.S)
cards=[re.sub(r' data-kind="[^"]+"','',c) for c in cards]
archive='<section id="earlier-colourways"><h2>Earlier selected-logo colour treatments</h2><p>The five treatments below are preserved from the first selected-logo colour round, including the original chilli, black-and-saffron and green versions. The current guide explores more colour across the lid and lettering.</p><div class="grid">'+''.join(cards)+'</div></section>'
old=old.replace('<title>Dum E Biryani — Brand guide / six logo directions</title>','<title>Dum E Biryani — Brand and design history</title>')
old=old.replace('<main>','<main><nav class="history-nav" aria-label="Brand pages"><a href="brand-review.html">← Current multicolour brand guide</a><a href="#earlier-colourways">Earlier selected-logo colours</a></nav><div class="history-notice"><strong>Brand and design history</strong><p>All six early logo directions, their brand strategy and palette, plus the five earlier selected-logo treatments are preserved here. Recommendations on this page describe earlier rounds; the current guide records the latest work.</p></div>',1)
old=old.replace('<details><summary>Skill sources and process</summary>',archive+'<details><summary>Skill sources and process</summary>')
old=old.replace('</style>','.history-nav{display:flex;gap:24px;flex-wrap:wrap;padding-bottom:25px}.history-notice{padding:24px;border:1px solid #A63825;border-radius:12px;margin-bottom:35px}.history-notice p{margin-bottom:0}</style>')
for rel in re.findall(r'(?:src|href)="([^"]+)"',old):
 if not rel.startswith(('http','#')):assert (r/rel).is_file(),rel
(r/'brand-history.html').write_text(old)
print('Brand history page created: six original designs, original brand definition, and five previous selected-logo colourways.')
