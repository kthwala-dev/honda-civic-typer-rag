# Honda Civic Type R RAG Assistant

A retrieval-augmented generation (RAG) system that answers questions about the Honda Civic Type R using the official owner's manual as its knowledge source.

## Status
🚧 In development — early stage.

## Goal
Load the owner's manual (PDF), split and embed its contents, store it in a vector database, and let a user ask natural-language questions (e.g. "What's the recommended tyre pressure?") and get accurate answers pulled directly from the manual.

## Planned Stack
- Python
- Anthropic Claude API
- ChromaDB (vector store)
- pypdf (PDF text extraction)

## Roadmap
- [ ] Extract and clean text from the owner's manual PDF
- [ ] Chunk and embed the manual content
- [ ] Build a basic retrieval + query pipeline
- [ ] Add a simple CLI or chat interface
- [ ] Write tests

## Author
Keenen Thwala
