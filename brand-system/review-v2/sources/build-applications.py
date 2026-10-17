"""Build portable HTML templates. Generated artwork stays raster; type stays editable."""
from pathlib import Path
import base64

R = Path(__file__).resolve().parents[1]
def image(path):
    p = R / path
    return 'data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode()

logo = image('assets/logo/primary.png')
art = image('assets/illustration/lifted-lid.png')
css = '''*{box-sizing:border-box}body{margin:0;background:#e9dfd0;color:#29231f;font:16px/1.5 Arial,Helvetica,sans-serif}.toolbar{max-width:1100px;margin:24px auto;padding:24px;background:#fff6e7}a{color:#852d26}h1{font:34px Georgia,serif;margin:0 0 12px}button{padding:10px 18px;background:#852d26;color:#fff6e7;border:0;font:inherit;cursor:pointer}input{display:block;width:100%;padding:10px;border:1px solid #786757;font:inherit;background:#fffdf6}label{display:block;margin:12px 0}.fields{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #852d26;outline-offset:4px}.stage{padding:30px 0;overflow:auto}.artboard{position:relative;background:#fff6e7;overflow:hidden;margin:0 auto;color:#852d26;flex-shrink:0}.artboard img{display:block}.brand{object-fit:contain}.social{width:1080px;height:1350px;padding:65px 70px}.social .brand{width:240px;height:190px}.social h2{font:100px/1.03 Georgia,serif;letter-spacing:-3px;font-weight:normal;max-width:920px;margin:55px 0 0;min-height:220px;overflow-wrap:anywhere}.social .art{position:absolute;left:0;top:540px;width:1080px;height:650px;object-fit:cover;mix-blend-mode:multiply}.social .caption{position:absolute;left:70px;right:70px;bottom:75px;border-top:2px solid #852d26;padding-top:20px;font:23px Arial,sans-serif;overflow-wrap:anywhere}.social .ig{position:absolute;right:70px;top:95px;font-size:22px}.label{width:900px;height:550px;padding:40px;display:grid;grid-template-columns:260px 1fr;gap:35px}.label .brand{width:250px;height:210px;margin-top:35px}.label .signature{font:italic 20px/1.4 Georgia,serif;text-align:center;margin-top:22px}.label .info{padding-left:30px;border-left:1px solid #b9a489;color:#29231f}.label .eyebrow{font-size:12px;letter-spacing:2px}.label h2{font:38px/1.1 Georgia,serif;margin:20px 0;overflow-wrap:anywhere}.label .meta{font-size:19px;margin:14px 0;overflow-wrap:anywhere}.label .allergens{border-top:1px solid #b9a489;padding-top:18px;font-size:18px;margin-top:23px;overflow-wrap:anywhere}.label .footer{font-size:15px;margin-top:24px;color:#852d26}.hint{font-size:13px}button:hover{background:#29231f}@media(max-width:650px){.toolbar{margin:0;padding:20px}.fields{grid-template-columns:1fr}.stage{padding:20px}}@media print{@page{size:__PAGE__;margin:0}.toolbar{display:none}body{background:#fff6e7}.stage{padding:0;overflow:visible}.artboard{margin:0;width:__WIDTH__px;height:__HEIGHT__px;print-color-adjust:exact;-webkit-print-color-adjust:exact}}'''
script = '''document.querySelectorAll('input[data-target]').forEach(input=>input.addEventListener('input',()=>{document.getElementById(input.dataset.target).textContent=input.value||input.placeholder}));document.getElementById('print').addEventListener('click',()=>window.print());'''

def build(name,title,fields,canvas,w,h):
    controls=''.join(f'<label>{label}<input data-target="{key}" maxlength="{limit}" value="{value}" placeholder="{value}"></label>' for key,label,value,limit in fields)
    page=css.replace('__PAGE__',f'{w}px {h}px').replace('__WIDTH__',str(w)).replace('__HEIGHT__',str(h))
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — Dum E Odisha</title><style>{page}</style></head><body><div class="toolbar"><a href="../index.html#applications">← Back to the brand kit</a><h1>{title}</h1><p>Edit the fields, then print or save a PDF proof. Artwork is embedded for portability. This is a draft layout, not production packaging.</p><div class="fields">{controls}</div><button id="print" type="button">Print / save PDF proof</button><p class="hint">The canvas is {w} × {h} px. Review text wrapping before export. Replace every bracketed field with verified content. These working dimensions have not been validated against current Instagram crops.</p></div><div class="stage"><article class="artboard {'social' if name=='social-portrait' else 'label'}" aria-label="{title} preview">{canvas}</article></div><script>{script}</script></body></html>'''
    (R/f'applications/{name}.html').write_text(html)

build('social-portrait','Portrait social template',[
 ('headline','Heading (up to 42 characters)','Flavour in Every Layer.',42),
 ('caption','Supporting line (up to 70 characters)','Bhubaneswar · Bulk orders: +91 78942 65632',70),
],f'<img class="brand" src="{logo}" alt="Dum E Odisha"><div class="ig">@dum_e_odisha</div><h2 id="headline">Flavour in Every Layer.</h2><img class="art" src="{art}" alt="Gouache-style biryani illustration"><div class="caption" id="caption">Bhubaneswar · Bulk orders: +91 78942 65632</div>',1080,1350)

build('order-label','Editable order label',[
 ('dish','Dish (up to 48 characters)','[Dish name]',48),
 ('portion','Portion (up to 36 characters)','[Portion]',36),
 ('order','Order number (up to 25 characters)','[Order number]',25),
 ('packed','Packed date and time (up to 35 characters)','[Date / time]',35),
 ('allergens','Verified allergens (up to 65 characters)','[Verified allergen information]',65),
],f'<div><img class="brand" src="{logo}" alt="Dum E Odisha"><div class="signature">Flavour in Every Layer.</div></div><div class="info"><div class="eyebrow">ORDER LABEL · CONTENT TEMPLATE</div><h2 id="dish">[Dish name]</h2><p class="meta">Portion: <span id="portion">[Portion]</span></p><p class="meta">Order: <span id="order">[Order number]</span></p><p class="meta">Packed: <span id="packed">[Date / time]</span></p><p class="allergens">Allergens: <span id="allergens">[Verified allergen information]</span></p><div class="footer">@dum_e_odisha · +91 78942 65632</div></div>',900,550)
print('Built two portable, editable HTML applications')
