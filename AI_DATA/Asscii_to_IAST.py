import re
from indic_transliteration.sanscript import transliterate, VELTHUIS, IAST

#csx_text = "Tadyath2, ar02-gl2ne 0} 0} marda0 chid sa3-bhavatu sv2h2."
#csx_text = "Nama 2rya-ma#ju0r1 bodhisattv2ya mah2sattv2ya. Tadyath2, om, 2-rak=a janaya sv2h2."
csx_text = """
Namo bhagavate siddha-aparyanta-vipula-acintya-pra5idh2na-va0a,
na tat ki3 sarva sattv2m apa-v2da0 ca pr25i-bh9tam uparodha-k2rin
pra-v4tti pratigha-citta3, bodhi-cary2-gati3-gata-avivartya-sa3panne,
a-parim25a-gu5a-s2gara-0ubha-sa3bh4ta-sa3bh2ra-parip9r5e, sarva-
jagad-du`kha-agni-skandha-nirv2payit4, anuttara-pradh2na mah2-
2dar0a-j#2na-prabh2va da0a-dig-vipula-ma{gala-prabh2-samanta-
avabh2sa-loka-dh2tau ak=obhy2ya tath2gat2ya arhate samyak-
sa3buddh2ya. Om, adhim2tra-k2ru5ik2 pra-5idh2na-vi0e=a-gu5a
dharma-mukha sarva-loka-anugraha, mah2-2dar0a-j#2na tejo-
anubh2va adhi=6hite, sarva paripakva-ku0ala-m9la-sattv23 pra5idhi-
anta-vel2 pari-h4daye abhirati-buddha-vi=aya3 sa3-graha; vajra-
sattva vajra-r2ja vajra-r2ga vajra-har=a catur-2rya bodhisattv23
mah2-2vedha-va0am a-parikheda sarva-yoga-2cara` pari-tr2ya5e
sa3s2ra apa-kar=a5e sv2h2.
"""

# 1️⃣ 先處理多碼組合（順序一定要在單碼之前）
MULTI = {
    "0}": "śṝ",
    "08": "śṛ",
    "j#": "jñ",
    "n~": "ñ",
    "t.h": "ṭh",
    "d.h": "ḍh",
    "sh": "ś",
    "~n": "ñ",
    "n.t": "ṇṭ",
    "aa": "ā",
    "ii": "ī",
    "uu": "ū",
    "{g": "ṅg",
    "=o": "kṣ",
    "=a": "ṣ",  
    "#j": "ñj",
    "j#": "jñ",
    "=ḍh": "ṣṭh",  
    "#k": "ṅk", "#kh": "ṅkh", "#g": "ṅg", "#gh": "ṅgh",
    "#c": "ñc", "#ch": "ñch", "#j": "ñj", "#jh": "ñjh",
    "#ṭ": "ṇṭ", "#ṭh": "ṇṭh", "#ḍ": "ṇḍ", "#ḍh": "ṇḍh",
    "#t": "nt", "#th": "nth", "#d": "nd", "#dh": "ndh",
    "#p": "mp", "#ph": "mph", "#b": "mb", "#bh": "mbh"    
}
"""
for pat, repl in MULTI.items():
    csx_text = csx_text.replace(pat, repl)
"""
# 2️⃣ 再做單碼對映（仍採你原來的 8 個字元表）
TABLE = str.maketrans({
    '"': "Ā",
    #"0": "ś",  # ś (可能出現在 śrī)
    #"1": "",   # 無明確用途，可忽略或自定義
    "2": "ā",  # 長 a
    "&": "Ḍ",
    "7": "ḍ",
    "`": "ḥ",
    ">": "Ī",
    "1": "ī",
    "*": "Ḷ",
    "8": "ḷ",
    "3": "ṃ",
    "~": "Ñ",
    "#": "ñ",
    "%": "Ṇ",
    "5": "ṇ",
    "{": "ṅ",
    "$": "Ṛ",
    "4": "ṛ",
    "}": "ṝ",
    "_": "Ś",
    "0": "ś",
    "+": "Ṣ",
    "=": "ṣ",
    "^": "Ṭ",
    "6": "ṭ",
    "<": "Ū",
    "9": "ū"
})

"""
    "3": "ṃ",  # anusvāra
    "4": "ṛ",  # ṛ 捲舌元音
    "5": "ṇ",  # 捲舌鼻音
    "6": "ḍ",  # 捲舌塞音
    "7": "ṇ",  # 可與 5 同處理
    "8": "ṛ",  # 有時與 4 功能重疊
    "9": "ū",  # 長 u
    "}": "ī"   # 長 i
"""

intermediate = csx_text.translate(TABLE)

# 3️⃣ Velthuis→IAST（這步現在主要把 t.h / sh 等 Velthuis 殘碼清理）
iast = transliterate(intermediate, VELTHUIS, IAST)

print(iast)
