import json

# 注音 → 拼音 簡易對照
zhuyin_to_pinyin_map = {
    'ㄅ': 'b', 'ㄆ': 'p', 'ㄇ': 'm', 'ㄈ': 'f',
    'ㄉ': 'd', 'ㄊ': 't', 'ㄋ': 'n', 'ㄌ': 'l',
    'ㄍ': 'g', 'ㄎ': 'k', 'ㄏ': 'h',
    'ㄐ': 'j', 'ㄑ': 'q', 'ㄒ': 'x',
    'ㄓ': 'zh', 'ㄔ': 'ch', 'ㄕ': 'sh', 'ㄖ': 'r',
    'ㄗ': 'z', 'ㄘ': 'c', 'ㄙ': 's',
    'ㄚ': 'a', 'ㄛ': 'o', 'ㄜ': 'e', 'ㄝ': 'ê',
    'ㄞ': 'ai', 'ㄟ': 'ei', 'ㄠ': 'ao', 'ㄡ': 'ou',
    'ㄢ': 'an', 'ㄣ': 'en', 'ㄤ': 'ang', 'ㄥ': 'eng',
    'ㄦ': 'er', 'ㄧ': 'i', 'ㄨ': 'u', 'ㄩ': 'ü',
    '˙': '', 'ˊ': '2', 'ˇ': '3', 'ˋ': '4', 'ˉ': '1'
}

# 常見咒語用漢字 → IAST 對應
iast_dict = {
    '嗡': 'oṃ', '唵': 'oṃ', '訶': 'ha', '離': 'lī', '婆': 'va',
    '帝': 'te', '求': 'khu', '陀': 'ta', '羅': 'la', '尼': 'ni',
    '囉': 'ra', '毘': 'vi', '黎': 'li', '你': 'ni', '摩': 'ma',
    '伽': 'ga', '真': 'jña', '陵': 'liṅ', '乾': 'kāṇ', '娑': 'sva',
    '南': 'nām', '謨': 'mo', '喝': 'hā', '怛': 'da', '那': 'na',
    '哆': 'da', '波': 'bha', '耶': 'ya', '佉': 'kha', '俱': 'jū',
    '住': 'stha', '虎': 'vi', '吽': 'hūṃ', '賀': 'ha', '潑': 'pha',
    '室': 'śri', '哩': 'li', '吒': 'ṭha', '唎': 'li', '修': 'śu',
    '嚩': 'va', '日': 'ṛ', '斛': 'hu', '無': 'mū', '滿': 'man',
    '度': 'du', '尾': 'vai', '薩': 'sarva', '莎': 'śa', '捺': 'nā',
    '巴': 'ba', '葛': 'ga', '瓦': 'vā', '阿': 'a', '密': 'mi',
    '納': 'na', '實': 'sat', '哿': 'gha', '多': 'da', '悉': 'siddhi',
    '遮': 'ja', '菩': 'pu', '提': 'ti', '迦': 'ka'
    # 可擴充
}

def convert_zhuyin_to_pinyin(zhuyin):
    result = ''
    tone = ''
    for ch in zhuyin:
        val = zhuyin_to_pinyin_map.get(ch, ch)
        if val in {'1', '2', '3', '4'}:
            tone = val
        else:
            result += val
    return result + tone

def parse_input_text(text):
    entries = []
    for idx, line in enumerate(text.strip().splitlines(), start=1):
        if '\t' in line:
            hanzi, zhuyin = line.strip().split('\t')
            pinyin = convert_zhuyin_to_pinyin(zhuyin)
            iast = iast_dict.get(hanzi, "")
            entries.append({
                "id": idx,
                "漢字": hanzi,
                "注音": zhuyin,
                "漢語拼音": pinyin,
                "IAST": iast
            })
    return entries

def main():
    input_file = 'zhuyin_list.txt'  # 替換為你的原始檔案
    output_file = 'zhuyin_to_pinyin_iast.json'

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    results = parse_input_text(raw_text)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ 已匯出 JSON：{output_file}")

if __name__ == '__main__':
    main()
