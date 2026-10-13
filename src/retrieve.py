from pathlib import Path
from functools import lru_cache
from collections import Counter
import math
import re
import chromadb

DB_PATH = Path(__file__).parent.parent / "data" / "chroma_db"
COLLECTION_NAME = "civic_manual"

STOPWORDS = set(
    "a an and are as at be by can do does for from how i in is it my of on or should that the this to what when where which who why will with you your use".split()
)


def get_collection():
    client = chromadb.PersistentClient(path=str(DB_PATH))
    return client.get_collection(COLLECTION_NAME)


def tokenize(text):
    words = re.findall(r"[a-z0-9\-]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


@lru_cache(maxsize=1)
def load_index():
    data = get_collection().get(include=["documents", "metadatas"])
    tokens = [tokenize(d) for d in data["documents"]]
    df = Counter()
    for t in tokens:
        df.update(set(t))
    return {
        "ids": data["ids"],
        "docs": data["documents"],
        "metas": data["metadatas"],
        "counts": [Counter(t) for t in tokens],
        "lengths": [len(t) for t in tokens],
        "df": df,
        "avgdl": sum(len(t) for t in tokens) / len(tokens),
    }


def bm25_rank(query, k=40, k1=1.5, b=0.75):
    index = load_index()
    terms = tokenize(query)
    n = len(index["ids"])
    scored = []
    for i, counts in enumerate(index["counts"]):
        score = 0.0
        for term in terms:
            tf = counts.get(term, 0)
            if tf == 0:
                continue
            df = index["df"][term]
            idf = math.log((n - df + 0.5) / (df + 0.5) + 1)
            denom = tf + k1 * (1 - b + b * index["lengths"][i] / index["avgdl"])
            score += idf * tf * (k1 + 1) / denom
        scored.append((score, i))
    scored.sort(reverse=True)
    return [i for score, i in scored[:k] if score > 0]


def semantic_rank(query, k=40):
    index = load_index()
    position = {cid: i for i, cid in enumerate(index["ids"])}
    result = get_collection().query(query_texts=[query], n_results=k)
    return [position[cid] for cid in result["ids"][0]]


def retrieve(query, n_results=4, mode="semantic", k=40, rrf_k=60):
    index = load_index()
    if mode == "semantic":
        ranked = semantic_rank(query, k)[:n_results]
    else:
        fused = {}
        for ranking in (semantic_rank(query, k), bm25_rank(query, k)):
            for rank, i in enumerate(ranking):
                fused[i] = fused.get(i, 0) + 1 / (rrf_k + rank + 1)
        ordered = sorted(fused.items(), key=lambda item: item[1], reverse=True)
        ranked = [i for i, score in ordered][:n_results]
    return [
        {
            "text": index["docs"][i],
            "start_page": index["metas"][i]["start_page"],
            "end_page": index["metas"][i]["end_page"],
        }
        for i in ranked
    ]