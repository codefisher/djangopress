from django import template
from djangopress.blog.models import Entry, Blog

register = template.Library()

@register.inclusion_tag('blog/list_latest.html')
def list_blog_latest(number=5, blog=None):
    blog = Blog.objects.get(slug=blog)
    try:
        number = int(number)
    except ValueError:
        number = 5
    entries_list = Entry.objects.filter(blog=blog).order_by('-sticky', '-posted')[0:number]
    return {
        "entries": entries_list,
    }