import os, glob, markdown, html
ROOT=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(ROOT)
POSTS=os.path.join(REPO,"posts"); SITE=os.path.join(REPO,"docs")
CSS="body{font-family:system-ui,-apple-system,'Noto Sans JP',sans-serif;background:#f7f7fb;margin:0} .header{background:#111;color:#fff;padding:18px 16px}.title{max-width:980px;margin:0 auto;font-weight:700}.container{max-width:980px;margin:18px auto;padding:0 12px}.card{background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06);padding:16px 18px;margin:12px 0} a{color:#0a58ca} .post-meta{color:#666;font-size:.9em;margin-top:-6px;margin-bottom:10px}"
IDX='<!doctype html><html lang=ja><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>マッタラミーヤ｜統合ホーム</title><style>'+CSS+'</style><div class=header><div class=title>マッタラミーヤの音楽実験室｜統合ホーム</div></div><div class=container><div class=card><h2>最新の投稿</h2>{items}</div><div class=card><h2>このサイトについて</h2><p>スマホからの1行メモをAIで増幅して読み物化したサイトです。</p></div></div>'
PST='<!doctype html><html lang=ja><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{t}</title><style>'+CSS+'</style><div class=header><div class=title><a href=./index.html style="color:#fff">← トップ</a></div></div><div class=container><div class=card><h1>{t}</h1><div class=post-meta>{d} {tags}</div><div class=content>{c}</div></div></div>'
def parse_fm(s):
    if s.startswith('---'):
        end=s.find('\n---',3)
        if end!=-1:
            fm=dict([tuple(map(str.strip,l.split(':',1))) for l in s[3:end].splitlines() if ':' in l])
            return fm, s[end+4:].lstrip()
    return {}, s
os.makedirs(SITE,exist_ok=True)
items=[]
for p in sorted(glob.glob(os.path.join(POSTS,'*.md')), reverse=True):
    raw=open(p,encoding='utf-8').read(); fm, body=parse_fm(raw)
    title=fm.get('title') or os.path.splitext(os.path.basename(p))[0]; date=fm.get('date',''); tags=fm.get('tags','')
    html_body=markdown.markdown(body, extensions=['extra'])
    name=os.path.splitext(os.path.basename(p))[0]+'.html'
    open(os.path.join(SITE,name),'w',encoding='utf-8').write(PST.format(t=html.escape(title), d=html.escape(date), tags=html.escape(' / '+tags if tags else ''), c=html_body))
    items.append(f'<a class=list-item href="{name}">{html.escape(date)} — {html.escape(title)}</a>')
open(os.path.join(SITE,'index.html'),'w',encoding='utf-8').write(IDX.format(items='\n'.join(items) if items else '<p>まだ投稿がありません。</p>'))
