---
description: 顯示分類「【米彩】初戀篇」下的所有文章。
layout: category
permalink: /category/米彩初戀篇/
title: 【米彩】初戀篇
---

<h1>分類：【米彩】初戀篇</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
