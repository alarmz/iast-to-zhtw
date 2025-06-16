
#!/usr/bin/env python3
"""
zh_to_iast_table.py  (v2)

Table‑driven Chinese → IAST converter.
Supports external auxiliary marker list loaded from JSON.

See README in code comments.
"""
import re, json, argparse
from pathlib import Path

def load_aux(path):
    if Path(path).is_file():
        return set(json.loads(Path(path).read_text(encoding="utf-8")))
    return set()

def load_mapping(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def is_index_marker(text: str) -> bool:
    chinese_nums = "一二三四五六七八九十百千萬〇零廿卅卌"
    return all(ch in chinese_nums or ch.isdigit() for ch in text)

def clean_line(line: str, aux_set):
    index_marker = ""
    def repl(m):
        nonlocal index_marker
        inner = m.group(1)
        if is_index_marker(inner):
            index_marker = inner
            return f"({inner})"
        for aux in aux_set:
            if aux in inner:
                return ""
        return ""
    cleaned = re.sub(r"[(（]([^()（）]*)[)）]", repl, line)
    return cleaned.strip(), index_marker

def tokenize(text: str):
    return re.findall(r"[\u4e00-\u9fff]+", text)

def lookup_iast(tokens, mapping):
    out = []
    i = 0
    while i < len(tokens):
        matched = False
        for n in (3, 2, 1):
            if i + n <= len(tokens):
                segment = "".join(tokens[i:i+n])
                if segment in mapping:
                    out.append(mapping[segment])
                    i += n
                    matched = True
                    break
        if not matched:
            seg = tokens[i]
            out.append(mapping.get(seg, seg))
            i += 1
    return " ".join(filter(None, out)).strip()

def process(src_path, mapping, aux_set, out_txt, out_md):
    with Path(src_path).open(encoding="utf-8") as f_in, \
         Path(out_txt).open("w", encoding="utf-8") as f_txt, \
         Path(out_md).open("w", encoding="utf-8") as f_md:

        f_md.write("# Chinese ⇒ IAST Mapping\n\n")
        for idx, raw in enumerate(f_in, start=1):
            raw = raw.strip()
            if not raw:
                continue
            cleaned, _ = clean_line(raw, aux_set)
            tokens = tokenize(cleaned)
            iast = lookup_iast(tokens, mapping)
            out_line = f"{cleaned} => {iast}\n"
            f_txt.write(out_line)
            f_md.write(f"{idx}. `{cleaned}` => **{iast}**\n\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input .txt with Chinese phonetic lines")
    ap.add_argument("--map", default="zh_iast_mapping.json", help="JSON mapping file")
    ap.add_argument("--aux", default="auxiliary_markers.json", help="Auxiliary markers JSON")
    ap.add_argument("--out", default="mapping.txt", help="Output txt file")
    args = ap.parse_args()

    mapping = load_mapping(args.map)
    aux_set = load_aux(args.aux)
    process(args.input, mapping, aux_set, args.out, Path(args.out).with_suffix(".md"))
    print(f"✓ wrote {args.out} and {Path(args.out).with_suffix('.md')}")

if __name__ == "__main__":
    main()
