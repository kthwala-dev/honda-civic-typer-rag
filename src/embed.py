from pathlib import Path
import json
import chromadb

CHUNKS_PATH = Path(__file__).parent.parent / "data" / "manual_chunks.json"
DB_PATH = Path(__file__).parent.parent / "data" / "chroma_db"

COLLECTION_NAME = "civic_manual"


def load_chunks(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    chunks = load_chunks(CHUNKS_PATH)
    print(f"Loaded {len(chunks)} chunks")

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Start fresh each time this script runs
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    ids = [str(c["chunk_id"]) for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {"start_page": c["start_page"], "end_page": c["end_page"]}
        for c in chunks
    ]

    # Chroma embeds automatically using its default embedding model
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    print(f"Stored {collection.count()} chunks in ChromaDB at {DB_PATH}")


if __name__ == "__main__":
    main()
