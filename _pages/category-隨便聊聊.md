---
description: 顯示分類「隨便聊聊」下的所有文章。
layout: category
permalink: /category/隨便聊聊/
title: 隨便聊聊
---

<h1>分類：隨便聊聊</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
