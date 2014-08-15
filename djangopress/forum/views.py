# Create your views here.

from djangopress.forum.models import Forums, ForumCategories
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.conf import settings

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
    }
    return render_to_response('forum/index.html' , data,
            context_instance=RequestContext(request))
    
def view_thread(request):
    pass

def view_forum(request, forums, forum_id):
    data = {
    }
    return render_to_response('forum/forum.html' , data,
            context_instance=RequestContext(request))

def new_thead(request):
    pass

def reply_thread(request):
    pass
