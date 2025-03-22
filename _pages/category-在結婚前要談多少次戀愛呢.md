---
description: 顯示分類「在結婚前要談多少次戀愛呢？」下的所有文章。
layout: category
permalink: /category/在結婚前要談多少次戀愛呢/
title: 在結婚前要談多少次戀愛呢？
---

<h1>分類：在結婚前要談多少次戀愛呢？</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
