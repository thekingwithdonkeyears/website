---
description: 顯示分類「同人」下的所有文章。
layout: category
permalink: /category/同人/
title: 同人
---

<h1>分類：同人</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
