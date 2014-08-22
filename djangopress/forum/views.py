from djangopress.forum.models import ForumGroup, ForumCategory, Forum, Thread, Post
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def resolve_forum(function):
    def _resolve_forum(*args, **kargs):
        kargs["forums"] = get_object_or_404(ForumGroup, slug=kargs.get("forums"), sites__id__exact=settings.SITE_ID)
        return function(*args, **kargs)
    return _resolve_forum

@resolve_forum
def index(request, forums=None):
    categories = ForumCategory.objects.filter(forums=forums).order_by('position')
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

class ThreadForm(forms.ModelForm):
    class Meta(object):
        fields = ("subject",)
        model = Thread

class PostForm(forms.ModelForm):
    class Meta(object):
        fields = ("message","show_similies")
        model = Post
        
class PostAnonymousForm(forms.ModelForm):
    class Meta(object):
        fields = ("poster_name", "poster_email", "message","show_similies")
        model = Post
        
class PostEditForm(forms.ModelForm):
    class Meta(object):
        fields = ("message", "edit_reason", "show_similies")
        model = Post

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR')

@resolve_forum
def new_thead(request, forums, forum_id):
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        if request.user.is_authenticated():
            post_form = PostForm(request.POST)
        else:
            post_form = PostAnonymousForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(commit=False)
            if request.user.is_authenticated():
                thread.poster = request.user
            else:
                thread.poster_name = post_form.poster_name
                thread.poster_email = post_form.poster_email
            thread.forum = Forum.objects.get(pk=forum_id)
            thread.save()
            if request.user.is_authenticated():
                thread.subscriptions.add(request.user)
            
            post = post_form.save(commit=False)
            post.ip = get_client_ip(request)
            post.thread = thread
            post.format = forums.format
            post.save()
            
            thread.first_post = post
            thread.last_post = post
            thread.save()
            
            if forums.slug:
                return HttpResponseRedirect(reverse('forum-view-thread', args={"forums": forums.slug, "thread": thread.pk}))
            else:
                return HttpResponseRedirect(reverse('forum-view-thread', args={"thread": thread.pk}))
    else:
        thread_form = ThreadForm()
        if request.user.is_authenticated():
            post_form = PostForm()
        else:
            post_form = PostAnonymousForm()
    data = {
        "forums": forums,
        "thread_form": thread_form,
        "post_form": post_form,
    }
    return render(request, 'forum/new_thread.html' , data)

@resolve_forum
def view_thread(request, forums, thread):
    return render(request, 'forum/thread.html' , data)

@resolve_forum
def reply_thread(request, forums):
    pass
