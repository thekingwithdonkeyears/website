---
description: 顯示分類「Déjà vu」下的所有文章。
layout: category
permalink: /category/déjà-vu/
title: Déjà vu
---

<h1>分類：Déjà vu</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
