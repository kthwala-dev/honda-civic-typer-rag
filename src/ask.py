from retrieve import retrieve


def main():
    print("Honda Civic Type R manual search. Type 'quit' to exit.\n")
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue
        for rank, chunk in enumerate(retrieve(question, n_results=3), start=1):
            print(f"\n[{rank}] pages {chunk['start_page']}-{chunk['end_page']}")
            print(chunk["text"][:700] + "...")
        print()


if __name__ == "__main__":
    main()