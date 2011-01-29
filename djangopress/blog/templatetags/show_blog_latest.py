from django import template
from djangopress.blog.models import Entry, Blog

register = template.Library()

@register.inclusion_tag('blog/show_latest.html')
def show_blog_latest(number=5, words=20, blog=None):
    blog = Blog.objects.get(slug=blog)
    try:
        number = int(number)
    except ValueError:
        number = 5
    entries_list = Entry.get_entries(blog=blog)[0:number]
    return {
        "entries": entries_list,
        "words": words
    }