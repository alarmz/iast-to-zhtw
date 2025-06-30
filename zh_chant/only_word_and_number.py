import re

def clean_mantra(text: str) -> str:
    """
    依照需求清理咒語文字：
      1) 去掉「」  2) 全形空白→換行
      3) 刪除 […]  4) 刪除帶發音提示的 (…)
    """
    # 1. 去掉中文引號
    text = re.sub(r'[「」]', '', text)

    # 2. 以全形空白 (\u3000) 斷行
    text = text.replace('\u3000', '\n')

    # 3. 移除方括號內所有內容
    text = re.sub(r'\[[^\]]*\]', '', text)

    # 4. 移除含發音提示的括號
    phonetic_keywords = r'引|合|上|去|反|轉|聲|三合|無鉢|\*'
    text = re.sub(r'\([^)]*(?:' + phonetic_keywords + r')[^)]*\)', '', text)

    # 5. 些許收尾：多餘空白與連續換行
    text = re.sub(r' +', ' ', text)          # 連續空白 → 1 個
    text = re.sub(r'\s+\n', '\n', text)      # 行尾空白
    text = re.sub(r'\n{2,}', '\n', text)     # 連續空行 → 1 行
    return text.strip()


if __name__ == "__main__":
    with open("raw.txt", "r", encoding="utf-8") as f:   # 原始檔
        raw = f.read()

    cleaned = clean_mantra(raw)

    # 存檔或後續處理
    with open("cleaned.txt", "w", encoding="utf-8") as f:
        f.write(cleaned)

    print("✅ 文字清理完成，已輸出 cleaned.txt")
