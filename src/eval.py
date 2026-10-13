from retrieve import retrieve

TESTS = [
    ("What is the recommended tyre pressure?", "kpa"),
    ("How do I reset the maintenance light?", "maintenance minder"),
    ("What type of engine oil should I use?", "genuine motor oil 0w-20"),
    ("What coolant does the car use?", "antifreeze"),
    ("How do I pair my phone with Bluetooth?", "bluetooth"),
    ("How do I use the parking brake?", "parking brake"),
    ("How do I turn on cruise control?", "cruise control"),
    ("What does the tyre pressure warning light mean?", "tire pressure monitoring"),
]


def run(mode, n_results, verbose):
    hits = 0
    for question, keyword in TESTS:
        chunks = retrieve(question, n_results=n_results, mode=mode)
        found = any(keyword in c["text"].lower() for c in chunks)
        hits += found
        if verbose:
            print(("PASS" if found else "FAIL"), "-", question)
    return hits


def main():
    for mode in ("semantic", "hybrid"):
        print(f"--- {mode} ---")
        for n in (2, 4, 6):
            hits = run(mode, n, verbose=(n == 4))
            print(f"n_results={n}: {hits}/{len(TESTS)}")


if __name__ == "__main__":
    main()