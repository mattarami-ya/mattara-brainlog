# scripts/expand_issue.py （無料版・API不要）
import os, re, datetime, html, textwrap

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(REPO_DIR, "posts")

issue_title = os.getenv("ISSUE_TITLE","Memo").strip() or "Memo"
issue_body  = os.getenv("ISSUE_BODY","").strip()
issue_number = os.getenv("ISSUE_NUMBER","") or "N/A"

def slugify(s):
    s = s.strip().lower()
    s = re.sub(r"[^\w\-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:60] or "post"

def extract_tags(text):
    return " ".join(sorted(set([t.lower() for t in re.findall(r"#([A-Za-z0-9_\-]+)", text)])))

def expand_manually(title, body):
    # “手動増幅”のための軽い整形だけ（見出し・箇条書き化）
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    bullets = "\n".join([f"- {l}" for l in lines]) or "- (no content)"
    article = f"""# {title}

> Quick memo expanded without AI. You can later paste an edited version here.

## Points
{bullets}

## One-line summary
Write your own summary here.
"""
    return article

def main():
    tags = extract_tags(issue_body)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    title = issue_title
    md = expand_manually(title, issue_body)
    slug = today + "-" + slugify(title)
    os.makedirs(POSTS_DIR, exist_ok=True)
    front = f"""---
title: {title}
date: {today}
tags: {tags}
source: issue #{issue_number}
---

"""
    with open(os.path.join(POSTS_DIR, slug + ".md"), "w", encoding="utf-8") as f:
        f.write(front + md.strip() + "\n")
    print("WROTE", slug)

if __name__ == "__main__":
    main()
