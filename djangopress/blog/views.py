import datetime

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from djangopress.blog.models import Blog, Entry, Tag, Category
from django.utils.translation import ugettext as _
from django.conf import settings

#TODO: neither the visibility nor status tags are currently used

def resolve_blog(function):
    def _resolve_blog(*args, **kargs):
        kargs["blog"] = get_object_or_404(Blog, slug=kargs.get("blog"))
        return function(*args, **kargs)
    return _resolve_blog

def display_list(request, entries_list, blog, extra=None, template='blog/index.html'):
    paginator = Paginator(entries_list, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    data = {
        "blog": blog,
        "entries": entries,
        "title": blog.name,
        "respond": True,
    }
    if extra:
        data.update(extra)
    return render_to_response(template , data,
            context_instance=RequestContext(request))

@resolve_blog
def index(request, blog=None):
    entries_list = Entry.objects.filter(blog=blog).order_by('-sticky', '-posted')
    return display_list(request, entries_list, blog)

@resolve_blog
def archive(request, year, month=None, blog=None):
    extra = {"format": "YEAR_MONTH_FORMAT"}
    year = int(year)
    entries_list = Entry.objects.filter(blog=blog, posted__year=year)
    if month is None:
        month = 1
        extra["format"] = "Y"
    else:
        month = int(month)
        entries_list = entries_list.filter(posted__month=month)
    extra["date"] = datetime.date(year=year, month=month, day=1)
    entries_list = entries_list.order_by('-posted')
    return display_list(request, entries_list, blog, extra, "blog/date-archive.html")

@resolve_blog
def post(request, year, month, day, slug, blog=None):
    entry = get_object_or_404(Entry, posted__year=year, posted__month=month, posted__day=day, slug=slug)
    data = {
        "title": settings.TITLE_FORMAT % (blog.name, entry.title),
        "entry": entry,
        "respond": False,
    }
    return render_to_response("blog/post.html", data,
            context_instance=RequestContext(request))

@resolve_blog
def tag(request, slug, blog=None):
    post_tag = get_object_or_404(Tag, slug=slug)
    entries_list = Entry.objects.filter(blog=blog, tags__slug=slug).order_by('-posted')
    return display_list(request, entries_list, blog,
            {"blog_heading": _("Posts Tagged '%s'") % post_tag.name})


@resolve_blog
def category(request, slug, blog=None):
    post_category = get_object_or_404(Category, slug=slug)
    entries_list = Entry.objects.filter(blog=blog, categories__slug=slug).order_by('-posted')
    return display_list(request, entries_list, blog,
            {"blog_heading": _("Archive for the '%s' Category") % post_category.name})

@resolve_blog
def moved(request, post=None, blog=None):
    entry = get_object_or_404(Entry, pk=post, blog=blog)
    return redirect(entry.get_absolute_url())
