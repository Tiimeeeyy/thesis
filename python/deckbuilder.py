import re
import sys
import json
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict

# Map YGOPro Lua SetCategory -> Trigger Event SetCode for mechanical combo chains
ACTION_TO_TRIGGER = {
    "CATEGORY_TOGRAVE": {"EVENT_TO_GRAVE", "EVENT_SUMMON_SUCCESS"},
    "CATEGORY_DECKDES": {"EVENT_TO_GRAVE"},
    "CATEGORY_HANDES": {"EVENT_TO_GRAVE", "EVENT_DISCARD"},
    "CATEGORY_DESTROY": {"EVENT_DESTROYED", "EVENT_TO_GRAVE", "EVENT_BATTLE_DESTROYED"},
    "CATEGORY_REMOVE": {"EVENT_REMOVE"},
    "CATEGORY_SPECIAL_SUMMON": {"EVENT_SPSUMMON_SUCCESS"},
    "CATEGORY_TOHAND": {"EVENT_TO_HAND", "EVENT_CUSTOM"},
    "CATEGORY_RELEASE": {"EVENT_RELEASE"},
}

# Bitmask constants from cards.cdb
TYPE_MONSTER = 0x1
TYPE_SPELL = 0x2
TYPE_TRAP = 0x4
TYPE_FUSION = 0x40
TYPE_SYNCHRO = 0x2000
TYPE_XYZ = 0x800000
TYPE_LINK = 0x4000000
EXTRA_DECK_MASK = TYPE_FUSION | TYPE_SYNCHRO | TYPE_XYZ | TYPE_LINK

class YGODeckBuilder:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.emb_dir = root_dir / "embeddings"
        self.jsonl_path = root_dir / "parsed_ygo_scripts.jsonl"

        print("Loading embeddings and parsed Lua metadata...")
        self.vecs = np.load(self.emb_dir / "card_embeddings.npy")
        self.cards = []
        self.id_to_idx = {}

        with self.jsonl_path.open("r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                c = json.loads(line)
                c["idx"] = idx
                self._extract_card_profile(c)
                self.cards.append(c)
                self.id_to_idx[c["card_id"]] = idx

        print(f"Indexed {len(self.cards)} cards with Lua mechanical profiles.")

    def _extract_card_profile(self, card: dict):
        """Extracts inputs (demands), outputs (actions/triggers), setcodes, and deck role."""
        cats, codes, types, props, flows, ranges = set(), set(), set(), set(), set(), set()
        raw_lua_chunks = []

        for eff in card.get("effects", []):
            m = eff["metadata"]
            cats.update(m.get("categories", []))
            codes.update(m.get("codes", []))
            types.update(m.get("type", []))
            props.update(m.get("properties", []))
            flows.update(m.get("action_flow", []))
            if m.get("range"):
                ranges.add(m["range"])
            raw_lua_chunks.append(eff.get("canonical_effect_str", ""))

        full_lua = "\n".join(raw_lua_chunks)

        # Extract hex setcodes mentioned in Lua filters: e.g. IsSetCard(0xdd)
        mentioned_setcodes = {
            int(h, 16) for h in re.findall(r"IsSetCard\(\s*(0x[0-9a-fA-F]+)", full_lua)
        }
        # Extract card's own 16-bit setcode chunks from cards.cdb
        own_setcode_raw = card.get("stats", {}).get("setcode", 0) or 0
        own_setcodes = set()
        for shift in (0, 16, 32, 48):
            chunk = (own_setcode_raw >> shift) & 0xFFFF
            if chunk:
                own_setcodes.add(chunk)

        # Extract mentioned card IDs in Lua
        mentioned_ids = {
            int(cid) for cid in re.findall(r"\b(\d{7,9})\b", full_lua)
        }

        # Classify mechanical deckbuilding roles from Lua flags
        roles = set()
        ctype = card.get("stats", {}).get("type", 0) or 0
        is_extra = bool(ctype & EXTRA_DECK_MASK)

        if ("CATEGORY_SEARCH" in cats or "CATEGORY_TOHAND" in cats) and not is_extra:
            if "EVENT_SUMMON_SUCCESS" in codes or "EVENT_SPSUMMON_SUCCESS" in codes or "EFFECT_TYPE_IGNITION" in types or "EFFECT_TYPE_ACTIVATE" in types:
                roles.add("starter")
        if "CATEGORY_SPECIAL_SUMMON" in cats and ("LOCATION_HAND" in ranges or "LOCATION_GRAVE" in ranges or "EFFECT_TYPE_IGNITION" in types):
            roles.add("extender")
        if "CATEGORY_TOGRAVE" in cats or "CATEGORY_DECKDES" in cats or "REASON_COST" in flows:
            roles.add("gy_setup")
        if ("CATEGORY_NEGATE" in cats or "CATEGORY_DISABLE" in cats or "EFFECT_TYPE_QUICK_O" in types) and (
            "LOCATION_MZONE" in ranges or "LOCATION_HAND" in ranges or (ctype & TYPE_TRAP)
        ):
            roles.add("disruption")
        if is_extra or (card.get("stats", {}).get("atk", 0) >= 2500 and (ctype & TYPE_MONSTER)):
            roles.add("boss_payoff")

        card["profile"] = {
            "cats": cats,
            "codes": codes,
            "types": types,
            "props": props,
            "flows": flows,
            "ranges": ranges,
            "own_setcodes": own_setcodes,
            "mentioned_setcodes": mentioned_setcodes,
            "mentioned_ids": mentioned_ids,
            "roles": roles,
            "is_extra": is_extra,
        }

    def find_card(self, query_name: str) -> dict:
        exact = [c for c in self.cards if (c.get("name") or "").lower() == query_name.lower()]
        matches = exact or [c for c in self.cards if query_name.lower() in (c.get("name") or "").lower()]
        if not matches:
            raise ValueError(f"Card '{query_name}' not found.")
        return matches[0]

    def compute_synergy_score(self, seed: dict, cand: dict, cos_sim: float) -> tuple[float, list[str]]:
        """Computes a multi-factor deckbuilding synergy score between a seed card and a candidate."""
        if seed["card_id"] == cand["card_id"]:
            return -1.0, []

        sp, cp = seed["profile"], cand["profile"]
        ss, cs = seed.get("stats", {}), cand.get("stats", {})
        reasons = []
        bonus = 0.0

        # 1. Direct ID mention in Lua script (Highest priority combo piece)
        if cand["card_id"] in sp["mentioned_ids"] or seed["card_id"] in cp["mentioned_ids"]:
            bonus += 0.45
            reasons.append("Direct Name Mention")

        # 2. Archetype / Setcode handshake (Own <-> Mentioned or Shared Setcode)
        shared_arch = (sp["own_setcodes"] & cp["own_setcodes"]) | (sp["mentioned_setcodes"] & cp["own_setcodes"]) | (cp["mentioned_setcodes"] & sp["own_setcodes"])
        if shared_arch:
            bonus += 0.30
            reasons.append("Shared Archetype")

        # 3. Mechanical Action -> Trigger Handshake (Seed triggers Candidate or Candidate triggers Seed)
        for cat, trig_codes in ACTION_TO_TRIGGER.items():
            if cat in sp["cats"] and (cp["codes"] & trig_codes):
                bonus += 0.12
                reasons.append(f"Seed {cat.replace('CATEGORY_', '')} -> Cand Trigger")
                break
        for cat, trig_codes in ACTION_TO_TRIGGER.items():
            if cat in cp["cats"] and (sp["codes"] & trig_codes):
                bonus += 0.12
                reasons.append(f"Cand {cat.replace('CATEGORY_', '')} -> Seed Trigger")
                break

        # 4. Monster Race & Attribute Compatibility (for tribal/type locks)
        if ss.get("race") and ss.get("race") == cs.get("race"):
            bonus += 0.06
            reasons.append("Same Type/Race")
        if ss.get("attribute") and ss.get("attribute") == cs.get("attribute"):
            bonus += 0.04
            reasons.append("Same Attribute")

        # 5. Level / Rank / Scale alignment (e.g. same level for Xyz/Synchro engines)
        if ss.get("level") and ss.get("level") == cs.get("level") and (ss.get("type", 0) & TYPE_MONSTER) and (cs.get("type", 0) & TYPE_MONSTER):
            bonus += 0.05
            reasons.append(f"Matching Level/Rank ({ss['level']})")

        total_score = (0.55 * float(cos_sim)) + bonus
        return total_score, reasons

    def query_by_role(self, seed_name: str, role: str, top_k: int = 10):
        seed = self.find_card(seed_name)
        cos_scores = self.vecs @ self.vecs[seed["idx"]]

        results = []
        for cand in self.cards:
            if cand["card_id"] == seed["card_id"]:
                continue
            if role not in cand["profile"]["roles"]:
                continue
            syn_score, reasons = self.compute_synergy_score(seed, cand, cos_scores[cand["idx"]])
            results.append((syn_score, float(cos_scores[cand["idx"]]), cand, reasons))

        results.sort(key=lambda x: x[0], reverse=True)
        print(f"\n=== Top {top_k} [{role.upper()}] cards for [{seed['name']}] ===")
        for rank, (syn, cos, cand, reasons) in enumerate(results[:top_k], 1):
            r_str = ", ".join(reasons) if reasons else "Vector Mechanics"
            print(f"  {rank:2d}. {cand['name']} (Synergy: {syn:.3f} | EmbSim: {cos:.3f}) — [{r_str}]")

    def build_deck_core(self, seed_names: list[str]):
        seeds = [self.find_card(name) for name in seed_names]
        seed_ids = {s["card_id"] for s in seeds}

        # Average embedding of the seed cards as our semantic centroid
        centroid = np.mean([self.vecs[s["idx"]] for s in seeds], axis=0)
        centroid /= np.linalg.norm(centroid) + 1e-9
        cos_scores = self.vecs @ centroid

        scored_Pool = []
        for cand in self.cards:
            if cand["card_id"] in seed_ids or not cand.get("name"):
                continue
            # Take best synergy across any of the seed cards
            best_syn, best_reasons = -1.0, []
            for s in seeds:
                syn, r = self.compute_synergy_score(s, cand, cos_scores[cand["idx"]])
                if syn > best_syn:
                    best_syn, best_reasons = syn, r
            scored_Pool.append((best_syn, float(cos_scores[cand["idx"]]), cand, best_reasons))

        scored_Pool.sort(key=lambda x: x[0], reverse=True)

        # Bucket into functional deckbuilding categories
        buckets = {
            "1. Archetype & Direct Support": [],
            "2. Starters & Consistency (Searchers)": [],
            "3. Extenders & Combo Enablers": [],
            "4. GY / Banish / Trigger Synergy": [],
            "5. Extra Deck & Boss Payoffs": [],
            "6. In-Engine Disruption": [],
        }

        used_ids = set(seed_ids)

        def assign_bucket(item, key, limit):
            syn, cos, cand, reasons = item
            if cand["card_id"] not in used_ids and len(buckets[key]) < limit:
                buckets[key].append(item)
                used_ids.add(cand["card_id"])
                return True
            return False

        for item in scored_Pool[:250]:
            syn, cos, cand, reasons = item
            roles = cand["profile"]["roles"]
            is_arch = any("Archetype" in r or "Mention" in r for r in reasons)

            if is_arch and assign_bucket(item, "1. Archetype & Direct Support", 8):
                continue
            if cand["profile"]["is_extra"] and assign_bucket(item, "5. Extra Deck & Boss Payoffs", 6):
                continue
            if "starter" in roles and assign_bucket(item, "2. Starters & Consistency (Searchers)", 6):
                continue
            if "extender" in roles and assign_bucket(item, "3. Extenders & Combo Enablers", 6):
                continue
            if any("->" in r for r in reasons) and assign_bucket(item, "4. GY / Banish / Trigger Synergy", 6):
                continue
            if "disruption" in roles and assign_bucket(item, "6. In-Engine Disruption", 5):
                continue

        seed_titles = ", ".join(s["name"] for s in seeds)
        print(f"\n" + "=" * 75)
        print(f"RECOMMENDED DECK CORE & SYNERGY PACKAGE FOR: [{seed_titles}]")
        print("=" * 75)

        for section, items in buckets.items():
            print(f"\n### {section}:")
            if not items:
                print("  (No strong matches found)")
            for syn, cos, cand, reasons in items:
                role_tags = "/".join(sorted(cand["profile"]["roles"])) or "utility"
                why = ", ".join(reasons) if reasons else "High Mechanical Similarity"
                print(f"  • {cand['name']:<38} [{role_tags:<18}] (Score: {syn:.3f}) -> {why}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-grained YGO Synergy & Deck Core Builder")
    parser.add_argument("--cards", nargs="+", default=["Snake-Eye Ash"], help="One or more seed card names")
    parser.add_argument("--role", type=str, default=None, choices=["starter", "extender", "gy_setup", "disruption", "boss_payoff"],
                        help="Filter specifically by a mechanical role")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent
    builder = YGODeckBuilder(root_dir)

    if args.role:
        builder.query_by_role(args.cards[0], args.role, top_k=12)
    else:
        builder.build_deck_core(args.cards)
