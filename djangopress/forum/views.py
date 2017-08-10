import datetime
from itertools import chain
import re

from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.http.response import Http404, HttpResponseRedirect
from django.contrib import messages
from djangopress.forum.models import ForumGroup, ForumCategory, Forum, Thread, Post, ForumUser
from djangopress.core.util import get_client_ip, has_permission, choose_form
from djangopress.forum.forms import PostAnonymousForm, PostEditForm, PostForm, ReportForm, ThreadForm, QuickPostForm
from djangopress.accounts.middleware import get_last_seen
from django.utils.encoding import force_str

TITLE_FORMAT = getattr(settings, 'FORUM_TITLE_FORMAT', "%s :: %s")

try:
    import akismet
except ImportError:
    akismet = None

def get_forum(forums_slug):
    return get_object_or_404(ForumGroup, slug=forums_slug, sites__id__exact=settings.SITE_ID)

def index(request, forums_slug, category_id=None):
    forums = get_forum(forums_slug)
    categories = ForumCategory.objects.filter(forums=forums).order_by('position').select_related('forums')
    if category_id:
        categories = [get_object_or_404(categories, pk=category_id)]
    total_posts = Post.objects.filter().count()
    total_topics = Thread.objects.filter().count()
    total_users = User.objects.filter(is_active=True).count()
    if total_users > 0:
        newest_user = User.objects.filter(is_active=True).order_by('-date_joined')[0]
    else:
        newest_user = None
    data  = {
             "forums": forums,
             "categories": categories,
             "title": forums.name,
             "total_posts": total_posts,
             "total_topics": total_topics,
             "total_users": total_users,
             "newest_user": newest_user,
    }
    return render(request, 'forum/index.html' , data)

def moderator_forum(request):
    #needs to be the same as view_forum, but can move, delete, open or close any topic in batch.
    pass

def view_forum(request, forums_slug, forum_id, page=1):
    forums = get_forum(forums_slug)
    forum = get_object_or_404(Forum.objects.select_related('category', 'category__forums'), pk=forum_id, category__forums=forums.pk)
    
    paginator = Paginator(Thread.objects.filter(forum=forum).select_related(
                'poster', 'last_post__author', 'forum__category__forums'
            ).exclude(first_post=None).defer('last_post__message').order_by('-sticky', '-last_post_date'), forums.number_of_threads)
    
    try:
        threads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            return redirect(forum.get_absolute_url(paginator.num_pages))
    data = {
        "forums": forums,
        "forum": forum,
        "title": forum.name,
        "threads": threads,
    }
    return render(request, 'forum/forum.html' , data)

        
def check_askmet_spam(request, form):
    if not akismet:
        return False
    try:
        api = akismet.Akismet(key=settings.AKISMET_API.get('key'),
                              blog_url=settings.AKISMET_API.get('blog_url'))
    except akismet.ConfigurationError as e:
        return False
    except akismet.APIKeyError as e:
        return False
    if request.user.is_authenticated():
        return api.comment_check(user_ip=get_client_ip(request),
                                 user_agent=request.META.get("HTTP_USER_AGENT"),
                                 referrer=request.META.get("HTTP_REFERER"),
                                 comment_content=form.cleaned_data["message"],
                                 comment_author=request.user.username,
                                 comment_author_email=request.user.email,
                                 comment_author_url=request.user.profile.homepage)
    else:
        return api.comment_check(user_ip=get_client_ip(request),
                                 user_agent=request.META.get("HTTP_USER_AGENT"),
                                 referrer=request.META.get("HTTP_REFERER"),
                                 comment_content=form.cleaned_data["message"],
                                 comment_author= form.cleaned_data["poster_name"],
                                 comment_author_email=form.cleaned_data["poster_email"])

def new_thread(request, forums_slug, forum_id):
    forums = get_forum(forums_slug)
    forum = get_object_or_404(Forum, pk=forum_id)
    if not has_permission(request, 'forum', 'can_post_threads'):
        data = {
                "forums": forums,
                "forum": forum,
                "title": "Permission denied to post thread",
                "anonymous": not request.user.is_authenticated(),
        }
        return render(request, 'forum/thread/new_denied.html' , data)
    preview = None
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = choose_form(request, PostForm, PostAnonymousForm, request.POST)
        if not request.POST.get('preview') and thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(commit=False)
            if request.user.is_authenticated():
                thread.poster = request.user
            else:
                thread.poster_name = post_form.cleaned_data["poster_name"]
                thread.poster_email = post_form.cleaned_data["poster_email"]
            thread.forum = forum
            thread.save()
            for user in forum.subscriptions.all():
                if user == request.user:
                    continue
                if not user.forum_subscriptions.filter(pk=thread.pk).exists():
                    thread.subscriptions.add(user)
            return process_post(request, thread, post_form, forums)
        elif request.POST.get('preview') and post_form.is_valid():
            preview = post_form.save(commit=False)
            preview.format = forums.format
    else:
        thread_form = ThreadForm()
        post_form = choose_form(request, PostForm, PostAnonymousForm)
    data = {
        "forums": forums,
        "forum": forum,
        "preview": preview,
        "title": TITLE_FORMAT % (forum.name, "New Thread"),
        "thread_form": thread_form,
        "post_form": post_form,
    }
    return render(request, 'forum/thread/new.html' , data)

def view_thread(request, forums_slug, thread_id, page=1):
    forums = get_forum(forums_slug)
    thread = get_object_or_404(Thread.objects.select_related('forum', 'forum__category__forums'), pk=thread_id)
    paginator = Paginator(Post.objects.filter(thread=thread, is_spam=False, is_public=True
                    ).select_related('author', 'thread', 'edited_by', 'thread__forum__category__forums', 'author__forum_profile', 'author__profile').order_by('posted'), forums.number_of_posts)
    
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            return redirect(thread.get_absolute_url(paginator.num_pages))
    Thread.objects.filter(pk=thread.pk).update(num_views=models.F('num_views') + 1)
    
    data = {
        "forums": forums,
        "form": QuickPostForm(),
        "thread": thread,
        "title": thread.subject,
        "posts": posts,
    }
    return render(request, 'forum/thread/index.html' , data)

def view_post(request, forums_slug, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return redirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post_id))

def last_post(request, forums_slug, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    try:
        post = Post.objects.filter(thread=thread, is_spam=False, is_public=True
                    ).select_related('thread').order_by('posted')[0]
    except IndexError:
        raise Http404
    return redirect("%s#p%s" % (thread.get_absolute_url(post.get_page()), post.pk))

def process_post(request, thread, post_form, forums):
    post = post_form.save(commit=False)
    if request.user.is_authenticated():
        forum_profile, created = ForumUser.objects.get_or_create(user=request.user)
        if forum_profile.notify == 'AL' and not request.user.forum_subscriptions.filter(pk=thread.pk).exists():
            thread.subscriptions.add(request.user)
        post.author = request.user
    try:
        spam = check_askmet_spam(request, post_form)
        post.is_spam = spam
        if spam and request.user.is_authenticated():
            profile = request.user.profile
            profile.banned = True
            profile.save()
    except NameError:
        post.is_spam = False
    post.ip = get_client_ip(request)
    post.user_agent = request.META.get("HTTP_USER_AGENT")[0:250]
    post.thread = thread
    post.format = forums.format
    post.save()
    site = Site.objects.get_current()
    if post.is_public and not post.is_spam:
        for user in thread.subscriptions.all():
            if user == request.user:
                continue
            # TODO: should check here if the last post was after the user last visited
            # in which cause we don't need to email them
            message_data = {
                "site": site,
                "user": user,
                "thread": thread,
                "forums": forums,
                "post": post,
                "scheme": "https" if request.is_secure() else "http",
            }
            message = render_to_string('forum/email/subscription_notification.txt', message_data)
            user.email_user("Topic Subscription Notification for %s" % forums.name, message)
    data = {
            "post": post,
            "title": "Post Submitted",
            "thread": thread,
            "forums": forums,
    }
    if forums.post_redirect_delay:
        responce = render(request, 'forum/post/posted.html' , data)
        if not post.is_spam and post.is_public:
            responce["Refresh"] = "%s;%s" % (forums.post_redirect_delay, post.get_absolute_url())
    else:
        if not post.is_spam and post.is_public:
            messages.add_message(request, messages.SUCCESS, "Your post has been made.")
        else:
            messages.add_message(request, messages.WARNING, "Your post was made, but will not be public till it has been view by an administrator.")
        responce = HttpResponseRedirect(post.get_absolute_url())
    return responce

def reply_thread(request, forums_slug, thread_id):
    forums = get_forum(forums_slug)
    thread = get_object_or_404(Thread, pk=thread_id)
    if thread.closed:
        data = {
                "forums": forums,
                "title": "Thread Closed",
                "thread": thread,
        }
        return render(request, 'forum/thread/closed.html' , data)
    if not has_permission(request, 'forum', 'can_post_replies'):
        data = {
                "forums": forums,
                "title": "Permission Denied",
                "thread": thread,
                "anonymous": not request.user.is_authenticated(),
        }
        return render(request, 'forum/thread/denied.html' , data)
    preview = None
    if request.method == 'POST':
        post_form = choose_form(request, PostForm, PostAnonymousForm, request.POST)
        if post_form.is_valid():
            if request.POST.get('preview'):
                preview = post_form.save(commit=False)
                preview.format = forums.format
            else:
                return process_post(request, thread, post_form, forums)
    else:
        quotes = []
        for post_id in request.GET.getlist('quote'):
            if not post_id or not post_id.isdigit():
                continue
            try:
                post = Post.objects.get(pk=post_id)
                quotes.append("[quote post=%s]%s[/quote]" % (post.pk, post.message))
            except Post.DoesNotExist:
                pass
        post_form = choose_form(request, PostForm, PostAnonymousForm, initial={'message': "\n".join(quotes)})
    posts = Post.objects.filter(thread=thread, is_spam=False, is_public=True
                    ).select_related('author', 'thread').order_by('-posted')[:5]
    data = {
        "forums": forums,
        "posts": posts,
        "preview": preview,
        "thread": thread,
        "title": TITLE_FORMAT % (thread.subject, "Post Reply"),
        "post_form": post_form,
    }
    return render(request, 'forum/thread/reply.html' , data)

def report_post(request, forums_slug, post_id):
    forums = get_forum(forums_slug)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.post = post
            if request.user.is_authenticated():
                report.reported_by = request.user
            report.save()
        return redirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
    else:
        report_form = ReportForm()
    data = {
            "post": post,
            "title": "Report Post",
            "forums": forums,
            "report_form": report_form
    }
    return render(request, 'forum/post/report.html' , data)

def edit_post(request, forums_slug, post_id):
    forums = get_forum(forums_slug)
    post = get_object_or_404(Post, pk=post_id)
    if not (has_permission(request, 'forum', 'can_edit_others_posts') 
            or (post.author == request.user and has_permission(request, 'forum', 'can_edit_own_posts'))):
        data = {
                "forums": forums,
                "title": "Permission Denied",
                "post": post,
        }
        return render(request, 'forum/post/edit_denied.html' , data)
    thread_form = None
    if request.method == 'POST':
        edit_form = PostEditForm(request.POST, instance=post)
        valid = True
        if post == post.thread.first_post:
            thread_form = ThreadForm(request.POST, instance=post.thread)
            if thread_form.is_valid():
                thread_form.save()
            else:
                valid = False
        if edit_form.is_valid() and valid:
            post = edit_form.save(commit=False)
            post.edited = datetime.datetime.now()
            post.edited_by = request.user
            post.save()
            return redirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
    else:
        edit_form = PostEditForm(instance=post)
        if post == post.thread.first_post:
            thread_form = ThreadForm(instance=post.thread)
    data = {
            "forums": forums,
            "post": post,
            "title": "Edit: %s" % post.thread.subject,
            "edit_form": edit_form,
            "thread_form": thread_form,
    }
    return render(request, 'forum/post/edit.html' , data)
    
def post_action(request, forums_slug, post_id, redirect_before, do_action, name, message, permission):
    forums = get_forum(forums_slug)
    post = get_object_or_404(Post, pk=post_id)
    if not has_permission(request, 'forum', permission):
        return redirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
    if request.method == 'POST' and request.POST.get('post'):
        if redirect_before:
            redirect_responce = redirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
        do_action(post)
        post.save()
        if not redirect_before:
            redirect_responce = redirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
        return redirect_responce
    data = {
            "post": post,
            "title": name,
            "forums": forums,
            "message": message,
            "name": name,
    }
    return render(request, 'forum/post/action.html' , data)
    
def delete_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_public = False
    return post_action(request, forums_slug, post_id, True, do_action, "Delete Post", "delete the post", "can_mark_public")

def restore_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_public = True
    return post_action(request, forums_slug, post_id, False, do_action, "Restore Post", "restore the post", "can_mark_public")
    
def spam_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_spam = True
        # we we could call upon akismet
    return post_action(request, forums_slug, post_id, True, do_action, "Mark as Spam", "mark the post as spam", "can_mark_spam")
    
def not_spam_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_spam = False
    return post_action(request, forums_slug, post_id, False, do_action, "Mark as Not Spam", "mark the post as not span", "can_mark_spam")
    
def remove_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_removed = True
    return post_action(request, forums_slug, post_id, True, do_action, "Remove", "mark the post as removed", "can_mark_removed")
    
    
def recover_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_removed = False
    return post_action(request, forums_slug, post_id, True, do_action, "Restore", "mark the post as not removed", "can_mark_removed")
    
def subscribe(request, forums_slug, thread_id, subscribe=True):
    forums = get_forum(forums_slug)
    thread = get_object_or_404(Thread, pk=thread_id)
    data = {
            "forums": forums,
            "title": "Subscriptions",
            "thread": thread,
    }
    if not request.user.is_authenticated():
        return render(request, 'forum/thread/access.html', data)
    if subscribe:
        request.user.forum_subscriptions.add(thread)
        return render(request, 'forum/thread/subscribed.html' , data)
    else:
        request.user.forum_subscriptions.remove(thread)
        return render(request, 'forum/thread/unsubscribed.html' , data)

def unsubscribe(request, forums_slug, thread_id):
    return subscribe(request, forums_slug, thread_id, subscribe=False)

class ThreadListPage(object):
    def __init__(self, name, args):
        self._name = name
        self._args = args if args else {}
    
    def get_absolute_url(self, page=1):
        self._args["page"] = page
        return reverse(self._name, kwargs=self._args)

def show_unanswered(request, forums_slug, page=1):
    forums = get_forum(forums_slug)
    return show_post_list(request, forums, Thread.objects.filter(num_posts=1, forum__category__forums=forums), "Unanswered Posts", page, 'forum-unanswered-posts')

def show_recent(request, forums_slug, page=1):
    forums = get_forum(forums_slug)
    recent = datetime.datetime.now() - datetime.timedelta(days=1)
    return show_post_list(request, forums, Thread.objects.filter(last_post_date__gt=recent, forum__category__forums=forums), "Recent Posts", page, 'forum-recent-posts')

def show_new(request, forums_slug, page=1):
    forums = get_forum(forums_slug)
    recent = get_last_seen(request)
    return show_post_list(request, forums, Thread.objects.filter(last_post_date__gt=recent, forum__category__forums=forums), "Posts Since Last Visit", page, 'forum-since-last-visit-posts')


def show_user_posts(request, forums_slug, user_id=None, page=1):
    forums = get_forum(forums_slug)
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    elif request.user.is_authenticated():
        user = request.user
    else:
        raise Http404
    url_args = {"user_id": user_id} if user_id else None
    posts = Post.objects.filter(author=user, thread__forum__category__forums=forums).values('thread')
    return show_post_list(request, forums, Thread.objects.filter(pk__in=posts), 
                "%s's Posts" % user.username, page, 'forum-user-posts', url_args)

def show_post_list(request, forums, threads_query, title, page, url_name, url_args=None):
    paginator = Paginator(threads_query.select_related(
                'poster', 'last_post__author', 'forum__category__forums'
            ).defer('last_post__message').order_by('-sticky', '-last_post_date'), forums.number_of_threads)
    
    try:
        threads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            if not url_args:
                url_args = {}
            url_args["page"] = paginator.num_pages
            return redirect(reverse(url_name, kwargs=url_args))
    data = {
        "forums": forums,
        "title": title,
        "threads": threads,
        "pages": ThreadListPage(url_name, url_args),
    }
    return render(request, 'forum/thread/list.html' , data)

def moved_forum(request, forums_slug):
    forums = get_forum(forums_slug)
    fid = request.GET.get('id')
    if not re.match(r'^\d+$', str(fid)):
        raise Http404
    return redirect(reverse('forum-view', kwargs={"forums_slug": forums.slug, 'forum_id': fid}))

def moved_thread(request, forums_slug):
    forums = get_forum(forums_slug)
    if request.GET.get('pid'):
        pid = request.GET.get('pid')
        if not re.match(r'^\d+$', str(pid)):
            raise Http404
        return redirect(reverse('forum-view-post', kwargs={"forums_slug": forums.slug, 'post_id': pid}), permanent=True)
    tid = request.GET.get('id')
    if not re.match(r'^\d+$', str(tid)):
        raise Http404
    return redirect(reverse('forum-view-thread', kwargs={"forums_slug": forums.slug, 'thread_id': tid}), permanent=True)
