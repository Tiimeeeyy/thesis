import json
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MultiLabelBinarizer
from sentence_transformers import SentenceTransformer
from train_joint_model import get_amd_device, extract_mechanical_set, format_fused_view

def main():
    root_dir = Path(__file__).resolve().parent
    in_file = root_dir / "parsed_ygo_scripts.jsonl"
    trained_model_dir = root_dir / "ygo_joint_encoder"
    out_dir = root_dir / "embeddings"
    out_dir.mkdir(exist_ok=True)

    cards = [json.loads(line) for line in in_file.open("r", encoding="utf-8")]
    print(f"Loaded {len(cards)} cards.")

    # 1. Explicit Engine Multi-Hot Bitmasks (Categories, Types, Codes, Action Flow)
    token_lists = [list(extract_mechanical_set(c)) for c in cards]
    mlb = MultiLabelBinarizer()
    engine_multihot = mlb.fit_transform(token_lists).astype(np.float32)
    norms = np.linalg.norm(engine_multihot, axis=1, keepdims=True)
    engine_normed = np.divide(engine_multihot, norms, out=np.zeros_like(engine_multihot), where=norms != 0)

    # 2. Load Trained Bimodal Encoder (or fallback to base model if not trained yet)
    device = get_amd_device()
    model_path = str(trained_model_dir) if trained_model_dir.exists() else "microsoft/unixcoder-base"
    print(f"Encoding cards using {model_path} on {device}...")
    encoder = SentenceTransformer(model_path, device=device)

    # Encode full fused view (PSCT + Lua)
    fused_prompts = [format_fused_view(c) for c in cards]
    holistic_vecs = encoder.encode(fused_prompts, batch_size=32, show_progress_bar=True, normalize_embeddings=True)

    # Encode individual sub-effects to prevent 512-token truncation on 3-effect cards
    all_sub_effects = []
    card_effect_slices = []
    for c in cards:
        start = len(all_sub_effects)
        eff_strs = [e["canonical_effect_str"] for e in c.get("effects", [])]
        if not eff_strs:
            eff_strs = [c.get("psct_text") or c.get("name") or "NONE"]
        all_sub_effects.extend(eff_strs)
        card_effect_slices.append((start, len(all_sub_effects)))

    print(f"Encoding {len(all_sub_effects)} individual sub-effects...")
    sub_vecs = encoder.encode(all_sub_effects, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

    pooled_sub_vecs = np.zeros_like(holistic_vecs)
    for i, (start, end) in enumerate(card_effect_slices):
        mean_vec = np.mean(sub_vecs[start:end], axis=0)
        norm = np.linalg.norm(mean_vec)
        pooled_sub_vecs[i] = mean_vec / (norm + 1e-9)

    # Combine Holistic (50%) + Sub-Effect Pooled (30%) + Strict Engine Bitmask (20%)
    neural_combined = 0.625 * holistic_vecs + 0.375 * pooled_sub_vecs
    neural_combined /= np.linalg.norm(neural_combined, axis=1, keepdims=True) + 1e-9

    final_embeddings = np.hstack([neural_combined * 0.80, engine_normed * 0.20])
    final_embeddings /= np.linalg.norm(final_embeddings, axis=1, keepdims=True) + 1e-9

    np.save(out_dir / "card_embeddings.npy", final_embeddings)
    index_meta = [
        {"idx": i, "card_id": c["card_id"], "name": c.get("name", f"Card_{c['card_id']}")}
        for i, c in enumerate(cards)
    ]
    with (out_dir / "card_index.json").open("w", encoding="utf-8") as f:
        json.dump(index_meta, f, indent=2)

    print(f"Saved {final_embeddings.shape} hybrid embeddings to {out_dir / 'card_embeddings.npy'}")

if __name__ == "__main__":
    main()
