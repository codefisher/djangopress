"""
from djangopress.core import dynamic
from djangopress.blog import urls
from djangopress.blog.models import Blog

def test_slug(slug):
    return Blog.objects.get(slug=slug)

dynamic.register("blog", test_slug, urls)
"""