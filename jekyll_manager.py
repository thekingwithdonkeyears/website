import gradio as gr
import os
import datetime
import re
import yaml

# === 文章上傳相關設定 ===
POSTS_DIR = "_posts"

def process_post(file_obj, title, date, categories, tags):
    """
    1. 讀取上傳的 Markdown 內容
    2. 組合 Jekyll Front Matter 與文章內容
    3. 依據日期與標題產生檔案名稱，並存到 _posts 目錄
    """
    # 讀取上傳檔案的內容（解碼為 utf-8）
    try:
        file_content = file_obj.read().decode("utf-8")
    except AttributeError:
        file_content = file_obj.decode("utf-8")
    
    # 處理日期，格式必須為 YYYY-MM-DD，若失敗則使用今天日期
    try:
        d = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_str = d.strftime("%Y-%m-%d")
    except Exception:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 將 categories 與 tags 使用逗號分隔的字串轉成 list
    categories_list = [cat.strip() for cat in categories.split(",") if cat.strip()]
    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    # 組合 YAML Front Matter
    front_matter = {
         "layout": "post",
         "title": title,
         "date": date_str,
         "categories": categories_list,
         "tags": tags_list
    }
    front_yaml = "---\n" + yaml.dump(front_matter, allow_unicode=True, default_flow_style=False) + "---\n\n"
    final_content = front_yaml + file_content

    # 建立檔案名稱：YYYY-MM-DD-標題.md（簡單 slug 處理）
    slug = "".join([c for c in title if c.isalnum() or c==" "]).strip().replace(" ", "-").lower()
    filename = f"{date_str}-{slug}.md"

    os.makedirs(POSTS_DIR, exist_ok=True)
    file_path = os.path.join(POSTS_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
         f.write(final_content)

    return f"文章已儲存至: {file_path}"

# === 分類管理相關設定 ===
DATA_FILE = "_data/categories.yml"
PAGES_DIR = "_pages"

def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)  # 移除非字母、數字、空白及連字號
    value = re.sub(r"[-\s]+", "-", value)    # 將空白與連字號合併為單一連字號
    return value

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

def save_categories(categories):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        yaml.dump(categories, f, allow_unicode=True, default_flow_style=False)

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

def add_category(title: str, description: str = ""):
    title = title.strip()
    description = description.strip()
    slug = slugify(title)
    
    categories = load_categories()
    # 檢查是否已存在
    for cat in categories:
        if cat.get("slug") == slug:
            return f"分類 {title} 已存在！"
    
    new_category = {
        "title": title,
        "slug": slug,
        "permalink": f"/category/{slug}/",
        "description": description if description else f"顯示分類「{title}」下的所有文章。"
    }
    categories.append(new_category)
    save_categories(categories)
    create_category_page(new_category)
    
    return f"分類 {title} 新增成功！"

# === Gradio 介面建立 ===
with gr.Blocks() as demo:
    gr.Markdown("# Jekyll 網站管理工具")
    
    with gr.Tab("上傳文章"):
        gr.Markdown("### 上傳 Markdown 檔案並補齊文章 Front Matter")
        post_file = gr.File(label="選擇 Markdown 檔案")
        post_title = gr.Textbox(label="標題")
        post_date = gr.Textbox(label="日期 (YYYY-MM-DD)", value=datetime.datetime.now().strftime("%Y-%m-%d"))
        post_categories = gr.Textbox(label="分類 (以逗號分隔)")
        post_tags = gr.Textbox(label="標籤 (以逗號分隔)")
        post_submit = gr.Button("上傳文章")
        post_output = gr.Textbox(label="結果")
        post_submit.click(fn=process_post, inputs=[post_file, post_title, post_date, post_categories, post_tags], outputs=post_output)
    
    with gr.Tab("新增分類"):
        gr.Markdown("### 輸入分類資訊")
        cat_title = gr.Textbox(label="分類名稱")
        cat_description = gr.Textbox(label="分類描述", placeholder="可選，輸入分類的描述")
        cat_submit = gr.Button("新增分類")
        cat_output = gr.Textbox(label="結果")
        cat_submit.click(fn=add_category, inputs=[cat_title, cat_description], outputs=cat_output)

if __name__ == "__main__":
    demo.launch()