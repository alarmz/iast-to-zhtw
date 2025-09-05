import argparse
import re

# IAST to Zhuyin mapping (expanded for more complete coverage)
IAST_TO_ZHUYIN = {
    # Vowels
    'āi': 'ㄞˉ', 'ai': 'ㄞ',
    'au': 'ㄠ', 'āu': 'ㄠˉ',
    'a': 'ㄚ', 'ā': 'ㄚˉ',
    'i': 'ㄧ', 'ī': 'ㄧˉ',
    'u': 'ㄨ', 'ū': 'ㄨˉ',
    'ṛ': 'ㄦˋ', 'ṝ': 'ㄦˉ',
    'ḷ': 'ㄌˋ', 'ḹ': 'ㄌˉ',
    'e': 'ㄝ', 'o': 'ㄛ',

    # Anusvāra and visarga
    'ṃ': 'ㆬ', 'ḥ': '˙',

    # Consonants with inherent vowel 'a'
    'kha': 'ㄎㄚ', 'ka': 'ㄎㄚ',
    'gha': 'ㄍㄚ', 'ga': 'ㄍㄚ',
    'ṅa': 'ㄫㄚ',

    'cha': 'ㄘㄚ', 'ca': 'ㄘㄚ',
    'jha': 'ㄐㄚ', 'ja': 'ㄐㄚ',
    'ña': 'ㄋㄧㄚ',

    'ṭha': 'ㄊㄚ', 'ṭa': 'ㄉㄚ',
    'ḍha': 'ㄉㄚ', 'ḍa': 'ㄉㄚ',
    'ṇa': 'ㄋㄚ',

    'tha': 'ㄊㄚ', 'ta': 'ㄊㄚ',
    'dha': 'ㄉㄚ', 'da': 'ㄉㄚ',
    'na': 'ㄋㄚ',

    'pha': 'ㄈㄚ', 'pa': 'ㄆㄚ',
    'bha': 'ㄅㄚ', 'ba': 'ㄅㄚ',
    'ma': 'ㄇㄚ',

    'ya': '一ㄚ', 'ra': 'ㄖㄚ', 'la': 'ㄌㄚ', 'va': 'ㄨㄚ',

    'śa': 'ㄒㄚ', 'ṣa': 'ㄕㄚ', 'sa': 'ㄙㄚ',
    'ha': 'ㄏㄚ',

    # Standalone consonants
    'k': 'ㄎ', 'kh': 'ㄎ',
    'g': 'ㄍ', 'gh': 'ㄍ',
    'ṅ': 'ㄫ',
    'c': 'ㄘ', 'ch': 'ㄘ',
    'j': 'ㄐ', 'jh': 'ㄐ',
    'ñ': 'ㄋ',
    'ṭ': 'ㄉ', 'ṭh': 'ㄉ',
    'ḍ': 'ㄉ', 'ḍh': 'ㄉ',
    'ṇ': 'ㄋ',
    't': 'ㄊ', 'th': 'ㄊ',
    'd': 'ㄉ', 'dh': 'ㄉ',
    'n': 'ㄋ',
    'p': 'ㄆ', 'ph': 'ㄈ',
    'b': 'ㄅ', 'bh': 'ㄅ',
    'm': 'ㄇ',
    'y': '一', 'r': 'ㄖ', 'l': 'ㄌ', 'v': 'ㄨ',
    'ś': 'ㄒ', 'ṣ': 'ㄕ', 's': 'ㄙ',
    'h': 'ㄏ',
}

# Order matters: longer keys first to match correctly
iast_keys = sorted(IAST_TO_ZHUYIN, key=lambda x: -len(x))
iast_pattern = re.compile('|'.join(re.escape(k) for k in iast_keys))

def iast_to_zhuyin_sentence_pairs_1(text: str) -> list:
    results = []
    lines = text.splitlines()
    for line in lines:
        if not line.strip():
            continue
        zhuyin_line = ''
        index = 0
        while index < len(line):
            match = iast_pattern.match(line, index)
            if match:
                iast = match.group(0)
                zhuyin = IAST_TO_ZHUYIN[iast]
                zhuyin_line += zhuyin
                index += len(iast)
            else:
                zhuyin_line += line[index]
                index += 1
        results.append((line, zhuyin_line))
    return results

def iast_to_zhuyin_sentence_pairs(text: str) -> list:
    # 分隔符：遇到這些字元就先把目前的注音 token 用「△」串起來輸出，再原樣輸出分隔符
    SEP_PATTERN = re.compile(r"[\s/,\.\-;:()【】\[\]{}!?]+")
    results = []

    for line in text.splitlines():
        if not line.strip():
            continue

        zhuyin_out = []
        tokens = []          # 暫存連續的注音片段，之後用「△」連接
        idx = 0
        L = len(line)

        def flush_tokens():
            nonlocal tokens
            if tokens:
                zhuyin_out.append("△".join(tokens))
                tokens = []

        while idx < L:
            # 1) 先找分隔字元（空白/斜線/標點…）
            m_sep = SEP_PATTERN.match(line, idx)
            if m_sep:
                # 把目前累積的注音 token 先輸出（用△相連），再輸出原始分隔符
                flush_tokens()
                zhuyin_out.append(m_sep.group(0))
                idx = m_sep.end()
                continue

            # 2) 嘗試匹配 IAST 片段
            m = iast_pattern.match(line, idx)
            if m:
                iast = m.group(0)
                tokens.append(IAST_TO_ZHUYIN[iast])
                idx += len(iast)
            else:
                # 3) 非映射字元（例如數字、其他符號等）
                flush_tokens()
                zhuyin_out.append(line[idx])
                idx += 1

        # 行尾若尚有 token，補輸出
        flush_tokens()
        results.append((line, "".join(zhuyin_out)))

    return results


def main():
    parser = argparse.ArgumentParser(description='Convert IAST text to Zhuyin Markdown table.')
    parser.add_argument('input', help='Input file with IAST text')
    parser.add_argument('output', help='Output Markdown file')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        input_text = f.read()

    pairs = iast_to_zhuyin_sentence_pairs(input_text)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('| IAST 原文 | 注音符號轉換 |\n')
        f.write('|------------|----------------|\n')
        for iast_line, zhuyin_line in pairs:
            f.write(f'| {iast_line} | {zhuyin_line} |\n')

    print(f"Converted IAST text to sentence-wise Zhuyin table and saved to {args.output}")

if __name__ == '__main__':
    main()
