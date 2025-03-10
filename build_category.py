import os
import re
import yaml

# 定義 _posts 與 _pages 目錄
POSTS_DIR = "_posts"
PAGES_DIR = "_pages"

# 自訂一個 slugify 函數
def slugify(value):
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)  # 移除非單字、空白、連字號的字元
    value = re.sub(r"[-\s]+", "-", value)    # 將空白或連字號轉為單一連字號
    return value

# 讀取檔案的 Front Matter（假設 Front Matter 夾在第一組 --- 之間）
def read_front_matter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                data = yaml.safe_load(parts[1])
                return data
            except yaml.YAMLError as e:
                print(f"YAML 解析錯誤：{file_path} - {e}")
    return {}

# 收集所有文章中的分類（categories）
categories_set = set()

# 遍歷 _posts 資料夾下所有 .md 檔案
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):
        file_path = os.path.join(POSTS_DIR, filename)
        front = read_front_matter(file_path)
        if front:
            cats = front.get("categories")
            if cats:
                # 如果是字串，直接加入；如果是 list，就加入其中所有項目
                if isinstance(cats, list):
                    for cat in cats:
                        if cat:
                            categories_set.add(str(cat).strip())
                else:
                    categories_set.add(str(cats).strip())

print("找到的分類：", categories_set)


# 對每個分類建立一個分類頁面
for category in categories_set:
    slug = slugify(category)
    page_filename = f"category-{slug}.md"
    page_path = os.path.join(PAGES_DIR, page_filename)
    
    # 若檔案已存在，可以選擇覆寫或跳過；這裡示範覆寫
    front_matter = {
        "layout": "category",
        "title": category,
        "permalink": f"/category/{slug}/",
        "description": f"顯示分類「{category}」下的所有文章。"
    }
    # 組合 YAML Front Matter 與預設內容
    content = "---\n"
    content += yaml.dump(front_matter, allow_unicode=True, default_flow_style=False)
    content += "---\n\n"
    content += f"<h1>分類：{category}</h1>\n\n"
    content += "{% for post in site.categories[page.title] %}\n"
    content += "  <p><a href=\"{{ post.url | relative_url }}\">{{ post.title }}</a> ({{ post.date | date: \"%Y-%m-%d\" }})</p>\n"
    content += "{% endfor %}\n"
    
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"建立分類頁面：{page_path}")