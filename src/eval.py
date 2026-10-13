from retrieve import retrieve, load_index

TESTS = [
    ("What is the recommended tyre pressure?", "kpa"),
    ("How do I reset the maintenance light?", "maintenance minder"),
    ("What type of engine oil should I use?", "genuine motor oil 0w-20"),
    ("What coolant does the car use?", "antifreeze"),
    ("How do I pair my phone with Bluetooth?", "bluetooth"),
    ("How do I use the parking brake?", "parking brake"),
    ("How do I turn on cruise control?", "cruise control"),
    ("What does the tyre pressure warning light mean?", "tire pressure monitoring"),
    ("How do I use Apple CarPlay?", "carplay"),
    ("How do I jump start the car?", "jump start"),
    ("How do I change the wiper blades?", "wiper blade"),
    ("Where is the fuse box?", "fuse box"),
    ("What does the check engine light mean?", "malfunction indicator lamp"),
    ("How does adaptive cruise control work?", "adaptive cruise control"),
    ("What does collision mitigation braking do?", "collision mitigation"),
    ("How do I turn off traction control?", "vehicle stability assist"),
]


def check_keywords():
    docs = load_index()["docs"]
    for question, keyword in TESTS:
        count = sum(keyword in d.lower() for d in docs)
        if count == 0:
            print("BAD KEYWORD (not in manual):", keyword)
        elif count > 25:
            print("TOO COMMON:", keyword, "-", count, "chunks")


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
    check_keywords()
    for mode in ("semantic", "hybrid"):
        print(f"--- {mode} ---")
        for n in (2, 4, 6):
            hits = run(mode, n, verbose=(n == 4 and mode == "semantic"))
            print(f"n_results={n}: {hits}/{len(TESTS)}")


if __name__ == "__main__":
    main()