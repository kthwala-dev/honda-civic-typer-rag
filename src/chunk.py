from pathlib import Path
import json

INPUT_PATH = Path(__file__).parent.parent / "data" / "manual_text.json"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "manual_chunks.json"

CHUNK_SIZE = 500       # words per chunk
CHUNK_OVERLAP = 75     # words shared between consecutive chunks


def load_pages(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_full_text(pages: list[dict]) -> list[tuple[str, int]]:
    """Flatten all pages into a single list of (word, page_number) pairs."""
    words_with_pages = []
    for page in pages:
        for word in page["text"].split():
            words_with_pages.append((word, page["page_number"]))
    return words_with_pages


def chunk_text(words_with_pages: list[tuple[str, int]], size: int, overlap: int) -> list[dict]:
    chunks = []
    step = size - overlap
    for start in range(0, len(words_with_pages), step):
        window = words_with_pages[start:start + size]
        if not window:
            continue
        text = " ".join(w for w, _ in window)
        page_numbers = sorted(set(p for _, p in window))
        chunks.append({
            "chunk_id": len(chunks),
            "text": text,
            "start_page": page_numbers[0],
            "end_page": page_numbers[-1],
        })
        if start + size >= len(words_with_pages):
            break
    return chunks


def main():
    pages = load_pages(INPUT_PATH)
    words_with_pages = build_full_text(pages)
    chunks = chunk_text(words_with_pages, CHUNK_SIZE, CHUNK_OVERLAP)

    print(f"Total words in manual: {len(words_with_pages)}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Example chunk (first 100 chars): {chunks[0]['text'][:100]}...")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved chunks to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
