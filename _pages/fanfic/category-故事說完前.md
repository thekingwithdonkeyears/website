---
description: 顯示分類「故事說完前」下的所有文章。
layout: category
permalink: /category/故事說完前/
title: 故事說完前
---

<h1>分類：故事說完前</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
