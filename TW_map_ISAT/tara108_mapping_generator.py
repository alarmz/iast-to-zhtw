
"""
tara108_mapping_generator.py

Generate mapping file where each line is:

中文音註 => IAST

Steps:
1. Fill CHINESE_LINES and IAST_LINES with 108 items each (same order).
2. Run `python tara108_mapping_generator.py`.
3. Get UTF‑8 `tara_108_mapping.txt` and `tara_108_mapping.md`.

"""

from pathlib import Path

# ---------------------------------------------------------------------------
# 1.  Put your full 108‑item lists here.
# ---------------------------------------------------------------------------
CHINESE_LINES = [
    # "唵(引)…帝惹",
    # "路(去引)…野捨(引上)",
    # ...
]

IAST_LINES = [
    # "oṃ śrī kāryāṇi mahā-teja",
    # "lokadhātu mahā-yaśas",
    # ...
]

assert len(CHINESE_LINES) == len(IAST_LINES), \
    "CHINESE_LINES and IAST_LINES must have the same length!"

def write_files(base_dir: Path = Path(".")):
    txt_path = base_dir / "tara_108_mapping.txt"
    md_path  = base_dir / "tara_108_mapping.md"

    with txt_path.open("w", encoding="utf-8") as f_txt, \
         md_path.open("w", encoding="utf-8") as f_md:

        # Markdown header
        f_md.write("# 108 Names of Tārā – 中文 => IAST 對照\n\n")

        # Write lines
        for idx, (chn, iast) in enumerate(zip(CHINESE_LINES, IAST_LINES), start=1):
            line_txt = f"{idx:02d}. {chn} => {iast}\\n"
            f_txt.write(line_txt)

            line_md  = f"{idx}. `{chn}` => **{iast}**\\n\\n"
            f_md.write(line_md)

    print(f"✓ Wrote {txt_path}")
    print(f"✓ Wrote {md_path}")

if __name__ == "__main__":
    write_files()
