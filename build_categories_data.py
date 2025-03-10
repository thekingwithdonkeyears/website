import yaml
import re

# 定義你找到的分類（注意：set 的順序可能會亂，所以你可以轉成 list 排序）
categories = {
    'TWICE', 
    '如果是Omega有七八個炮友很正常吧', 
    '隨便聊聊', 
    '我還想和妳...', 
    '行星。恆星', 
    '氣象觀察站', 
    '【米彩】初戀篇', 
    'Omega作家 X Alpha 編輯', 
    '在結婚前要談多少次戀愛呢？', 
    '如果明天還會到來的話', 
    '故事說完前', 
    '同人', 
    '【37line】高中篇', 
    '【?】完結篇', 
    'Déjà vu', 
    '【定南】大學篇', 
    '喜歡曖昧假說'
}

# 自訂 slugify 函數，轉換成網址友好的格式
def slugify(value):
    value = value.lower()
    # 移除非單字、數字、空白與連字號的字元
    value = re.sub(r"[^\w\s-]", "", value)
    # 將空白與連字號合併為一個連字號
    value = re.sub(r"[-\s]+", "-", value)
    return value

# 將分類資料整理成列表（依照字母排序可以更好管理）
data = []
for cat in sorted(categories):
    slug = slugify(cat)
    permalink = f"/category/{slug}/"
    entry = {
        "title": cat,
        "slug": slug,
        "permalink": permalink,
        "description": f"顯示分類「{cat}」下的所有文章。"
    }
    data.append(entry)

# 將資料寫入 _data/categories.yml
data_file = "_data/categories.yml"
with open(data_file, "w", encoding="utf-8") as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

print(f"建立資料檔案：{data_file}")