# Honda Civic Type R RAG Assistant

A retrieval-augmented generation (RAG) system that answers questions about a Honda Civic using the official owner's manual as its knowledge source.

## Status

Working end-to-end pipeline. Retrieval accuracy tuning and a command-line interface are in progress.

## What it does

Given a natural-language question such as "What is the recommended tyre pressure?", the system finds the most relevant excerpts from the 787-page owner's manual and generates an answer grounded in those excerpts, citing the page numbers.

## How it works

1. Extraction: the manual PDF is parsed page by page with pypdf (src/extract.py)
2. Chunking: the text is split into overlapping chunks of about 500 words, ignoring page boundaries (src/chunk.py)
3. Embedding and storage: chunks are embedded and stored in a local ChromaDB vector database (src/embed.py)
4. Retrieval and generation: the question is matched against the stored chunks and the best matches are passed to an LLM, which writes the answer

## Generation options

- src/query.py uses the Anthropic Claude API. It needs an API key in a .env file and billing set up on the Anthropic console.
- src/query_local_llm.py is a free alternative using an open-source model (Qwen2.5-3B-Instruct) on Google Colab's free T4 GPU. No API key and no local install needed.

## Stack

- Python
- pypdf
- ChromaDB
- Anthropic API or Hugging Face Transformers
- Google Colab (free GPU for the local LLM version)

## Known limitations

- Retrieval sometimes returns a nearby but wrong section for specific questions. For example, a question about engine oil once returned coolant information.
- The manual PDF and everything derived from it (extracted text, chunks, vector database) are excluded from this repository because the manual is Honda's copyrighted material. To run the project, place your own copy at data/manual.pdf.

## Setup

    python -m venv .venv
    source .venv/Scripts/activate
    pip install -r requirements.txt
    python src/extract.py
    python src/chunk.py
    python src/embed.py
    python src/query.py

For the free version, upload data/manual_chunks.json to a Google Colab notebook with a T4 GPU runtime and follow src/query_local_llm.py.

## Roadmap

- [x] Extract text from the owner's manual
- [x] Chunk and embed the manual content
- [x] Retrieval and generation pipeline
- [x] Free local-LLM alternative
- [ ] Measure and improve retrieval accuracy
- [ ] Command-line interface
- [ ] Tests

## Author

Keenen Thwala
