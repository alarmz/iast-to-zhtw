import pytesseract
from PIL import Image, ImageDraw
import re

# 如果你是 Windows，請指定 Tesseract 路徑：
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 讀入圖片
image = Image.open("Snap29.jpg")
draw = ImageDraw.Draw(image)

# OCR 辨識（使用繁體中文語言）
ocr_result = pytesseract.image_to_string(image, lang="chi_tra")
boxes = pytesseract.image_to_boxes(image, lang="chi_tra")

# 清理文字結果（去掉換行空格）
cleaned_text = re.sub(r"\s+", "", ocr_result)

# 你要找的字串（逐字、依順序）
target_text = "如是我聞。一時佛在舍衛國祇樹給孤獨園"

# 將每個 box 儲存為 list of dict
box_list = []
img_w, img_h = image.size

for line in boxes.splitlines():
    parts = line.split()
    if len(parts) != 6:
        continue
    char, x1, y1, x2, y2, _ = parts
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    # Tesseract 的 Y 座標是以底部為 0，要轉換
    box_list.append({
        "char": char,
        "x1": x1,
        "y1": img_h - y2,
        "x2": x2,
        "y2": img_h - y1
    })

# 根據目標字串逐字搜尋並畫框
found_boxes = []
current_idx = 0

for target_char in target_text:
    for i in range(current_idx, len(box_list)):
        box = box_list[i]
        if box["char"] == target_char:
            draw.rectangle([box["x1"], box["y1"], box["x2"], box["y2"]], outline="red", width=2)
            found_boxes.append(box)
            current_idx = i + 1
            break
    else:
        print(f"❌ 無法依序找到字元：「{target_char}」")
        break
else:
    print("✅ 所有字元依序找到並已框出")

# 儲存結果圖片
image.save("output_highlighted.png")
print("📸 已儲存標註圖片：output_highlighted.png")
