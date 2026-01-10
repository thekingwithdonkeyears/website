---
description: 顯示分類「【定南】大學篇」下的所有文章。
layout: category
permalink: /category/定南大學篇/
title: 【定南】大學篇
---

<h1>分類：【定南】大學篇</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
