---
description: 顯示分類「喜歡曖昧假說」下的所有文章。
layout: category
permalink: /category/喜歡曖昧假說/
title: 喜歡曖昧假說
---

<h1>分類：喜歡曖昧假說</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
