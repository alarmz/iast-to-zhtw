#!/usr/bin/env python3
import re
import argparse
from pypinyin import pinyin, Style

# 咒語常用注音表（覆蓋）
CUSTOM_BOPOMOFO = {
    '唵': 'ㄥˋ',
    '吽': 'ㄏㄨㄥ',
    '阿': 'ㄚ',
    '怛': 'ㄉㄚˊ',
    '囉': 'ㄌㄨㄛ',
    '薩': 'ㄙㄚˋ',
    '嚩': 'ㄨㄛˋ',
    '嗡': 'ㄨㄥ',
    '哞': 'ㄇㄡ',
    '娜': 'ㄋㄚˋ',
    '摩': 'ㄇㄛˊ',
    '訶': 'ㄏㄜ',
    '帝': 'ㄉㄧˋ',
    '賀': 'ㄏㄜˋ',
    '𤚥': 'ㄇㄢˇ',
}

# 長音轉換
LONG_VOWEL_BOPOMOFO = {
    'ㄚ': 'ㄚˉ',
    'ㄛ': 'ㄛˉ',
    'ㄜ': 'ㄜˉ',
    'ㄧ': 'ㄧˉ',
    'ㄨ': 'ㄨˉ',
    'ㄩ': 'ㄩˉ',
    'ㄝ': 'ㄝˉ',
}

# 要刪掉的音節提示（輸出前移除）
PRONUN_HINTS_TO_REMOVE = [
    "合", "引", "上", "去", "平", "入",
    "聲呼", "轉舌", "反", "切身", "准", "無鉢", "魚夭"
]

def is_chinese_numeral(text):
    return re.fullmatch(r'[一二三四五六七八九十百千零〇○]+', text) is not None

def extract_annotation(char_with_ann):
    """抽取中文字與所有提示括號"""
    char_match = re.match(r'^(.)(\(.+?\))*$', char_with_ann)
    if not char_match:
        return char_with_ann, []
    char = char_match.group(1)
    annotations = re.findall(r'\(([^()]+)\)', char_with_ann)
    return char, annotations

def clean_line(text: str) -> str:
    """步驟1：預處理，移除 [＊] 標記與全形引號"""
    text = re.sub(r'\[[^\]]*]', '', text)
    text = text.replace('「', '').replace('」', '')
    return text

def is_pronun_hint_to_remove(h: str) -> bool:
    return any(k in h for k in PRONUN_HINTS_TO_REMOVE)

def annotate_zh_text_with_bopomofo(raw_text):
    result_lines = []
    for line in raw_text.strip().splitlines():
        line = clean_line(line)
        footnote = ''

        # 處理尾段 (一)(二十)
        footnote_match = re.search(r'\(([^()]+)\)\s*$', line)
        if footnote_match:
            possible_number = footnote_match.group(1)
            if is_chinese_numeral(possible_number):
                footnote = f'〔{possible_number}〕'
                line = line[:footnote_match.start()].rstrip()

        parts = re.findall(r'[^\s()（）]+(?:\([^)]+\))*', line)
        annotated_line = []

        for part in parts:
            # 移除括號內提示符，僅保留文字
            char_text = re.sub(r'\([^()]*\)', '', part)
            chars = list(char_text)

            for char in chars:
                # 注音
                if char in CUSTOM_BOPOMOFO:
                    bopomofo = CUSTOM_BOPOMOFO[char]
                else:
                    zh_bopomofo = pinyin(char, style=Style.BOPOMOFO, errors='ignore')
                    bopomofo = zh_bopomofo[0][0] if zh_bopomofo else '？'

                if bopomofo in LONG_VOWEL_BOPOMOFO:
                    bopomofo = LONG_VOWEL_BOPOMOFO[bopomofo]

                annotated_line.append(f'{char}({bopomofo})')

        result_lines.append(' '.join(annotated_line) + (f' {footnote}' if footnote else ''))

    return '\n'.join(result_lines)


def main():
    parser = argparse.ArgumentParser(description='中文咒語加注音與發音提示工具')
    parser.add_argument('--in', dest='input_file', required=True, help='輸入咒語的 .txt 檔案')
    parser.add_argument('--out', dest='output_file', required=True, help='輸出加上注音的檔案')

    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as infile:
        raw_text = infile.read()

    annotated = annotate_zh_text_with_bopomofo(raw_text)

    with open(args.output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(annotated)

    print(f'✅ 注音結果已儲存到: {args.output_file}')

if __name__ == '__main__':
    main()
