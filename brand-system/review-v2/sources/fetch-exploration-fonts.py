"""Download unmodified Noto fonts and their OFL licenses from Google Fonts."""
from pathlib import Path
import hashlib,json,urllib.request
R=Path(__file__).resolve().parents[1]/'explorations/fonts'
families=['notoseriforiya','notosansoriya','notoserifdevanagari','notosansdevanagari']
records=[]
for family in families:
    url=f'https://api.github.com/repos/google/fonts/contents/ofl/{family}'
    request=urllib.request.Request(url,headers={'User-Agent':'DumEOdisha-local-brand-review'})
    listing=json.load(urllib.request.urlopen(request,timeout=30))
    font=next(x for x in listing if x['name'].endswith('.ttf'))
    license=next(x for x in listing if x['name']=='OFL.txt')
    for item,filename in [(font,f'{family}.ttf'),(license,f'{family}-OFL.txt')]:
        data=urllib.request.urlopen(item['download_url'],timeout=30).read()
        if filename.endswith('.txt') and b'SIL OPEN FONT LICENSE' not in data.upper():raise ValueError('Unexpected license')
        (R/filename).write_bytes(data)
        records.append({'file':filename,'source':item['download_url'],'upstreamName':item['name'],'sha256':hashlib.sha256(data).hexdigest(),'checkedAt':'2026-10-17','modified':False})
(R/'provenance.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([r['file'] for r in records]))
