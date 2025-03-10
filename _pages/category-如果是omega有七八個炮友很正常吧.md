---
description: 顯示分類「如果是Omega有七八個炮友很正常吧」下的所有文章。
layout: category
permalink: /category/如果是omega有七八個炮友很正常吧/
title: 如果是Omega有七八個炮友很正常吧
---

<h1>分類：如果是Omega有七八個炮友很正常吧</h1>

{% for post in site.categories[page.title] %}
  <p><a href="{{ post.url | relative_url }}">{{ post.title }}</a> ({{ post.date | date: "%Y-%m-%d" }})</p>
{% endfor %}
