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

def iast_to_zhuyin(text: str) -> str:
    def replace(match):
        return IAST_TO_ZHUYIN.get(match.group(0), match.group(0))
    return iast_pattern.sub(replace, text)

def main():
    parser = argparse.ArgumentParser(description='Convert IAST text to Zhuyin.')
    parser.add_argument('input', help='Input file with IAST text')
    parser.add_argument('output', help='Output file with Zhuyin')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        input_text = f.read()

    output_text = iast_to_zhuyin(input_text)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output_text)

    print(f"Converted IAST to Zhuyin and saved to {args.output}")

if __name__ == '__main__':
    main()
