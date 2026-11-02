import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

@dataclass
class CardEffect:
    var_name: str
    effect_type: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    codes: List[str] = field(default_factory=list)
    properties: List[str] = field(default_factory=list)
    range_loc: Optional[str] = None
    count_limit: Optional[str] = None
    con_func_name: Optional[str] = None
    cost_func_name: Optional[str] = None
    tg_func_name: Optional[str] = None
    op_func_name: Optional[str] = None
    val_func_name: Optional[str] = None
    condition_code: Optional[str] = None
    cost_code: Optional[str] = None
    target_code: Optional[str] = None
    operation_code: Optional[str] = None

class YGOLuaParser:
    FUNC_START_RE = re.compile(r"^function\s+([a-zA-Z0-9_.:]+)\s*\((.*?)\)")
    SETTER_RE = re.compile(r"^[\s]*(\w+):Set(\w+)\((.*)\)\s*$")
    CREATE_EFFECT_RE = re.compile(r"(?:local\s+)?(\w+)\s*=\s*Effect\.CreateEffect")
    AUX_PROC_RE = re.compile(
        r"^[\s]*(Synchro|Xyz|Link|Fusion|Ritual|Pendulum|aux|Auxiliary)\.(Add\w+|Create\w+)\((.*)\)"
    )

    def strip_comments(self, code: str) -> str:
        lines = []
        for line in code.splitlines():
            line_clean = re.sub(r"--.*$", "", line).rstrip()
            if line_clean:
                lines.append(line_clean)
        return "\n".join(lines)

    def extract_functions(self, clean_code: str) -> Dict[str, str]:
        functions: Dict[str, str] = {}
        lines = clean_code.splitlines()
        current_func_name = None
        current_body = []
        depth = 0

        open_tokens = re.compile(r"\b(function|then|do|repeat)\b")
        close_tokens = re.compile(r"\b(end|until)\b")

        for line in lines:
            if current_func_name is None:
                m = self.FUNC_START_RE.match(line.strip())
                if m:
                    raw_name = m.group(1)
                    norm_name = re.sub(r"^c\d+\.", "s.", raw_name)
                    current_func_name = norm_name
                    current_body = [line]
                    depth = len(open_tokens.findall(line)) - len(close_tokens.findall(line))
                    if depth <= 0:
                        functions[current_func_name] = "\n".join(current_body)
                        current_func_name = None
            else:
                current_body.append(line)
                opens = len(open_tokens.findall(line))
                closes = len(close_tokens.findall(line))
                depth += opens - closes
                if depth <= 0:
                    functions[current_func_name] = "\n".join(current_body)
                    current_func_name = None

        return functions

    def _split_bitmask(self, expr: str) -> List[str]:
        return [tok.strip() for tok in re.split(r"[+|]", expr) if tok.strip()]

    def _normalize_func_ref(self, ref: str) -> str:
        return re.sub(r"^c\d+\.", "s.", ref.strip())

    def parse_file(self, filepath: Path) -> Dict:
        raw_code = filepath.read_text(encoding="utf-8", errors="ignore")
        clean_code = self.strip_comments(raw_code)
        functions = self.extract_functions(clean_code)

        card_id_match = re.search(r"c(\d+)", filepath.stem)
        card_id = int(card_id_match.group(1)) if card_id_match else filepath.stem

        init_body = functions.get("s.initial_effect", "")
        effects: Dict[str, CardEffect] = {}
        aux_procs: List[str] = []

        for line in init_body.splitlines():
            line_s = line.strip()

            aux_m = self.AUX_PROC_RE.match(line_s)
            if aux_m:
                aux_procs.append(line_s)
                continue

            ce_m = self.CREATE_EFFECT_RE.search(line_s)
            if ce_m:
                var_name = ce_m.group(1)
                effects[var_name] = CardEffect(var_name=var_name)
                continue

            set_m = self.SETTER_RE.match(line_s)
            if set_m:
                var_name, prop, arg = set_m.group(1), set_m.group(2), set_m.group(3)
                if var_name not in effects:
                    effects[var_name] = CardEffect(var_name=var_name)
                eff = effects[var_name]

                if prop == "Category":
                    eff.categories.extend(self._split_bitmask(arg))
                elif prop == "Type":
                    eff.effect_type.extend(self._split_bitmask(arg))
                elif prop == "Code":
                    eff.codes.extend(self._split_bitmask(arg))
                elif prop == "Property":
                    eff.properties.extend(self._split_bitmask(arg))
                elif prop == "Range":
                    eff.range_loc = arg.strip()
                elif prop == "CountLimit":
                    eff.count_limit = arg.strip()
                elif prop == "Condition":
                    eff.con_func_name = self._normalize_func_ref(arg)
                    eff.condition_code = functions.get(eff.con_func_name, arg)
                elif prop == "Cost":
                    eff.cost_func_name = self._normalize_func_ref(arg)
                    eff.cost_code = functions.get(eff.cost_func_name, arg)
                elif prop == "Target":
                    eff.tg_func_name = self._normalize_func_ref(arg)
                    eff.target_code = functions.get(eff.tg_func_name, arg)
                elif prop == "Operation":
                    eff.op_func_name = self._normalize_func_ref(arg)
                    eff.operation_code = functions.get(eff.op_func_name, arg)
                elif prop == "Value":
                    eff.val_func_name = self._normalize_func_ref(arg)

        return {
            "card_id": card_id,
            "aux_procedures": aux_procs,
            "effects": [asdict(e) for e in effects.values()],
            "helper_functions": {k: v for k, v in functions.items() if k != "s.initial_effect"},
        }
