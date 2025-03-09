import os
import re
import frontmatter

# 設定 Jekyll 文章所在資料夾
POSTS_DIR = "_posts/"

# 批量處理所有 `.md` 檔案
for filename in os.listdir(POSTS_DIR):
    if filename.endswith(".md"):  # 只處理 Markdown 檔案
        filepath = os.path.join(POSTS_DIR, filename)

        # 讀取 Markdown 內容
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # 解析 YAML Front Matter
        post = frontmatter.loads(content)
        body = post.content  # 取得文章內容

        # 移除過多換行：將超過2行的換行符統一變成1行
        cleaned_body = re.sub(r'\n{3,}', '\n\n', body.strip())

        # 重新組合為 Markdown 格式
        new_content = f"{frontmatter.dumps(post)}\n\n{cleaned_body}"
        # 儲存清理後的內容
        with open(filepath, "w", encoding="utf-8") as new_file:
            new_file.write(new_content)

        print(f"✅ 已清理 {filename}，移除過多換行")

print("🎉 所有 Markdown 文章處理完成！")