import argparse
import json
import re

# 載入 IAST 對照表
with open("iast_to_bopomofo.json", "r", encoding="utf-8") as f:
    IAST_MAP = json.load(f)

# 音節優先長匹配順序（降序排列）
IAST_SYLLABLES = sorted(IAST_MAP.keys(), key=lambda x: -len(x))

def iast_to_bopomofo(text):
    result = []
    words = re.split(r'[\s,;。！!？?]', text)  # 支援簡單斷句
    for word in words:
        if not word.strip():
            continue
        i = 0
        line = ""
        while i < len(word):
            matched = False
            for syl in IAST_SYLLABLES:
                if word[i:i+len(syl)] == syl:
                    line += f"{IAST_MAP[syl]}\n"
                    i += len(syl)
                    matched = True
                    break
            if not matched:
                line += f"{word[i]}\n"  # 無對應，原樣保留
                i += 1
        result.append(line.strip())
    return "\n\n".join(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert IAST Sanskrit to Bopomofo")
    parser.add_argument("input", help="Input IAST text file")
    parser.add_argument("--out", default="result.txt", help="Output filename (default: result.txt)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as fin:
        content = fin.read()

    output = iast_to_bopomofo(content)

    with open(args.out, "w", encoding="utf-8") as fout:
        fout.write(output)

    print(f"✅ 已轉換並輸出至 {args.out}")
