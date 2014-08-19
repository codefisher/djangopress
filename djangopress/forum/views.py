from djangopress.forum.models import Forums, ForumCategories, Forum, Thread
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def resolve_forum(function):
    def _resolve_forum(*args, **kargs):
        kargs["forums"] = get_object_or_404(Forums, slug=kargs.get("forums"), sites__id__exact=settings.SITE_ID)
        return function(*args, **kargs)
    return _resolve_forum

@resolve_forum
def index(request, forums=None):
    categories = ForumCategories.objects.filter(forums=forums).order_by('position')
    data  = {
             "forums": forums,
             "categories": categories,
             "title": forums.name,
    }
    return render(request, 'forum/index.html' , data)

@resolve_forum
def view_forum(request, forums, forum_id, page=1):
    forum = get_object_or_404(Forum, pk=forum_id)
    paginator = Paginator(Thread.objects.filter(forum=forum), 40)
    
    try:
        threads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        threads = paginator.page(paginator.num_pages)
        
    data = {
        "forums": forums,
        "forum": forum,
        "title": forum.name,
        "threads": threads,
    }
    return render(request, 'forum/forum.html' , data)

@resolve_forum
def view_thread(request, forums):
    pass

@resolve_forum
def new_thead(request, forums, forum_id):
    pass

@resolve_forum
def reply_thread(request, forums):
    pass
