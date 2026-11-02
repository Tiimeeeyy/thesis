import argparse
import time
import torch
from pathlib import Path

import build_dataset
import train_joint_model
import embed_cards
import query

def verify_rocm():
    print("=" * 60)
    print("1. HARDWARE & ROCm CHECK")
    print("=" * 60)
    print(f"PyTorch Version : {torch.__version__}")
    print(f"ROCm / GPU Avail: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"AMD GPU Device  : {torch.cuda.get_device_name(0)}")
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        print(f"Total VRAM      : {vram_gb:.2f} GB")
    else:
        print("WARNING: GPU not detected! Training will run on CPU.")
        print("If using an older/consumer Radeon GPU, try setting HSA_OVERRIDE_GFX_VERSION.")
    print()

def main():
    parser = argparse.ArgumentParser(description="Run the full YGO Lua + PSCT embedding pipeline.")
    parser.add_argument("--skip-parse", action="store_true", help="Skip parsing Lua scripts if JSONL exists.")
    parser.add_argument("--skip-train", action="store_true", help="Skip contrastive model training.")
    parser.add_argument("--skip-embed", action="store_true", help="Skip generating final card embeddings.")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent
    jsonl_file = root_dir / "parsed_ygo_scripts.jsonl"

    start_time = time.time()
    verify_rocm()

    # Step 1: Parse Lua scripts + cards.cdb
    if not args.skip_parse or not jsonl_file.exists():
        print("=" * 60)
        print("2. PARSING LUA SCRIPTS & JOINING CARDS.CDB")
        print("=" * 60)
        build_dataset.main()
        print()
    else:
        print(f"[Skipping Parse] Found existing {jsonl_file.name}\n")

    # Step 2: Train Joint Contrastive & Mechanical Encoder
    if not args.skip_train:
        print("=" * 60)
        print("3. TRAINING JOINT PSCT + LUA ENCODER")
        print("=" * 60)
        train_joint_model.main()
        print()
    else:
        print("[Skipping Training]\n")

    # Step 3: Generate Hybrid Embeddings
    if not args.skip_embed:
        print("=" * 60)
        print("4. GENERATING HYBRID CARD EMBEDDINGS")
        print("=" * 60)
        embed_cards.main()
        print()
    else:
        print("[Skipping Embedding Generation]\n")

    # Step 4: Quick Sanity Check
    print("=" * 60)
    print("5. RUNNING SANITY CHECK QUERIES")
    print("=" * 60)
    for test_card in ["Ash Blossom & Joyous Spring", "Pot of Prosperity", "Infinite Impermanence"]:
        try:
            query.find_similar(test_card, top_k=5)
        except Exception as e:
            print(f"Query test skipped for {test_card}: {e}")

    elapsed = (time.time() - start_time) / 60
    print(f"\nPipeline finished in {elapsed:.1f} minutes!")

if __name__ == "__main__":
    main()
