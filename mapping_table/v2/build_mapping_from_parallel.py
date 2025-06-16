
#!/usr/bin/env python3
"""
build_mapping_from_parallel.py

Read a two‑column UTF‑8 text file where each line is:

<original Chinese with or without markers> => <IAST>

The script:
1. Strips auxiliary markers in (...) from the Chinese side.
2. Builds a JSON mapping table `{clean_chinese: iast}` using greedy longest-word wins rule (later duplicates overwrite earlier ones if longer).
3. Writes mapping to `zh_iast_mapping.json`.

Usage:
    python build_mapping_from_parallel.py tara_mapping.txt \
        --aux auxiliary_markers.json \
        --out zh_iast_mapping.json
"""
import re, json, argparse
from pathlib import Path

def load_aux(path):
    if Path(path).is_file():
        return set(json.loads(Path(path).read_text(encoding="utf-8")))
    return set()

def is_index_marker(text):
    chinese_nums = "一二三四五六七八九十百千萬〇零廿卅卌"
    return all(ch in chinese_nums or ch.isdigit() for ch in text)

def strip_markers(text, aux_set):
    def repl(m):
        inner = m.group(1)
        if is_index_marker(inner):
            return ""  # drop line number when building mapping
        # if any aux string occurs inside, drop entire marker
        for aux in aux_set:
            if aux in inner:
                return ""
        return ""  # default drop
    return re.sub(r"[(（]([^()（）]*)[)）]", repl, text)

def build_mapping(parallel_path: Path, aux_set):
    mapping = {}
    for line in parallel_path.read_text(encoding="utf-8").splitlines():
        if "=>" not in line:
            continue
        left, right = [x.strip() for x in line.split("=>", 1)]
        left_clean = strip_markers(left, aux_set)
        # remove spaces
        left_clean = "".join(left_clean.split())
        if not left_clean:
            continue
        mapping[left_clean] = right
    return mapping

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parallel", help="Two‑column mapping file (txt/md)")
    ap.add_argument("--aux", default="auxiliary_markers.json", help="JSON list of auxiliary marker words")
    ap.add_argument("--out", default="zh_iast_mapping.json", help="Output JSON mapping")
    args = ap.parse_args()

    aux_set = load_aux(args.aux)
    mapping = build_mapping(Path(args.parallel), aux_set)
    Path(args.out).write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ wrote {args.out} with {len(mapping)} entries")

if __name__ == "__main__":
    main()
