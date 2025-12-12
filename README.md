# 📑 TECHNICAL REPORT: Multi-Modal Document Intelligence

This repository implements a compact multimodal Retrieval-Augmented Generation (RAG) demo that indexes PDF pages, retrieves semantically relevant pages for a user query, converts those pages to images, and sends text+image context to a large-model chat completion for a grounded answer.

**What we built**
- A small Gradio app (`app.py`) that accepts a PDF and a user question and displays an assistant conversation UI.
- A processing module (`logic.py`) that performs PDF text extraction, page-level semantic indexing (embeddings), retrieval of top relevant pages, page image conversion, and a multimodal chat completion call to a model via the Groq client.

**Technologies & libraries used**
- `groq` — client used to call a chat/completion model (multimodal-capable) with text+image content.
- `sentence_transformers` — `all-MiniLM-L6-v2` used to produce compact sentence embeddings for semantic retrieval.
- `PyPDF2` — extract page-level text from PDFs.
- `pdf2image` — convert retrieved PDF pages into PNG images for multimodal prompts.
- `numpy` — vector math for similarity scoring and ranking.
- `base64`, `io` — encode images as data-URLs for inclusion in the model request.
- `dotenv` — load `GROQ_API_KEY` from environment.
- `gradio` — lightweight web UI used in `app.py` for file upload and chat interaction.

**How retrieval works (summary of `logic.py`)**
1. Indexing: `build_vector_index(pdf_path)` extracts text from each PDF page using `PyPDF2` and computes page embeddings using the SentenceTransformer model. Embeddings are cached per-file so repeated queries against the same PDF are fast.
2. Query encoding: on each user question the query is embedded with the same `embed_model`.
3. Retrieval: compute dot-product similarities between page embeddings and the query embedding (`numpy.dot`), then select the top-N page indices (the code selects top 2). These page indices are used as the relevant sources.
4. Multimodal context preparation: convert only the retrieved pages to images with `pdf2image`; encode images to base64 and attach them to the request as `data:image/png;base64,...` URLs. Also provide a short textual prompt instructing the model to analyze the returned pages in relation to the user query.
5. Grounded completion: send the prepared `content_list` (text prompt + image entries) to the Groq chat completion API. The assistant response is returned to the UI with an automated “Sources” line listing the verified page numbers.

**Why this design**
- Page-level indexing keeps retrieval fine-grained and memory-efficient (no need to index every paragraph separately unless desired).
- Using a small local embedding model (`all-MiniLM-L6-v2`) provides fast, offline semantic retrieval for documents.
- Converting only retrieved pages to images reduces IO and CPU overhead while enabling the multimodal model to inspect charts, figures, or visually formatted tables.
- Caching `page_embeddings` avoids repeated work when the same PDF is queried multiple times.

**How to run locally**
1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS / Linux
source .venv/bin/activate
```
2. Install dependencies (add any missing libraries to `requirements.txt`):

```bash
pip install -r requirements.txt
```
3. Set `GROQ_API_KEY` in your environment or a `.env` file.
4. Launch the Gradio app:

```bash
python app.py
```

**Limitations & notes**
- Security: the demo encodes images and sends them to the model provider; do not use with sensitive documents unless your model provider's policy and encryption meet your requirements.
- Scaling: for very large document collections you should shard, persist, and use a dedicated vector database (FAISS, Milvus, Pinecone, etc.) instead of in-memory arrays.
- Citation granularity: current implementation cites page numbers. For paragraph-level provenance, split pages into smaller chunks and store chunk-level metadata alongside embeddings.

**Files of interest**
- `app.py`: Gradio UI glue and event handlers.
- `logic.py`: indexing, retrieval, multimodal input construction, and Groq completion call.

If you want, I can add a short diagram, example interaction transcript, or expand the README with code snippets highlighting the retrieval code paths. Tell me which you'd prefer.

