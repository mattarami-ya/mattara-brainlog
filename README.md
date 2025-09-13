# 🧠 Mattara Brainlog

A personal "Brain-to-Web" system for Mattara.  
Short notes written as GitHub Issues (with label `note`) are expanded into full-length articles by AI and automatically published via GitHub Pages.  

## ✨ Features
- Write a quick thought → AI expands it into an article
- Auto-published as a blog-style site via GitHub Pages
- Supports tags like `#anime`, `#music`, `#minecraft`
- Powered by OpenAI + GitHub Actions

## 🚀 How it works
1. Create a new Issue with the label `note`
2. Add a short memo or impression (1–5 lines is enough)
3. GitHub Actions will:
   - Call AI to expand your note into an article
   - Save it as Markdown in `posts/`
   - Build the site into `site/`
   - Publish automatically via GitHub Pages

Your memo instantly becomes part of your external brain 🌐

## 🔧 Setup
- Add your `OPENAI_API_KEY` in GitHub → Settings → Secrets → Actions
- Enable GitHub Pages (deploy from branch, `/root`)
- Start writing Issues!

---
