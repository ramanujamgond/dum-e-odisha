from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import subprocess
import urllib.request
import zipfile

COMMIT = '270f2916f64c14a24ac6180d0e55ee6ba9dfc1e1'
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'public'

def digest(data):
    return hashlib.sha256(data).hexdigest()

if os.environ.get('DUM_E_SOURCE'):
    source = Path(os.environ['DUM_E_SOURCE']) / 'brand'
else:
    archive = ROOT / 'source.tar.gz'
    url = f'https://codeload.github.com/ramanujamgond/dum-e-odisha/tar.gz/{COMMIT}'
    print(f'Downloading public source commit {COMMIT}', flush=True)
    urllib.request.urlretrieve(url, archive)
    extracted = ROOT / 'source'
    extracted.mkdir(exist_ok=True)
    subprocess.run(['tar', '-xzf', str(archive), '--strip-components=1', '-C', str(extracted)], check=True)
    source = extracted / 'brand'

if OUTPUT.exists():
    shutil.rmtree(OUTPUT)
shutil.copytree(source, OUTPUT, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.zip', '.DS_Store'))
bundles = json.loads((ROOT / 'bundles.json').read_text())
for bundle in bundles:
    target = OUTPUT / bundle['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for entry in bundle['entries']:
            content = (source / entry['source']).read_bytes() if 'source' in entry else base64.b64decode(entry['data'])
            if digest(content) != entry['sha256']:
                raise ValueError(f"Bundle content mismatch: {bundle['path']}:{entry['name']}")
            archive.writestr(entry['name'], content)
    print(f"Built {bundle['path']} ({target.stat().st_size} bytes)", flush=True)
shutil.copyfile(OUTPUT / 'brand-review.html', OUTPUT / 'index.html')
(OUTPUT / 'deployment.json').write_text(json.dumps({'repository': 'ramanujamgond/dum-e-odisha', 'commit': COMMIT, 'bundles': len(bundles)}) + '\n')
print('Static site ready in public/', flush=True)
