from clean import clean
from pathlib import Path
import json
from pypdf import PdfReader

PDF_PATH = Path(__file__).parent.parent / "data" / "manual.pdf"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "manual_text.json"


def extract_pages(pdf_path: Path) -> list[dict]:
    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page_number": i + 1, "text": clean(text)})
    return pages


def main():
    if not PDF_PATH.exists():
        print(f"PDF not found at {PDF_PATH}")
        return

    pages = extract_pages(PDF_PATH)

    non_empty = [p for p in pages if p["text"]]
    print(f"Total pages: {len(pages)}")
    print(f"Pages with extractable text: {len(non_empty)}")
    print(f"Pages with no text (likely images/diagrams): {len(pages) - len(non_empty)}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print(f"Saved extracted text to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
