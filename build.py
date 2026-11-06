"""Rebuild the self-contained home health dashboard from the included snapshot."""
from pathlib import Path
import argparse, hashlib, html, json, re

ROOT=Path(__file__).resolve().parent

def safe_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def inline(text):
    text=html.escape(text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',text)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',text)

def methodology():
    parts=[]
    for block in (ROOT/'README.md').read_text(encoding='utf-8').strip().split('\n\n'):
        if block.startswith('```'):
            parts.append('<pre><code>'+html.escape('\n'.join(block.splitlines()[1:-1]))+'</code></pre>')
        elif block.startswith('# '):parts.append('<h1>'+inline(block[2:])+'</h1>')
        elif block.startswith('## '):
            title=block[3:];slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')
            parts.append('<h2 id="'+slug+'">'+inline(title)+'</h2>')
        elif block.startswith('- '):parts.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines())+'</ul>')
        else:parts.append('<p>'+inline(block)+'</p>')
    style='body{margin:0;background:#f3f6f8;color:#193044;font:16px/1.7 Segoe UI,Arial,sans-serif}nav{background:#102f43;padding:15px 24px}nav a{color:#b7e8e2}main{max-width:920px;margin:24px auto;padding:28px 38px;background:white;border:1px solid #dce5eb;border-radius:12px}h1{line-height:1.2}h2{margin-top:30px;font-size:22px}a{color:#006c7b}pre{background:#edf5f6;padding:14px;overflow:auto}code{overflow-wrap:anywhere}li{margin:7px 0}@media(max-width:650px){main{padding:20px;margin:8px}h1{font-size:28px}}'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Home Health Network Explorer · Methodology</title><style>'+style+'</style></head><body><nav><a href="index.html">← Open dashboard</a></nav><main>'+''.join(parts)+'</main></body></html>'

def outputs():
    page=(ROOT/'src/page.html').read_text(encoding='utf-8')
    initialize=(ROOT/'src/initialize.js').read_text(encoding='utf-8')
    runtime=(ROOT/'src/dashboard.js').read_text(encoding='utf-8')
    for name,file in [('PAYLOAD','payload'),('BASE_GROUPS','baseline_groups')]:
        token='__'+name+'__';assert initialize.count(token)==1
        initialize=initialize.replace(token,safe_json(json.loads((ROOT/'data'/f'{file}.json').read_text(encoding='utf-8'))))
    for name,file in [('POLICIES','policy_anchors'),('DATES','survey_dates')]:
        token='__'+name+'__';assert runtime.count(token)==1
        runtime=runtime.replace(token,safe_json(json.loads((ROOT/'data'/f'{file}.json').read_text(encoding='utf-8'))))
    scripts=[(ROOT/'vendor/vis-network-9.1.9.min.js').read_text(encoding='utf-8'),(ROOT/'src/community_groups.js').read_text(encoding='utf-8'),(ROOT/'src/interactions.js').read_text(encoding='utf-8'),initialize,runtime]
    for i,script in enumerate(scripts):
        token=f'__SCRIPT{i}__';assert page.count(token)==1;page=page.replace(token,script)
    return {'index.html':page,'methodology.html':methodology()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for name,text in outputs().items():
        target=ROOT/name
        if args.check:assert target.read_bytes()==text.encode('utf-8'),'Rebuild needed: '+name
        else:target.write_text(text,encoding='utf-8',newline='\n')
    paths=[ROOT/'build.py',ROOT/'README.md',ROOT/'THIRD_PARTY_NOTICES.md',ROOT/'index.html',ROOT/'methodology.html']
    for folder in ['src','data','methods','vendor']:paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
    manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    target=ROOT/'build_manifest.json'
    if args.check:assert json.loads(target.read_text(encoding='utf-8'))==manifest,'Build manifest differs'
    else:target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'checked':args.check,'verified_files':len(manifest)}))

if __name__=='__main__':main()
