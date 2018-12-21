---
layout: default
title: "Blog"
permalink: /blog/
---

<div id="blog" class="container text-center" style="min-height:100vh">
	<h2 class="heading-1 top-margin"><span><strong>When</strong> I Did Things</span></h2>
	<h2><strong><u>Blog</u></strong></h2>
	<div class="form-group"></div>
		{% for post in site.posts %}
			<div class="text-left reveal-left">
			<a href="{{ post.url }}"><h3>{{ post.title }}</h3></a>
			<p><span style='font-size: 16px'>{{ post.date | date: '%A, %B %d, %Y' }}</span></p>
			<div class="row">
				<div class="col-lg-9">
				<p>{{ post.preview }}</p>
				</div>
				<div class="col-lg-3"></div>
			</div>
			{% if forloop.last != true %}<div class="form-group"></div>{% endif %}
			</div>
		{% endfor %}
	<div class="form-group"></div>
	<a href="/" id="homeButton" class="btn btn-default text-uppercase reveal-bottom-scale">Back to Home Page</a>
</div>

{% include footer.html %}