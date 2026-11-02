import json
import random
import torch
from pathlib import Path
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer, InputExample, losses, models

def get_amd_device() -> str:
    """Detects AMD ROCm (via hip/cuda), Windows DirectML, or CPU."""
    if torch.cuda.is_available():
        dev_name = torch.cuda.get_device_name(0)
        print(f"Detected GPU via ROCm/CUDA: {dev_name}")
        return "cuda"
    try:
        import torch_directml
        dml = torch_directml.device()
        print(f"Detected AMD GPU via DirectML: {dml}")
        return str(dml)
    except ImportError:
        pass
    print("WARNING: No ROCm or DirectML GPU detected. Falling back to CPU.")
    return "cpu"

def extract_mechanical_set(card: dict) -> set[str]:
    """Extracts the complete set of discrete Lua engine behaviors for Jaccard similarity."""
    tokens = set()
    for proc in card.get("aux_procedures", []):
        tokens.add(f"PROC:{proc.split('.')[0].strip()}")
    for eff in card.get("effects", []):
        m = eff["metadata"]
        tokens.update(f"T:{x}" for x in m.get("type", []))
        tokens.update(f"C:{x}" for x in m.get("categories", []))
        tokens.update(f"E:{x}" for x in m.get("codes", []))
        tokens.update(f"P:{x}" for x in m.get("properties", []))
        tokens.update(f"F:{x}" for x in m.get("action_flow", []))
        if m.get("range"):
            tokens.add(f"R:{m['range']}")
    return tokens

def format_text_view(card: dict) -> str:
    s = card.get("stats", {})
    return (
        f"[CARD] {card.get('name', '')}\n"
        f"[STATS] Level {s.get('level', 0)} ATK {s.get('atk', 0)} DEF {s.get('def', 0)} "
        f"Race {s.get('race', 0)} Attr {s.get('attribute', 0)}\n"
        f"[PSCT] {card.get('psct_text', '')}"
    )

def format_lua_view(card: dict) -> str:
    procs = card.get("aux_procedures", [])
    effs = [e["canonical_effect_str"] for e in card.get("effects", [])]
    return "[LUA]\n" + "\n".join(procs + effs)

def format_fused_view(card: dict) -> str:
    return format_text_view(card) + "\n" + format_lua_view(card)

def build_training_data(jsonl_path: Path):
    cards = []
    mech_sets = []

    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            c = json.loads(line)
            if c.get("psct_text") and c.get("effects"):
                mset = extract_mechanical_set(c)
                if len(mset) >= 3:
                    cards.append(c)
                    mech_sets.append(mset)

    # 1. Cross-Modal Contrastive Pairs (InfoNCE)
    align_examples = []
    for c in cards:
        t_view = format_text_view(c)
        l_view = format_lua_view(c)
        f_view = format_fused_view(c)
        align_examples.append(InputExample(texts=[t_view, l_view]))
        align_examples.append(InputExample(texts=[f_view, l_view]))

    # 2. Continuous Mechanical Similarity Pairs (CoSENT / OASIS Order-Augmented Loss)
    # Samples card pairs and labels them with their exact Lua Jaccard similarity (0.0 to 1.0)
    cosent_examples = []
    n_cards = len(cards)
    rng = random.Random(42)

    for i in range(n_cards):
        # Sample 3 random comparisons per card to teach fine-grained mechanical distance
        for _ in range(3):
            j = rng.randrange(n_cards)
            if i == j:
                continue
            inter = len(mech_sets[i] & mech_sets[j])
            union = len(mech_sets[i] | mech_sets[j])
            jaccard = float(inter / union) if union > 0 else 0.0
            cosent_examples.append(
                InputExample(texts=[format_fused_view(cards[i]), format_fused_view(cards[j])], label=jaccard)
            )

    print(f"Prepared {len(align_examples)} bimodal pairs & {len(cosent_examples)} continuous mechanical pairs.")
    return align_examples, cosent_examples

def main():
    root_dir = Path(__file__).resolve().parent
    jsonl_path = root_dir / "parsed_ygo_scripts.jsonl"
    model_save_path = str(root_dir / "ygo_joint_encoder")

    device = get_amd_device()
    align_examples, cosent_examples = build_training_data(jsonl_path)

    # microsoft/unixcoder-base is specifically pre-trained on ASTs + bimodal Code/Text.
    # You can also use "BAAI/bge-base-en-v1.5".
    base_model_name = "microsoft/unixcoder-base"
    print(f"Initializing bimodal encoder from {base_model_name}...")
    word_emb = models.Transformer(base_model_name, max_seq_length=512)
    pooling = models.Pooling(word_emb.get_word_embedding_dimension(), pooling_mode="mean")
    model = SentenceTransformer(modules=[word_emb, pooling], device=device)

    # Batch size 16 fits comfortably in 8GB-12GB AMD VRAM
    align_loader = DataLoader(align_examples, shuffle=True, batch_size=16)
    cosent_loader = DataLoader(cosent_examples, shuffle=True, batch_size=16)

    align_loss = losses.MultipleNegativesRankingLoss(model=model)
    mech_order_loss = losses.CoSENTLoss(model=model)

    # Use AMP only when running on ROCm/CUDA
    use_amp = (device == "cuda")

    model.fit(
        train_objectives=[
            (align_loader, align_loss),
            (cosent_loader, mech_order_loss),
        ],
        epochs=3,
        warmup_steps=250,
        output_path=model_save_path,
        use_amp=use_amp,
        show_progress_bar=True,
    )
    print(f"Training complete! Saved model to {model_save_path}")

if __name__ == "__main__":
    main()
