from djangopress.forum.models import ForumGroup, ForumCategory, Forum, Thread, Post, THREADS_PER_PAGE, POSTS_PER_PAGE
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from djangopress.core.util import get_client_ip
from django.contrib.auth.models import User

try:
    import akismet
except:
    pass

def get_forum(forums_slug):
    return get_object_or_404(ForumGroup, slug=forums_slug, sites__id__exact=settings.SITE_ID)


def index(request, forums_slug):
    forums = get_forum(forums_slug)
    categories = ForumCategory.objects.filter(forums=forums).order_by('position')
    total_posts = Post.objects.filter().count()
    total_topics = Thread.objects.filter().count()
    total_users = User.objects.filter(is_active=True).count()
    data  = {
             "forums": forums,
             "categories": categories,
             "title": forums.name,
             "total_posts": total_posts,
             "total_topics": total_topics,
             "total_users": total_users,
    }
    return render(request, 'forum/index.html' , data)

def view_forum(request, forums_slug, forum_id, page=1):
    forums = get_forum(forums_slug)
    forum = get_object_or_404(Forum.objects.select_related('category__forums'), pk=forum_id)
    
    paginator = Paginator(Thread.objects.filter(forum=forum).select_related(
                'poster', 'last_post__author', 'forum__category__forums'
            ).order_by('-sticky', '-last_post_date'), THREADS_PER_PAGE)
    
    try:
        threads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        return HttpResponseRedirect(forum.get_absolute_url(paginator.num_pages))

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
        
def check_askmet_spam(request, post, form):
    api = akismet.Akismet()
    api.setAPIKey(settings.AKISMET_API_KEY)
    if api.verify_key():
        data = {
                "user_ip": get_client_ip(request),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "referrer": request.META.get("HTTP_REFERER"),
        }
        if request.user.is_authenticated():
            data.update({
                "comment_author": request.user.username,
                "comment_author_email": request.user.email,
                "comment_author_url": request.user.profile.homepage,
            })
        else:
            data.update({
                "comment_author": form.cleaned_data["poster_name"],
                "comment_author_email": form.cleaned_data["poster_email"],
            })
        return api.comment_check(form.cleaned_data["message"], data)
    return False

def new_thead(request, forums_slug, forum_id):
    forums = get_forum(forums_slug)
    forum = get_object_or_404(Forum, pk=forum_id)
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
                thread.poster_name = post_form.cleaned_data["poster_name"]
                thread.poster_email = post_form.cleaned_data["poster_email"]
            thread.forum = forum
            thread.save()
            if request.user.is_authenticated():
                thread.subscriptions.add(request.user)
            
            post = post_form.save(commit=False)
            post.is_spam = check_askmet_spam(post, post_form)
            post.ip = get_client_ip(request)
            post.thread = thread
            post.format = forums.format
            post.save()
            return HttpResponseRedirect(reverse('forum-view-thread', kwargs={"forums_slug": forums.slug, "thread": thread.pk}))
    else:
        thread_form = ThreadForm()
        if request.user.is_authenticated():
            post_form = PostForm()
        else:
            post_form = PostAnonymousForm()
    data = {
        "forums": forums,
        "forum": forum,
        "thread_form": thread_form,
        "post_form": post_form,
    }
    return render(request, 'forum/new_thread.html' , data)

def view_thread(request, forums_slug, thread_id, page=1):
    forums = get_forum(forums_slug)
    thread = get_object_or_404(Thread, pk=thread_id)
    paginator = Paginator(Post.objects.filter(thread=thread, is_spam=False, is_public=True
                    ).select_related('author', 'thread').order_by('posted'), POSTS_PER_PAGE)
    
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        return HttpResponseRedirect(thread.get_absolute_url(paginator.num_pages))
    thread.num_views += 1
    thread.save()
    
    data = {
        "forums": forums,
        "thread": thread,
        "posts": posts,
    }
    return render(request, 'forum/thread.html' , data)

def view_post(request, forums_slug, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post_id))

def reply_thread(request, forums_slug, thread_id):
    forums = get_forum(forums_slug)
    pass
