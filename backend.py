from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import re
import yaml

app = FastAPI()

# 目錄設定
DATA_FILE = "_data/categories.yml"
PAGES_DIR = "_pages"

# 自訂 slugify 函數，將分類名稱轉換成網址友好的格式
def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)  # 移除非字母、數字、空白及連字號
    value = re.sub(r"[-\s]+", "-", value)    # 將空白與連字號合併為單一連字號
    return value

# 讀取現有的分類資料
def load_categories():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
                return data if data else []
            except yaml.YAMLError as e:
                print("YAML 解析錯誤:", e)
                return []
    return []

# 儲存分類資料到 YAML 檔案
def save_categories(categories):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        yaml.dump(categories, f, allow_unicode=True, default_flow_style=False)

# 自動建立分類頁面
def create_category_page(category_entry):
    slug = category_entry["slug"]
    filename = f"category-{slug}.md"
    filepath = os.path.join(PAGES_DIR, filename)
    
    front_matter = {
        "layout": "category",
        "title": category_entry["title"],
        "slug": slug,
        "permalink": f"/category/{slug}/",
        "description": category_entry.get("description", f"顯示分類「{category_entry['title']}」下的所有文章。")
    }
    
    content = "---\n" + yaml.dump(front_matter, allow_unicode=True, default_flow_style=False) + "---\n\n"
    content += f"<h1>分類：{category_entry['title']}</h1>\n\n"
    content += "{% for post in site.categories[page.title] %}\n"
    content += "  <p><a href=\"{{ post.url | relative_url }}\">{{ post.title }}</a> ({{ post.date | date: \"%Y-%m-%d\" }})</p>\n"
    content += "{% endfor %}\n"
    
    os.makedirs(PAGES_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"建立分類頁面：{filepath}")

# 請求模型
class CategoryRequest(BaseModel):
    title: str
    description: str = ""

@app.post("/add-category")
async def add_category(request: CategoryRequest):
    title = request.title.strip()
    description = request.description.strip() if request.description else ""
    slug = slugify(title)
    
    categories = load_categories()
    
    # 檢查是否已存在相同 slug 的分類
    for cat in categories:
        if cat.get("slug") == slug:
            return {"message": "此分類已存在", "category": cat}
    
    new_category = {
        "title": title,
        "slug": slug,
        "permalink": f"/category/{slug}/",
        "description": description if description else f"顯示分類「{title}」下的所有文章。"
    }
    
    categories.append(new_category)
    save_categories(categories)
    create_category_page(new_category)
    
    return {"message": "新增分類成功", "category": new_category}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
"""
curl -X POST http://127.0.0.1:8000/add-category \
-H "Content-Type: application/json" \
-d '{"title": "新分類名稱", "description": "這是新分類的描述"}'
"""