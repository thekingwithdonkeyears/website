---
description: 顯示分類「TWICE」下的所有文章。
layout: category
permalink: /category/twice/
title: TWICE
---

<h1>分類：TWICE</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
