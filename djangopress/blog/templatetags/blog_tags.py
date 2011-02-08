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

@register.inclusion_tag('blog/list_latest.html')
def list_blog_latest(number=5, blog=None):
    blog = Blog.objects.get(slug=blog)
    try:
        number = int(number)
    except ValueError:
        number = 5
    entries_list = Entry.get_entries(blog=blog)[0:number]
    return {
        "entries": entries_list,
    }

@register.inclusion_tag('blog/list_archive.html')
def list_blog_archive(blog):
    entries_list = Entry.get_entries(blog=blog)
    dates = entries_list.dates('posted', 'month', order='DESC')
    return {
        "dates": dates,
    }

@register.inclusion_tag('blog/list_categories.html')
def list_blog_categories(blog):
    return {
        "categories": blog.categories.all().order_by('name'),
    }