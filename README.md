# Honda Civic Type R RAG Assistant

A retrieval-augmented generation (RAG) system that answers questions about the Honda Civic Type R using the official owner's manual as its knowledge source.

## Status

Working end to end. Retrieval scores 15/16 on a 16-question test set, with one documented failure. A command-line search tool runs locally, and a Colab notebook adds answer generation with a free open-source model.

## What it does

Given a natural-language question such as "What is the recommended tyre pressure?", the system finds the most relevant excerpts from the 787-page owner's manual. The command-line tool prints those excerpts with page numbers. The Colab notebook goes one step further and writes an answer from them, citing the pages.

## How it works

1. Extraction and cleaning: the PDF is parsed page by page with pypdf (src/extract.py), and Honda's repeated print-file header is stripped from every page (src/clean.py)
2. Chunking: the text is split into overlapping chunks of about 500 words, ignoring page boundaries (src/chunk.py)
3. Embedding and storage: chunks are embedded and stored in a local ChromaDB vector database (src/embed.py)
4. Retrieval: a question is matched against the stored chunks by meaning (src/retrieve.py)
5. Generation (optional): the best matches are passed to a language model that writes the answer (Colab notebook)

## Ways to use it

- src/ask.py is a command-line search tool. It runs locally and prints the three most relevant excerpts with page numbers. No language model and no API key.
- notebooks/civic_rag_colab.ipynb adds answer generation using an open-source model (Qwen2.5-3B-Instruct) on Colab's free T4 GPU. No API key and no local install.

## Stack

- Python
- pypdf
- ChromaDB
- Hugging Face Transformers (Qwen2.5-3B-Instruct, in the notebook)
- Google Colab (free GPU)

## Retrieval results

Retrieval is checked by src/eval.py. A question passes if the retrieved text contains an expected phrase from the manual.

Current result, after cleaning (323 chunks): semantic search at 4 results scores 15/16 on a 16-question set. Five of those questions use phrases that appear in 30 to 50 chunks, so they are easy passes. On the 11 stricter questions the score is 10/11. Hybrid search (semantic plus BM25 keyword, rank fusion) scored 14/16, so semantic search is the default.

Experiments:

- 200-word chunks: 6/8 against 7/8 for 500-word chunks on the original 8-question set, no improvement
- Hybrid search: 6/8 against 7/8 on the same set, worse
- Layout-aware PDF extraction: tested on the failing page, columns were still interleaved and the output was reported as incomplete, so it was not adopted
- Stripping Honda's repeated page header: removed about 7,850 words (about 5% of the text), kept the 4-result score at 15/16 and raised the 2-result score from 12/16 to 14/16, so it was adopted (src/clean.py)

## Known limitations

- The engine oil question fails. The answer is in a multi-column specifications table (page 765). Extraction interleaves the columns, so in testing the relevant chunk ranked 12th by meaning and 20th by keyword. Table-aware extraction is planned as future work.
- In the Colab notebook the failure is quiet: the model answers from the general guidance it retrieved, citing API grade SN, but leaves out the specific 0W-20 viscosity. The notebook prints the retrieved page ranges so an answer can be checked against the source.
- The manual PDF and everything derived from it (extracted text, chunks, vector database) are excluded from this repository because the manual is Honda's copyrighted material. To run the project, place your own copy at data/manual.pdf.

## Setup

    python -m venv .venv
    source .venv/Scripts/activate
    pip install -r requirements.txt
    python src/extract.py
    python src/chunk.py
    python src/embed.py
    python src/ask.py

To measure retrieval, run python src/eval.py. For generated answers, upload data/manual_chunks.json to notebooks/civic_rag_colab.ipynb in Google Colab with a T4 GPU runtime.

## Roadmap

- [x] Extract and clean text from the owner's manual
- [x] Chunk and embed the manual content
- [x] Retrieval with a measured evaluation set
- [x] Command-line search
- [x] Free answer generation in Colab
- [ ] Table-aware extraction for specification tables
- [ ] Support for multiple car models

## Author

Keenen Thwala