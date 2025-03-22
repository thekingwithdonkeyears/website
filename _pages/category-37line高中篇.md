---
description: 顯示分類「【37line】高中篇」下的所有文章。
layout: category
permalink: /category/37line高中篇/
title: 【37line】高中篇
---

<h1>分類：【37line】高中篇</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
