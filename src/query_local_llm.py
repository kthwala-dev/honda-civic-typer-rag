"""
Local, zero-cost RAG query pipeline using a small open-source LLM.

Designed to run in Google Colab (free T4 GPU) since it does not require
API billing or local GPU hardware.

Known limitation: retrieval occasionally surfaces an incorrect but nearby
chunk for entity-specific questions (e.g. a question about engine oil
returned coolant information instead). This is a common RAG failure mode
and a good candidate for future improvement (smaller chunk size, reduced
n_results, or a reranking step).
"""

import json
import chromadb
from transformers import pipeline
import torch

CHUNKS_FILE = "manual_chunks.json"
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


def load_chunks(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_collection(chunks: list[dict]):
    client = chromadb.Client()
    collection = client.create_collection(name="civic_manual")

    ids = [str(c["chunk_id"]) for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {"start_page": c["start_page"], "end_page": c["end_page"]}
        for c in chunks
    ]
    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return collection


def load_generator():
    return pipeline(
        "text-generation",
        model=MODEL_NAME,
        dtype=torch.bfloat16,
        device_map="auto",
    )


def build_prompt(question: str, chunks_text: list[str], metadatas: list[dict]) -> str:
    context_blocks = []
    for text, meta in zip(chunks_text, metadatas):
        pages = f"pages {meta['start_page']}-{meta['end_page']}"
        context_blocks.append(f"[{pages}]\n{text}")
    context = "\n\n---\n\n".join(context_blocks)

    return f"""You are a helpful assistant answering questions about a Honda Civic based only on the owner's manual excerpts below. If the excerpts don't contain the answer, say so clearly.

MANUAL EXCERPTS:
{context}

QUESTION:
{question}

Answer clearly and concisely, and mention which page(s) the answer came from."""


def ask(collection, generator, question: str, n_results: int = 4) -> str:
    results = collection.query(query_texts=[question], n_results=n_results)
    chunks_text = results["documents"][0]
    metadatas = results["metadatas"][0]

    prompt = build_prompt(question, chunks_text, metadatas)
    messages = [{"role": "user", "content": prompt}]
    output = generator(messages, max_new_tokens=300, do_sample=False)
    return output[0]["generated_text"][-1]["content"]


if __name__ == "__main__":
    chunks = load_chunks(CHUNKS_FILE)
    collection = build_collection(chunks)
    generator = load_generator()

    print("Honda Civic Manual Assistant (Colab / local LLM version)")
    print("Run this script inside a Google Colab notebook with a T4 GPU runtime.\n")

    example_answer = ask(collection, generator, "What is the recommended tyre pressure?")
    print(example_answer)
