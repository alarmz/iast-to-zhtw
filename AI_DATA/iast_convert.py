import json
import re
import sys
from indic_transliteration.sanscript import transliterate, VELTHUIS, IAST

# 載入設定檔
with open("multi_mapping.json", encoding="utf-8") as f:
    MULTI = json.load(f)

with open("table_mapping.json", encoding="utf-8") as f:
    TABLE = str.maketrans(json.load(f))

with open("postfix_cleanup_rules.json", encoding="utf-8") as f:
    POSTFIX = json.load(f)

def convert_csx_to_iast(text: str) -> str:
    # 多碼轉換
    for pat, repl in MULTI.items():
        text = text.replace(pat, repl)

    # 單碼轉換
    text = text.translate(TABLE)

    # Velthuis → IAST
    text = transliterate(text, VELTHUIS, IAST)

    # 後處理 cleanup
    for bad, good in POSTFIX.items():
        text = text.replace(bad, good)

    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python iast_convert.py <詞句>")
        sys.exit(1)

    input_text = " ".join(sys.argv[1:])
    result = convert_csx_to_iast(input_text)
    print(result)
