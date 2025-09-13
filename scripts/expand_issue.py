import os, re, requests, datetime
REPO_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); POSTS_DIR=os.path.join(REPO_DIR,'posts'); PROMPT=open(os.path.join(REPO_DIR,'templates','post_prompt.md'),encoding='utf-8').read()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY'); MODEL=os.getenv('OPENAI_MODEL','gpt-4o-mini')
issue_title=os.getenv('ISSUE_TITLE','新規メモ'); issue_body=os.getenv('ISSUE_BODY',''); issue_number=os.getenv('ISSUE_NUMBER','')
def slug(s): import re; s=s.strip().lower(); s=re.sub(r'[^\w\-]+','-',s); s=re.sub(r'-+','-',s).strip('-'); return s[:60] or 'post'
def tags(t): import re; return ' '.join(sorted(set([m.lower() for m in re.findall(r'#([A-Za-z0-9_\-]+)', t)])))
def call_llm(note, title_hint):
    prompt=PROMPT.replace('{{NOTE}}', note.strip())
    r=requests.post('https://api.openai.com/v1/chat/completions', headers={'Authorization':f'Bearer {OPENAI_API_KEY}','Content-Type':'application/json'}, json={'model':MODEL,'messages':[{'role':'system','content':'You are a helpful editor and writer.'},{'role':'user','content':prompt}],'temperature':0.7}, timeout=120); r.raise_for_status()
    content=r.json()['choices'][0]['message']['content']
    lines=content.splitlines(); gen_title=title_hint
    if lines and lines[0].lstrip().startswith('# '):
        gen_title=lines[0].lstrip()[2:].strip() or title_hint; content='\n'.join(lines[1:]).lstrip()
    return gen_title, content
if not OPENAI_API_KEY: raise SystemExit('OPENAI_API_KEY is missing.')
title, article=call_llm(issue_body, issue_title); tg=tags(issue_body+'\n'+article)
today=datetime.datetime.now().strftime('%Y-%m-%d'); slug= today+'-'+slug(title)
os.makedirs(POSTS_DIR,exist_ok=True)
front=f"""---
title: {title}
date: {today}
tags: {tg}
source: issue #{issue_number}
---

"""
open(os.path.join(POSTS_DIR, slug+'.md'),'w',encoding='utf-8').write(front+article.strip()+'\n')
print('WROTE', slug)
