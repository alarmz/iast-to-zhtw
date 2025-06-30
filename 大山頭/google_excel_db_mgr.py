import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ======= 認證與初始化 =======
def get_sheet(sheet_url: str, worksheet_name: str = '工作表1'):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).worksheet(worksheet_name)
    return sheet


# ======= 查詢 =======
def find_row(sheet, character: str):
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):  # 表頭在第1列，資料從第2列開始
        if row['漢字'] == character:
            return i, row
    return None, None


# ======= 新增 =======
def add_row(sheet, character, zhuyin, pinyin, iast):
    sheet.append_row([character, zhuyin, pinyin, iast])
    print(f"✅ 已新增：{character}")


# ======= 修改 =======
def update_row(sheet, character, new_data: dict):
    row_index, old_row = find_row(sheet, character)
    if not row_index:
        print(f"⚠️ 找不到「{character}」，無法更新")
        return
    for col_name, value in new_data.items():
        col_index = sheet.row_values(1).index(col_name) + 1  # 找欄位名稱位置
        sheet.update_cell(row_index, col_index, value)
    print(f"✏️ 已更新：{character}")


# ======= 刪除 =======
def delete_row(sheet, character):
    row_index, _ = find_row(sheet, character)
    if row_index:
        sheet.delete_rows(row_index)
        print(f"🗑️ 已刪除：{character}")
    else:
        print(f"⚠️ 找不到「{character}」，無法刪除")


# ======= 主程序測試 =======
if __name__ == "__main__":
    SHEET_URL = 'https://docs.google.com/spreadsheets/d/你的表單ID/edit'
    sheet = get_sheet(SHEET_URL)

    # 新增
    add_row(sheet, '賀', 'ㄏㄜˋ', 'hè', 'ha')

    # 查詢
    idx, row = find_row(sheet, '賀')
    if row:
        print(f"🔍 查詢：{row}")

    # 修改
    update_row(sheet, '賀', {'注音': 'ㄏㄜˊ', 'IAST': 'hā'})

    # 刪除
    delete_row(sheet, '賀')
