from pathlib import Path
R=Path(__file__).resolve().parents[1]
C='#852D26'; S='#E8A535'; P='#FFF6E7'; I='#29231F'
# Original geometric lettering. All logo characters are editable paths, not font dependencies.
glyph={
'D':'M0 0H36C70 0 82 20 82 50S70 100 36 100H0ZM23 22V78H35C53 78 59 68 59 50S53 22 35 22Z',
'U':'M0 0H23V62C23 76 29 81 41 81S59 76 59 62V0H82V64C82 90 66 102 41 102S0 90 0 64Z',
'M':'M0 100V0H24L46 47 68 0H92V100H69V42L46 87 23 42V100Z',
'E':'M0 0H68V22H23V39H62V60H23V78H68V100H0Z',
'O':'M41 -2C70 -2 84 18 84 50S70 102 41 102-2 82-2 50 12-2 41-2ZM41 21C27 21 22 32 22 50S27 79 41 79 60 68 60 50 55 21 41 21Z',
'I':'M0 0H23V100H0Z',
'S':'M73 10L62 29C51 22 44 20 35 20 26 20 22 24 22 29 22 35 30 37 43 41 66 48 76 55 76 72 76 93 60 102 37 102 21 102 8 97-2 90L9 70C20 78 29 81 38 81 49 81 53 77 53 73 53 67 46 65 33 61 11 54-1 46-1 30-1 10 15-2 36-2 50-2 63 2 73 10Z',
'H':'M0 0H23V38H59V0H82V100H59V61H23V100H0Z',
'A':'M-2 100L31 0H58L92 100H67L61 79H28L22 100ZM34 59H55L44 23Z'}
width={'D':82,'U':82,'M':92,'E':68,'O':84,'I':23,'S':76,'H':82,'A':92}
def letters(word,x,y,scale=1,color=C,gap=12):
 out=''
 for ch in word:
  out+=f'<path fill="{color}" fill-rule="evenodd" d="{glyph[ch]}" transform="translate({x} {y}) scale({scale})"/>'
  x+=(width[ch]+gap)*scale
 return out

def pot(color=C,accent=S):
 return f'<g fill="{color}"><path d="M249 65Q260 29 311 29Q353 29 375 53L249 81Z"/><rect x="297" y="14" width="30" height="16" rx="6"/><path d="M249 89H391Q385 108 368 108H272Q255 108 249 89Z"/></g><path d="M244 81L391 51" fill="none" stroke="{accent}" stroke-width="9" stroke-linecap="round"/>'
def svg(body,w,h,title):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>'
def core(color=C,accent=S,rev=False):
 return pot(color,accent)+letters('DUM',74,140,1.12,color,12)+f'<rect x="432" y="133" width="118" height="122" rx="20" fill="{accent}"/>'+letters('E',457,153,.82,P if rev else color)+letters('ODISHA',70,285,1,color,12)
for mode,color,accent,rev in [('primary',C,S,False),('mono',I,I,True),('reversed',P,P,False)]:
 body=core(color,accent,rev)
 if mode=='mono':
  tile=f'<rect x="432" y="133" width="118" height="122" rx="20" fill="{accent}"/>'+letters('E',457,153,.82,P)
  cut=f'<defs><mask id="e-cutout"><rect width="640" height="410" fill="white"/>'+letters('E',457,153,.82,'black')+'</mask></defs>'+f'<rect x="432" y="133" width="118" height="122" rx="20" fill="{accent}" mask="url(#e-cutout)"/>'
  body=body.replace(tile,cut)
 if mode=='reversed':body=body.replace(letters('E',457,153,.82,P),letters('E',457,153,.82,C))
 (R/f'assets/logo/{mode}.svg').write_text(svg(body,640,410,'Dum E Odisha'))
# Compact mark deliberately contains no tiny name. Always pair with full name in context.
icon=f'<path d="M5 15Q8 6 17 6Q24 6 28 12L5 19Z" fill="{C}"/><rect x="14" y="2" width="6" height="4" rx="1" fill="{C}"/><path d="M4 23H29Q28 29 23 29H10Q5 29 4 23Z" fill="{C}"/><path d="M3 20L29 13" stroke="{S}" stroke-width="3" stroke-linecap="round"/>'
(R/'assets/logo/compact.svg').write_text(svg(icon,32,32,'Dum E Odisha serving lid symbol'))
# Supporting rice rhythm, independent from cultural craft traditions.
pattern=''.join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="15" transform="rotate(-28 {x} {y})" fill="{S if j%3==0 else C}"/>' for j,y in enumerate(range(30,230,45)) for x in range(30+(j%2)*25,640,60))
(R/'assets/logo/rice-pattern.svg').write_text(svg(pattern,640,240,'Abstract rice grain pattern'))
(R/'assets/tokens.css').write_text(':root{--chilli:#852D26;--saffron:#E8A535;--cream:#FFF6E7;--ink:#29231F;--space:8px;--radius:20px;--body-font:Arial,Helvetica,sans-serif;}\n')
# Actual editable applications with explicit, non-promotional operational placeholders.
label=f'<rect width="900" height="550" fill="{P}"/><g transform="translate(28 26) scale(.47)">{core()}</g><path d="M350 35V515" stroke="{C}" stroke-width="2"/><g font-family="Arial,Helvetica,sans-serif" fill="{I}"><text x="390" y="85" font-size="19" letter-spacing="3">ORDER LABEL • TEMPLATE</text><text x="390" y="150" font-size="38" font-weight="bold">[Dish name]</text><text x="390" y="205" font-size="24">[Portion] · [Order number]</text><text x="390" y="280" font-size="22">Packed: [date / time]</text><text x="390" y="330" font-size="22">Allergens: [verified information]</text><text x="390" y="380" font-size="22">[Dietary classification in words]</text><text x="390" y="470" font-size="17">Proof content and food-label requirements before use.</text></g>'
(R/'applications/order-label.svg').write_text(svg(label,900,550,'Draft editable order label with placeholders'))
social=f'<rect width="1080" height="1350" fill="{P}"/><g transform="translate(60 55) scale(.6)">{core()}</g><g font-family="Arial,Helvetica,sans-serif" fill="{C}"><text x="65" y="420" font-size="88" font-weight="bold">Flavour in</text><text x="65" y="515" font-size="88" font-weight="bold">every layer.</text><text x="65" y="600" font-size="28">DUM E ODISHA · BIRYANI</text></g><g transform="translate(0 690) scale(1.7)">{pattern}</g><path d="M65 1175H1015" stroke="{C}" stroke-width="2"/><text x="65" y="1240" font-family="Arial,Helvetica,sans-serif" font-size="26" fill="{C}">[Verified menu / ordering destination]</text>'
(R/'applications/social-portrait.svg').write_text(svg(social,1080,1350,'Draft portrait social template'))
# comparison retaining rather than adopting a fundamentally different route
alt=letters('DUM',35,50,.75,C)+letters('E',270,50,.75,C)+letters('ODISHA',35,155,.65,C)
(R/'sources/alternative-type-only.svg').write_text(svg(alt,400,260,'Alternative type-only direction, not selected'))
print('Generated 8 vector assets and CSS tokens')
