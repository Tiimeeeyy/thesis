import re
import json
import sqlite3
from pathlib import Path
from tqdm import tqdm
from parse_lua import YGOLuaParser

CARD_FILE_RE = re.compile(r"^c(\d+)\.lua$")
DUEL_CALL_RE = re.compile(r"\b(Duel\.[A-Za-z0-9_]+|REASON_[A-Z0-9_]+|LOCATION_[A-Z0-9_]+|POS_[A-Z0-9_]+)\b")

def load_engine_constants(scripts_dir: Path) -> dict[str, str]:
    """Parses constant.lua, archetype_setcode_constants.lua, and card_counter_constants.lua."""
    hex_to_name = {}
    const_re = re.compile(r"^([A-Z0-9_]+)\s*=\s*(0x[0-9a-fA-F]+|\d+)")

    for fname in ["constant.lua", "archetype_setcode_constants.lua", "card_counter_constants.lua"]:
        for fpath in scripts_dir.rglob(fname):
            for line in fpath.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = re.sub(r"--.*$", "", line).strip()
                m = const_re.match(line)
                if m:
                    name, val = m.group(1), m.group(2)
                    if name.startswith(("SET_", "COUNTER_", "RACE_", "ATTRIBUTE_")):
                        hex_to_name[val.lower()] = name
    print(f"Loaded {len(hex_to_name)} engine hex constants.")
    return hex_to_name

def load_cdb_lookup(root_dir: Path) -> dict:
    cdb_files = list(root_dir.rglob("*.cdb"))
    card_db = {}
    for cdb_path in cdb_files:
        try:
            conn = sqlite3.connect(cdb_path)
            cur = conn.cursor()
            cur.execute("""
                SELECT d.id, t.name, t.desc, d.type, d.atk, d.def, d.level, d.race, d.attribute, d.setcode
                FROM datas d JOIN texts t ON d.id = t.id
            """)
            for row in cur.fetchall():
                cid, name, desc, ctype, atk, def_, level, race, attr, setcode = row
                card_db[cid] = {
                    "name": name,
                    "desc": desc,
                    "type": ctype,
                    "atk": atk,
                    "def": def_,
                    "level": level & 0xff,
                    "lscale": (level >> 24) & 0xff,
                    "rscale": (level >> 16) & 0xff,
                    "race": race,
                    "attribute": attr,
                    "setcode": setcode,
                }
            conn.close()
        except Exception:
            pass
    print(f"Loaded {len(card_db)} cards from {len(cdb_files)} .cdb file(s).")
    return card_db

def enrich_lua_code(code_block: str, helpers: dict, card_db: dict, hex_map: dict, self_id: int) -> str:
    if not code_block:
        return ""
    norm_code = re.sub(r"\bc\d+\.", "s.", code_block)
    inlined = [norm_code]
    visited = set()

    current_text = norm_code
    for _ in range(2):
        refs = set(re.findall(r"\bs\.[a-zA-Z0-9_]+\b", current_text))
        new_additions = []
        for ref in refs:
            if ref not in visited and ref in helpers and not current_text.startswith(f"function {ref}"):
                visited.add(ref)
                helper_body = re.sub(r"\bc\d+\.", "s.", helpers[ref])
                new_additions.append(f"-- [Filter/Helper: {ref}]\n{helper_body}")
        if not new_additions:
            break
        inlined.extend(new_additions)
        current_text = "\n".join(new_additions)

    full_code = "\n".join(inlined)

    # 1. Annotate hardcoded card passcodes with English names
    if card_db:
        def replace_id(m):
            num = int(m.group(1))
            if num == self_id:
                return "id --[[SELF_CARD]]"
            if num in card_db:
                return f"{num} --[[{card_db[num]['name']}]]"
            return m.group(0)
        full_code = re.sub(r"\b(\d{7,9})\b", replace_id, full_code)

    # 2. Annotate hex setcodes & counters
    if hex_map:
        def replace_hex(m):
            val = m.group(1).lower()
            return f"{m.group(1)} --[[{hex_map[val]}]]" if val in hex_map else m.group(0)
        full_code = re.sub(r"\b(0x[0-9a-fA-F]+)\b", replace_hex, full_code)

    return full_code

def build_embedding_document(parsed_card: dict, card_db: dict, hex_map: dict) -> dict:
    cid = parsed_card["card_id"]
    helpers = parsed_card["helper_functions"]
    cdb_info = card_db.get(cid, {})
    structured_effects = []

    for idx, eff in enumerate(parsed_card["effects"]):
        con_full = enrich_lua_code(eff["condition_code"], helpers, card_db, hex_map, cid)
        cost_full = enrich_lua_code(eff["cost_code"], helpers, card_db, hex_map, cid)
        tg_full = enrich_lua_code(eff["target_code"], helpers, card_db, hex_map, cid)
        op_full = enrich_lua_code(eff["operation_code"], helpers, card_db, hex_map, cid)

        combined_lua = "\n".join([con_full, cost_full, tg_full, op_full])
        action_flow = list(dict.fromkeys(DUEL_CALL_RE.findall(combined_lua)))

        canonical_lines = [
            f"[EFFECT {idx+1}]",
            f"TYPE: {', '.join(eff['effect_type']) or 'NONE'} | CAT: {', '.join(eff['categories']) or 'NONE'}",
            f"CODE: {', '.join(eff['codes']) or 'NONE'} | PROP: {', '.join(eff['properties']) or 'NONE'}",
            f"RANGE: {eff['range_loc'] or 'NONE'} | LIMIT: {eff['count_limit'] or 'NONE'}",
            f"FLOW: {' -> '.join(action_flow) or 'PASSIVE'}",
        ]
        if con_full:
            canonical_lines.append(f"-- CONDITION:\n{con_full}")
        if cost_full:
            canonical_lines.append(f"-- COST:\n{cost_full}")
        if tg_full:
            canonical_lines.append(f"-- TARGET:\n{tg_full}")
        if op_full:
            canonical_lines.append(f"-- OPERATION:\n{op_full}")

        structured_effects.append({
            "effect_index": idx,
            "metadata": {
                "type": eff["effect_type"],
                "categories": eff["categories"],
                "codes": eff["codes"],
                "properties": eff["properties"],
                "range": eff["range_loc"],
                "count_limit": eff["count_limit"],
                "action_flow": action_flow,
            },
            "canonical_effect_str": "\n".join(canonical_lines),
        })

    return {
        "card_id": cid,
        "name": cdb_info.get("name"),
        "psct_text": cdb_info.get("desc"),
        "stats": {k: v for k, v in cdb_info.items() if k not in ("name", "desc")} if cdb_info else {},
        "aux_procedures": parsed_card["aux_procedures"],
        "effects": structured_effects,
    }

def main():
    root_dir = Path(__file__).resolve().parent.parent
    scripts_dir = root_dir / "scripts"
    out_file = root_dir / "python" / "parsed_ygo_scripts.jsonl"

    search_dir = scripts_dir / "official" if (scripts_dir / "official").exists() else scripts_dir
    lua_files = sorted(f for f in search_dir.rglob("c*.lua") if CARD_FILE_RE.match(f.name))
    print(f"Found {len(lua_files)} card scripts in {search_dir}")

    hex_map = load_engine_constants(scripts_dir)
    card_db = load_cdb_lookup(root_dir)
    parser = YGOLuaParser()

    with out_file.open("w", encoding="utf-8") as f_out:
        for filepath in tqdm(lua_files, desc="Building enriched dataset"):
            try:
                parsed = parser.parse_file(filepath)
                doc = build_embedding_document(parsed, card_db, hex_map)
                f_out.write(json.dumps(doc) + "\n")
            except Exception as e:
                print(f"Error parsing {filepath.name}: {e}")

    print(f"Saved enriched dataset to {out_file}")

if __name__ == "__main__":
    main()
