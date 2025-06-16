
#!/usr/bin/env python3
"""
zh_to_iast_table.py

Convert Chinese phonetic notation lines with auxiliary markers into IAST using a
table‑driven approach.

Usage:
    python zh_to_iast_table.py input.txt --map mapping.json --out mapping.txt

Output:
    Produces both .txt and .md mapping files with format:
        <cleaned Chinese> => <IAST>

The script ignores auxiliary markers like (引)、(上)、(二合) … but keeps the
final sequence number marker (e.g. (一)).
"""

import re
import json
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

AUX_MARKERS = [
    "引", "上", "去", "入", "平",
    "二合", "三合", "四合",
    "轉舌", "准", "反", "呼",
    "引上", "引去", "上引", "去引",
    "無鉢反轉舌", "切身引"
]

def load_mapping(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def is_index_marker(text: str) -> bool:
    """Return True if text inside parentheses is a Chinese numeral or digit."""
    chinese_nums = "一二三四五六七八九十百千萬〇零廿卅卌"
    return all(ch in chinese_nums or ch.isdigit() for ch in text)

def clean_line(line: str) -> tuple[str, str]:
    """
    Remove auxiliary markers in parentheses but keep index marker.

    Returns:
        cleaned_line, index_marker ('' if none)
    """
    index_marker = ""
    def repl(m):
        nonlocal index_marker
        inner = m.group(1)
        # keep line numbers
        if is_index_marker(inner):
            index_marker = inner
            return f"({inner})"
        # drop auxiliary markers
        return ""

    cleaned = re.sub(r"[(（]([^()（）]*)[)）]", repl, line)
    return cleaned.strip(), index_marker

def tokenize(text: str) -> list[str]:
    """Split into consecutive Han blocks (ignoring punctuation/spaces)."""
    return re.findall(r"[\u4e00-\u9fff]+", text)

def lookup_iast(tokens: list[str], mapping: dict) -> str:
    """
    Resolve IAST by greedy longest‑match lookup in mapping table.
    """
    out = []
    i = 0
    while i < len(tokens):
        matched = False
        # try trigram, bigram, unigram
        for n in (3, 2, 1):
            if i + n <= len(tokens):
                segment = "".join(tokens[i:i+n])
                if segment in mapping:
                    out.append(mapping[segment])
                    i += n
                    matched = True
                    break
        if not matched:
            # fallback: individual characters
            seg = tokens[i]
            out.append(mapping.get(seg, seg))
            i += 1
    return " ".join(filter(None, out)).strip()

def process_file(src_path: Path, mapping: dict, out_txt: Path, out_md: Path):
    with src_path.open(encoding="utf-8") as f_in, \
         out_txt.open("w", encoding="utf-8") as f_txt, \
         out_md.open("w", encoding="utf-8") as f_md:

        f_md.write("# Chinese ⇒ IAST Mapping\n\n")
        for line_num, raw in enumerate(f_in, start=1):
            raw = raw.strip()
            if not raw:
                continue
            cleaned, _ = clean_line(raw)
            tokens = tokenize(cleaned)
            iast = lookup_iast(tokens, mapping)
            out_line = f"{cleaned} => {iast}\n"
            f_txt.write(out_line)
            f_md.write(f"{line_num}. `{cleaned}` => **{iast}**\n\n")

def main():
    ap = argparse.ArgumentParser(description="Chinese → IAST converter (table driven)")
    ap.add_argument("input", help="Input text file with Chinese phonetic lines")
    ap.add_argument("--map", default="zh_iast_mapping.json", help="JSON mapping file")
    ap.add_argument("--out", default="mapping.txt", help="Output txt file")
    args = ap.parse_args()

    src_path = Path(args.input)
    map_path = Path(args.map)
    out_txt = Path(args.out)
    out_md  = out_txt.with_suffix(".md")

    mapping = load_mapping(map_path)
    process_file(src_path, mapping, out_txt, out_md)
    print(f"✓ Wrote {out_txt}")
    print(f"✓ Wrote {out_md}")

if __name__ == "__main__":
    main()
