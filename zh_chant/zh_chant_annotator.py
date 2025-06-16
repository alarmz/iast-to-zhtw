#!/usr/bin/env python3
import re
import argparse
from pypinyin import pinyin, Style

def extract_annotation(char_with_ann):
    """抽取中文字與所有提示括號"""
    char_match = re.match(r'^(.)(\(.+?\))*$', char_with_ann)
    if not char_match:
        return char_with_ann, []

    char = char_match.group(1)
    annotations = re.findall(r'\(([^()]+)\)', char_with_ann)
    return char, annotations

def annotate_zh_text_with_bopomofo(raw_text):
    result_lines = []
    for line in raw_text.strip().splitlines():
        parts = re.findall(r'[^\s()（）]+(?:\([^)]+\))*', line)
        annotated_line = []
        for part in parts:
            char, hints = extract_annotation(part)
            zh_bopomofo = pinyin(char, style=Style.BOPOMOFO, errors='ignore')
            bopomofo = zh_bopomofo[0][0] if zh_bopomofo else '？'
            if hints:
                hint_str = ','.join(hints)
                annotated = f'{char}({bopomofo}｜{hint_str})'
            else:
                annotated = f'{char}({bopomofo})'
            annotated_line.append(annotated)
        result_lines.append(' '.join(annotated_line))
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
