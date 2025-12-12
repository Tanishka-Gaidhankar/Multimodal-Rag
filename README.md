# 📑 Multi-Modal Document Intelligence — Compact RAG Demo

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/gradio-%3E%3D3.0-orange)](https://gradio.app/)


A compact, opinionated Retrieval-Augmented Generation (RAG) demo that turns PDFs into a multimodal knowledge source: index page-level semantics, retrieve relevant pages, convert them to images, and ask a multimodal assistant (text + images) to answer grounded questions.

This repo is designed for experimentation and demos — fast to run locally and easy to extend.


 Demo Video - https://drive.google.com/file/d/1Y64lY3x6zD5ck5a8igwfJB3yeNFEgcvh/view?usp=sharing
---

## ✨ Highlights 
- Page-level indexing for crisp, focused retrieval (fast and memory-light).
- Multimodal prompts: only the retrieved pages are converted to images and sent to the model, so charts/tables/figures become first-class evidence.
- Lightweight, local embedding model for offline semantic search (`all-MiniLM-L6-v2`).
- Simple Gradio UI to upload a PDF and chat with a grounded assistant.

## Bonus Tracks
- **Smart Page Viewer (Evidence Gallery):** The UI includes a Gallery that displays the page images saved under `temp_evidence` (see `app.py` and `logic.py`). After retrieval the code saves the retrieved pages as PNG files in `D:/MultiModalProject/temp_evidence` and returns their file paths so the Gradio Gallery can show the exact visual evidence (charts, tables, figures) used to ground answers.
- **Automated Summarization (Executive Summary):** A quick-action button in `app.py` pre-fills a summarization prompt and submits it to the same multimodal pipeline. `logic.py` routes the prompt to the Groq chat completion with the retrieved page images attached, producing a concise executive summary of main findings and financial tables.

 
---

## 🚀 Demo screenshots
<img width="850" alt="Screenshot 1" src="https://github.com/user-attachments/assets/530f36fc-c0b6-4c83-a809-6afc1bda8da2" />
<img width="850" alt="Screenshot 2" src="https://github.com/user-attachments/assets/3be8584a-d605-411d-bf67-9a9440b43876" />
<img width="850" alt="Screenshot 3" src="https://github.com/user-attachments/assets/0691501b-5627-49d0-ac44-522fcebeb972" />

---


---

## 🧰 Tech stack
- groq — chat/completion calls to a multimodal model
- sentence_transformers — `all-MiniLM-L6-v2` for lightweight embeddings
- PyPDF2 — page text extraction
- pdf2image — page → PNG conversions for multimodal contexts
- numpy — similarity math
- gradio — demo UI
- dotenv — local config of `GROQ_API_KEY`

---

## 🛠️ Quickstart (run locally)
1. Create a virtual environment and activate:
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\\Scripts\\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your API key:
- Create a `.env` with:
```
GROQ_API_KEY=sk-...
```

4. Launch the Gradio demo:
```bash
python app.py
```

Open the local URL printed by Gradio and upload a PDF.

---



## 📂 Files of interest
- app.py — Gradio UI + handlers
- logic.py — indexing, retrieval, image conversion, prompt construction, API call
- requirements.txt — Python dependencies

---

## ⚙️ How retrieval works (brief)
1. build_vector_index(pdf_path): extract each page's text and compute embeddings. Embeddings are cached so subsequent queries on the same file are fast.
2. Query: embed the user's question.
3. Ranking: compute dot-product similarity between the query embedding and each page embedding and pick top-N pages (default: 2).
4. Multimodal prompt: convert only the top pages to PNGs, encode as base64 data-URLs, and include them as image entries alongside a short text context.
5. Completion: call the Groq chat API with text+image contents. The assistant reply is returned to the UI and includes "Sources: page X" tags.

---







