---
description: 顯示分類「【YouNameIt】」下的所有文章。
layout: category
permalink: /category/YouNameIt/
title: YouNameIt
---

<h1>分類：YouNameIt</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
