import sys
sys.path.insert(0,'/private/tmp/dum-brand-python')
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from pathlib import Path
root=Path(__file__).resolve().parents[1]
red='#A63825';gold='#ECAA35';green='#254A39';cream='#FFF3DD'
def lettering(txt,font,size,x,y,color,spacing=0):
 f=TTFont(font);gs=f.getGlyphSet();cm=f.getBestCmap();scale=size/f['head'].unitsPerEm
 widths=[gs[cm[ord(c)]].width for c in txt];w=sum(widths)*scale+spacing*(len(txt)-1);cur=x-w/2
 out=''
 for c,adv in zip(txt,widths):
  pen=SVGPathPen(gs);gs[cm[ord(c)]].draw(pen)
  out+=f'<path fill="{color}" transform="translate({cur:.3f} {y}) scale({scale:.6f} {-scale:.6f})" d="{pen.getCommands()}"/>'
  cur+=adv*scale+spacing
 return out
symbol=f'''<g id="icon">
<path fill="{red}" d="M64 130 Q128 147 192 130 C213 151 215 176 198 197 Q184 220 153 220 H103 Q72 220 58 197 C41 176 43 151 64 130 Z"/>
<path fill="{gold}" d="M45 112 Q128 79 211 112 Q218 115 213 123 Q128 145 43 123 Q38 115 45 112 Z"/>
<path fill="{red}" d="M75 101 Q81 73 114 68 V63 Q114 57 120 57 H136 Q142 57 142 63 V68 Q175 73 181 101 Q127 84 75 101 Z"/>
<path fill="{red}" d="M138 12 C179 18 184 47 159 59 C146 66 127 61 128 47 C129 36 143 34 149 41 C136 38 134 48 144 49 C161 52 164 32 138 12 Z"/>
<path fill="{gold}" d="M108 17 C87 27 82 43 105 57 C96 41 108 32 108 17 Z"/>
<path fill="{cream}" d="M98 165 Q115 159 120 177 Q103 182 98 165 Z M127 158 Q143 163 132 179 Q119 172 127 158 Z M149 163 Q159 179 142 184 Q132 169 149 163 Z"/>
</g>'''
# A true transparent monochrome mark needs its negative space to remain transparent.
symbol=symbol.replace(f'<path fill="{red}" d="M64 130 Q128 147 192 130 C213 151 215 176 198 197 Q184 220 153 220 H103 Q72 220 58 197 C41 176 43 151 64 130 Z"/>',f'<path fill="{red}" fill-rule="evenodd" d="M64 130 Q128 147 192 130 C213 151 215 176 198 197 Q184 220 153 220 H103 Q72 220 58 197 C41 176 43 151 64 130 Z M98 165 Q115 159 120 177 Q103 182 98 165 Z M127 158 Q143 163 132 179 Q119 172 127 158 Z M149 163 Q159 179 142 184 Q132 169 149 163 Z"/>').replace(f'<path fill="{cream}" d="M98 165 Q115 159 120 177 Q103 182 98 165 Z M127 158 Q143 163 132 179 Q119 172 127 158 Z M149 163 Q159 179 142 184 Q132 169 149 163 Z"/>','')
head='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 600" role="img"><title>Dum E Biryani — The Aroma Handi concept</title>'
word=lettering('dum e','/System/Library/Fonts/Supplemental/Georgia Bold.ttf',96,320,386,red,-4)
word+=lettering('BIRYANI','/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf',43,320,451,red,8)
word+=lettering('O D I S H A','/System/Library/Fonts/Supplemental/Arial.ttf',19,320,500,green,1)
(root/'concepts/a-aroma-handi.svg').write_text(head+'<g transform="translate(185 25) scale(1.05)">'+symbol+'</g><g id="wordmark">'+word+'</g></svg>')
(root/'concepts/a-aroma-handi-symbol.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img"><title>Aroma Handi symbol</title>'+symbol+'</svg>')
print('Primary concept created with outlined lettering.')
