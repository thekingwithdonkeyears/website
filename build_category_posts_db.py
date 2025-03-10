import os
import re
import yaml
import datetime

# 資料夾設定
POSTS_DIR = "_posts"
OUTPUT_FILE = "_data/category_posts.yml"

def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "-", value)
    return value

def read_front_matter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                data = yaml.safe_load(parts[1])
                return data, parts[2]
            except yaml.YAMLError as e:
                print(f"YAML 解析錯誤：{file_path} - {e}")
    return {}, content

# 建立以分類為 key 的資料庫
category_db = {}

for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        file_path = os.path.join(POSTS_DIR, filename)
        front, _ = read_front_matter(file_path)
        title = front.get("title", "未命名")
        date_str = front.get("date")
        if date_str:
            try:
                # 僅解析前10個字元，即 "YYYY-MM-DD" 格式
                d = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d")
            except Exception as e:
                print(f"日期解析錯誤：{file_path} - {e}")
                continue  # 日期解析錯誤時，跳過該文章
        else:
            print(f"文章 {file_path} 缺少日期，跳過。")
            continue  # 若缺少日期則跳過

        categories = front.get("categories")
        if categories:
            if isinstance(categories, list):
                cats = [str(c).strip() for c in categories if c]
            else:
                cats = [str(categories).strip()]
        else:
            cats = []

        # 取得文章的相對網址；如果 Front Matter 沒有提供，就使用檔名（你可根據實際情況調整）
        url = front.get("permalink", f"/{filename}")

        post_info = {
            "title": title,
            "date": d.strftime("%Y-%m-%d"),
            "url": url,
            "filename": filename
        }
        
        # 將文章依每個分類納入資料庫
        for cat in cats:
            if cat not in category_db:
                category_db[cat] = []
            category_db[cat].append(post_info)

# 對每個分類內的文章依日期排序（從舊到新）
for cat, posts in category_db.items():
    posts.sort(key=lambda p: p["date"])

# 將分類資料寫入 OUTPUT_FILE
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(category_db, f, allow_unicode=True, default_flow_style=False)

print(f"建立分類文章資料庫成功：{OUTPUT_FILE}")