
"""
tara108_iast_generator.py

Utility script to generate UTF‑8 `.txt` and `.md` files for the 108 names of Tārā
in IAST.  The list is defined inside this file – extend it to all 108 names as
needed.

Run:
    python tara108_iast_generator.py
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# 1.  Fill in / extend this list to the complete 108‑item sequence.
# ---------------------------------------------------------------------------
IAST_NAMES = [
    "oṃ śrī kāryāṇi mahā-teja loka-dhātṛ",
    "mahā-yaśas",
    "sarasvatī",
    "viśā-rakṣī",
    "prajñā",
    "śrī",
    "buddhi",
    "vardhanī",
    "dhṛtinā",
    "puṣṭinā",
    "svāhā",
    "oṃkārā",
    "kāmarūpiṇī",
    "sarva-sattva-hitodyuktā",
    "saṃgrāmottaraṇī",
    "jayā",
    "prajñāpāramitā-devī",
    "ārya-tārā",
    "manoramā",
    "dundubhi",
    "śaṅkhinī",
    "pūrṇā",
    "vidyā-rājñī",
    "priyamvadā",
    "candrānanā",
    "mahā-gaurī",
    "ajitā",
    "pīta-vāsasā",
    "mahā-māyā",
    "mahā-śvetā",
    # ... add the remaining 78 names here ...
]

def write_files(base_dir: Path = Path(".")):
    txt_path = base_dir / "tara_108_iast.txt"
    md_path  = base_dir / "tara_108_iast.md"

    # Write plain‑text
    with txt_path.open("w", encoding="utf-8") as f_txt:
        for idx, name in enumerate(IAST_NAMES, start=1):
            f_txt.write(f"{idx:02d}. {name}\n")

    # Write Markdown
    with md_path.open("w", encoding="utf-8") as f_md:
        f_md.write("# 108 Names of Tārā (IAST)\n\n")
        for idx, name in enumerate(IAST_NAMES, start=1):
            f_md.write(f"{idx}. **{name}**\n\n")

    print(f"✓ Wrote {txt_path}")
    print(f"✓ Wrote {md_path}")

if __name__ == "__main__":
    write_files()
