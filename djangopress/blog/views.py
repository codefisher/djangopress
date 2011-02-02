import datetime

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from djangopress.blog.models import Blog, Entry, Tag, Category
from django.utils.translation import ugettext as _
from django.conf import settings

def resolve_blog(function):
    def _resolve_blog(*args, **kargs):
        kargs["blog"] = get_object_or_404(Blog, slug=kargs.get("blog"), sites__id__exact=settings.SITE_ID)
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
    entries_list = Entry.get_entries(blog=blog)
    return display_list(request, entries_list, blog)

@resolve_blog
def archive(request, year, month=None, blog=None):
    extra = {"format": "YEAR_MONTH_FORMAT"}
    year = int(year)
    entries_list = Entry.get_entries(blog=blog).filter(posted__year=year)
    if month is None:
        month = 1
        extra["format"] = "Y"
    else:
        month = int(month)
        entries_list = entries_list.filter(posted__month=month)
    extra["date"] = datetime.date(year=year, month=month, day=1)
    return display_list(request, entries_list, blog, extra, "blog/date_archive.html")

@resolve_blog
def post(request, year, month, day, slug, blog=None):
    kargs = {
        'posted__year':year,
        'posted__month':month,
        'posted__day':day,
        'slug':slug
    }
    entry = get_object_or_404(Entry, **kargs)
    try:
        previous = Entry.get_previous_by_posted(entry)
    except Entry.DoesNotExist:
        previous = None
    try:
        next = Entry.get_next_by_posted(entry)
    except Entry.DoesNotExist:
        next = None
    data = {
        "title": settings.TITLE_FORMAT % (blog.name, entry.title),
        "entry": entry,
        "respond": False,
        "next": next,
        "previous": previous,
        "blog": blog,
    }
    return render_to_response("blog/post.html", data,
            context_instance=RequestContext(request))

@resolve_blog
def tag(request, slug, blog=None):
    post_tag = get_object_or_404(Tag, slug=slug, blog=blog)
    entries_list = Entry.get_entries(blog=blog).filter(tags__slug=slug)
    return display_list(request, entries_list, blog,
            {"blog_heading": _("Posts Tagged '%s'") % post_tag.name})


@resolve_blog
def category(request, slug, blog=None):
    post_category = get_object_or_404(Category, slug=slug, blog=blog)
    entries_list = Entry.get_entries(blog=blog).filter(categories__slug=slug)
    return display_list(request, entries_list, blog,
            {"blog_heading": _("Archive for the '%s' Category") % post_category.name})

@resolve_blog
def moved(request, post=None, blog=None):
    entry = get_object_or_404(Entry, pk=post, blog=blog)
    return redirect(entry.get_absolute_url())
