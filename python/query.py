import sys
import json
import numpy as np
from pathlib import Path

def find_similar(query_name: str, top_k: int = 10):
    emb_dir = Path(__file__).resolve().parent / "embeddings"
    vecs_path = emb_dir / "card_embeddings.npy"
    idx_path = emb_dir / "card_index.json"

    if not vecs_path.exists() or not idx_path.exists():
        print(f"Embeddings not found in {emb_dir}. Run embed_cards.py first.")
        return

    vecs = np.load(vecs_path)
    with idx_path.open("r", encoding="utf-8") as f:
        meta = json.load(f)

    # Exact match first, then substring match
    exact = [m for m in meta if (m.get("name") or "").lower() == query_name.lower()]
    matches = exact or [m for m in meta if query_name.lower() in (m.get("name") or "").lower()]

    if not matches:
        print(f"Card '{query_name}' not found in index.")
        return

    target = matches[0]
    target_vec = vecs[target["idx"]]

    # Cosine similarity via dot product (vectors are L2-normalized)
    scores = vecs @ target_vec
    top_indices = np.argsort(scores)[::-1][1 : top_k + 1]

    print(f"\nTop {top_k} cards mechanically similar to [{target['name']}] (ID: {target['card_id']}):")
    for rank, idx in enumerate(top_indices, 1):
        print(f"  {rank:2d}. {meta[idx]['name']} (ID: {meta[idx]['card_id']}) — score: {scores[idx]:.4f}")

if __name__ == "__main__":
    card_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Ash Blossom & Joyous Spring"
    find_similar(card_query, top_k=10)
