"""Rebuild the self-contained home health dashboard from the included snapshot."""
from pathlib import Path
import argparse, hashlib, html, json, re

ROOT=Path(__file__).resolve().parent

def safe_json(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def inline(text):
    text=html.escape(text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',text)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    return re.sub(r'\b(n|c|m|w|s|f|df|x)_([A-Za-z]+)\b',r'<var>\1<sub>\2</sub></var>',text)

def methodology():
    equations={item['tex']:item for item in json.loads((ROOT/'methods/equations.json').read_text(encoding='utf-8'))}
    parts=[]
    for block in (ROOT/'README.md').read_text(encoding='utf-8').strip().split('\n\n'):
        if block.startswith('```math\n'):
            tex='\n'.join(block.splitlines()[1:-1]);item=equations[tex]
            parts.append('<figure class="equation" id="equation-'+item['id']+'"><figcaption>'+html.escape(item['title'])+'</figcaption><div class="equation-scroll" tabindex="0" role="group" aria-label="'+html.escape(item['label'],quote=True)+'"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><semantics>'+item['mathml']+'<annotation encoding="application/x-tex">'+html.escape(tex)+'</annotation></semantics></math></div></figure>')
        elif block.startswith('```'):
            parts.append('<pre><code>'+html.escape('\n'.join(block.splitlines()[1:-1]))+'</code></pre>')
        elif block.startswith('# '):parts.append('<h1>'+inline(block[2:])+'</h1>')
        elif block.startswith('## '):
            title=block[3:];slug=re.sub(r'[^a-z0-9]+','-',title.lower()).strip('-')
            parts.append('<h2 id="'+slug+'">'+inline(title)+'</h2>')
        elif block.startswith('### '):parts.append('<h3>'+inline(block[4:])+'</h3>')
        elif block.startswith('- '):parts.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines())+'</ul>')
        else:parts.append('<p>'+inline(block)+'</p>')
    style='''*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:#f3f6f8;color:#193044;font:17px/1.75 Segoe UI,Arial,sans-serif}nav{background:#102f43;padding:15px 24px}nav a{color:#b7e8e2}main{max-width:1000px;margin:28px auto;padding:34px 48px;background:white;border:1px solid #dce5eb;border-radius:14px}h1{line-height:1.2;font-size:36px;letter-spacing:-.6px}h2{margin:42px 0 16px;padding-top:18px;border-top:1px solid #dfE8ec;font-size:25px;line-height:1.35}h3{margin-top:30px;font-size:21px}a{color:#006c7b;text-underline-offset:3px;overflow-wrap:anywhere}a:hover{color:#004c58}a:focus-visible,.equation-scroll:focus-visible{outline:3px solid #008b8a;outline-offset:4px}p{margin:16px 0}pre{background:#edf5f6;padding:16px;overflow:auto;border-radius:8px;font-size:14px}code{overflow-wrap:anywhere}li{margin:8px 0}.equation{margin:18px 0;padding:18px 22px;border:1px solid #e3e8ee;border-radius:10px;background:#fff;color:#1f2d3a;font-size:16px;break-inside:avoid}.equation figcaption{font-weight:700;font-size:17px;color:#233d57;margin:0 0 10px}.equation-scroll{width:100%;overflow-x:auto;overflow-y:hidden;scrollbar-width:thin}.equation math{margin:12px 0;font-size:1.22em;font-family:math;display:block;overflow-x:auto;overflow-y:hidden;max-width:100%}#version-covered-by-these-methods+p{padding:18px 20px;border-radius:8px;background:#edf5f6;border:1px solid #cddfe4}.toc{display:flex;gap:8px 16px;flex-wrap:wrap;margin:24px 0;padding:16px 0;border-bottom:1px solid #dce5eb;font-size:15px}.toc a{white-space:normal}@media(max-width:650px){main{padding:22px 18px;margin:8px}h1{font-size:28px}h2{font-size:22px}body{font-size:16px}.equation{padding:15px 12px 14px;margin:20px 0}nav{padding:13px 20px}}@media print{body{background:white;font-size:11pt}main{border:0;padding:0;margin:0;max-width:none}nav,.toc{display:none}.equation{background:white}.equation math{font-size:16pt}a{color:inherit;text-decoration:none}h2{break-after:avoid}}'''
    toc='<div class="toc" role="navigation" aria-label="On this page">'+''.join('<a href="#'+slug+'">'+label+'</a>' for slug,label in [('data-and-scope','Data'),('from-narratives-to-ai-assisted-coding','AI-assisted coding'),('connection-mathematics','Connection formulas'),('removal-simulations','Published simulations'),('current-simulation-behavior','Current simulations'),('issues-and-policy','Policy mapping'),('reading-coverage-and-limitations','Limitations')])+'</div>'
    parts.insert(2,toc)
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
