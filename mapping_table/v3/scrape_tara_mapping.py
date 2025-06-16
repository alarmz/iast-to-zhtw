
#!/usr/bin/env python3
"""
scrape_tara_mapping.py

Fetch the Wisely Lan blog page that contains the 108 Names of Tārā with
parallel Chinese and IAST lines, then build `tara_full_mapping.txt` suitable
for feeding into `build_mapping_from_parallel.py`.

Requirements:
    pip install requests beautifulsoup4

Usage:
    python scrape_tara_mapping.py --url <blog URL> --out tara_full_mapping.txt
"""

import re
import argparse
import requests
from bs4 import BeautifulSoup
from pathlib import Path

CHINESE_RE = re.compile(r"^[\u4e00-\u9fff].*?\(\d+\)")
IAST_RE    = re.compile(r"^[A-Za-zāīūṛṝṅñṭḍṇśṣṃ \-\.,'\(\)]+$")

def extract_pairs(url):
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    lines = [t.strip() for t in soup.get_text("\n").splitlines()]
    pairs = []
    i = 0
    while i < len(lines):
        zh = lines[i].strip()
        if CHINESE_RE.match(zh):
            # assume next non-empty line is IAST
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                iast = lines[j].strip()
                if IAST_RE.match(iast):
                    pairs.append((zh, iast))
                    i = j + 1
                    continue
        i += 1
    return pairs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="https://wiselylan619.pixnet.net/blog/post/318212661",
                    help="Source URL containing parallel lines")
    ap.add_argument("--out", default="tara_full_mapping.txt", help="Output mapping file")
    args = ap.parse_args()

    pairs = extract_pairs(args.url)
    out_path = Path(args.out)
    with out_path.open("w", encoding="utf-8") as f:
        for zh, iast in pairs:
            f.write(f"{zh} => {iast}\n")
    print(f"✓ Extracted {len(pairs)} pairs -> {out_path}")

if __name__ == "__main__":
    main()
