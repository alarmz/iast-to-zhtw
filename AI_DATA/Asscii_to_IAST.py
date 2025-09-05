import re
from indic_transliteration.sanscript import transliterate, VELTHUIS, IAST

#csx_text = "Tadyath2, ar02-gl2ne 0} 0} marda0 chid sa3-bhavatu sv2h2."
#csx_text = "Nama 2rya-ma#ju0r1 bodhisattv2ya mah2sattv2ya. Tadyath2, om, 2-rak=a janaya sv2h2."
csx_text = """
O3, 0r1 k2ry25i mah2-teja loka-dh2t4, mah2-ya02 sarasvat1 vi=a 2-
rak=i, praj#2-0r1 buddhi vardhani dh4tin2 pu=6in2 sv2h2. O3, k2r2
k2ma-r9pin sarva sattva hitod-yukt2 sa3-gr2mott2ra5i, jay2 praj#2-
p2ramit2 devye, 2rya-t2r2 manoram2 dundubh1 0a{khin1 p9r52 vidy2-
r2j#1, priya3-v2d2 candr2nan2 mah2-gaur1, ajita p1ta-v2sas2, mah2-
m2ya mah2-0vet2 mah2-bala par2-kram2, mah2-rudra mah2-ca57a
du=6a-sattva ni-s9dani. Pra-02nt2 02nta r9pâcar, vi-jay2 jvalana-
prabh2 vidyu-m2lin dhvaji 0a{khi garji cakri dhanur-dhar2 jambhani
stambhani, k2l1 k2la-r2tr1 ni02-car1 r2k=as1 mohani, 02nti k2nt2r1
dravi7i, 0ubh2 br2hma5i vida m2tâcar, guhil2 guha-v2sini ma{galy2,
0a3kar1 saumy2 j2ta vid2 manojav2-k2p2lini, mah2-dev1 sa3dhy2
satya apar2jit2 s2ratha v2ha k4p2-vi=62 na=6a. M2rga pra-dar0ani
varad2 02sani-0astri. Str1-r9pa v4tta vi-kram2 0avari-yogin1, siddh2
ca572l1 amit2 dhruv2, dhanya pu5ya mah2-bhag2 su-bhag2 priya
dar0an2, k4tânt2 tr2sani bh1ma ugr2, ugra mah2-tapa jagadika hitod-
yukt2, sara5ya bhakti vatsala v2g10var1, 0iv2 s9k=ma nitya sarvatra
janu-j2 sarva-artha-s2dhani, bhadr2 gho=64 dh2t4 dhana3 dad2 a-
bhay2, gautam1 pu5ya-0r1mat loke0var2m acyuti.
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
