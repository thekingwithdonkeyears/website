import os
import re
import frontmatter
from bs4 import BeautifulSoup

# 設定 Jekyll 文章所在資料夾
POSTS_DIR = "_posts/"

# 批量處理所有 `.html` 檔案
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".html"):  # 確保是 HTML 文章
        filepath = os.path.join(POSTS_DIR, filename)

        # 讀取原始 HTML 檔案
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # 解析 YAML Front Matter
        match = re.match(r"^(---.*?---)", content, re.DOTALL)
        if match:
            front_matter = match.group(1)
            html_body = content[len(front_matter):]  # 移除 YAML 之後的 HTML 內容
        else:
            print(f"⚠️ {filename} 沒有 YAML Front Matter，略過處理。")
            continue

        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(html_body, "html.parser")

        # 移除不必要的標籤
        for tag in soup(["html", "body", "meta", "script", "style"]):
            tag.decompose()

        # 轉換 `<p>` 為純文字（加換行）
        content_text = "\n\n".join([p.get_text(strip=True) for p in soup.find_all("p")])

        # 組合成新的 Markdown 文章
        new_content = f"{front_matter}\n\n{content_text}\n"

        # 轉換 `.html` 為 `.md` 並儲存
        new_filename = filename.replace(".html", ".md")
        new_filepath = os.path.join(POSTS_DIR, new_filename)

        with open(new_filepath, "w", encoding="utf-8") as new_file:
            new_file.write(new_content)

        print(f"✅ 已轉換 {filename} ➜ {new_filename}")

print("🎉 所有文章轉換完成！")