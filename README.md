# Honda Civic Type R RAG Assistant

A retrieval-augmented generation (RAG) system that answers questions about the Honda Civic using the official owner's manual as its knowledge source.

## Status
✅ Working end-to-end pipeline — retrieval, embeddings, and local LLM generation all functional.

## What it does
Given a natural-language question (e.g. "What's the recommended tyre pressure?"), the system retrieves the most relevant excerpts from the 787-page owner's manual and generates a clear, grounded answer citing the source page numbers — without needing to search the manual manually.

## How it works
1. **Extraction** — the manual PDF is parsed page-by-page (`src/extract.py`) using `pypdf`
2. **Chunking** — extracted text is split into overlapping ~500-word chunks (`src/chunk.py`) so retrieval isn't limited by page boundaries
3. **Embedding & storage** — chunks are embedded and stored in a local ChromaDB vector database (`src/embed.py`)
4. **Retrieval + generation** — a user's question is embedded, the most relevant chunks are retrieved, and an LLM generates an answer grounded in that context

## Two generation options
- **`src/query.py`** — uses the Anthropic Claude API (requires an API key and billing set up at console.anthropic.com)
- **`src/query_local_llm.py`** — a fully free, zero-API-key alternative using an open-source model (Qwen2.5-3B-Instruct) running on Google Colab's free GPU tier, built specifically to avoid any cost or local installation requirements

## Stack
- Python
- pypdf (PDF text extraction)
- ChromaDB (vector database)
- Anthropic API and/or Hugging Face Transformers (generation)
- Google Colab (free GPU hosting for the local LLM version)

## Known limitations
- Retrieval occasionally surfaces an incorrect but nearby chunk for entity-specific questions (e.g. a question about engine oil once returned coolant information instead). This is a common RAG failure mode; candidate fixes include smaller chunk sizes, reduced retrieval count, or adding a reranking step.
- The manual PDF and derived data files (extracted text, chunks, vector database) are intentionally excluded from this repository, as the manual itself is Honda's copyrighted material. To run this project, supply your own copy of the manual in `data/manual.pdf`.

## Setup
For the free local LLM version, upload `data/manual_chunks.json` into a Google Colab notebook (T4 GPU runtime) and run the equivalent steps from `src/query_local_llm.py`.

## Roadmap
- [x] Extract and clean text from the owner's manual PDF
- [x] Chunk and embed the manual content
- [x] Build a basic retrieval + query pipeline
- [x] Free, local-LLM alternative (no API key required)
- [ ] Improve retrieval accuracy (reduce cross-topic confusion)
- [ ] Add a simple CLI or chat interface
- [ ] Write tests

## Author
Keenen Thwala
