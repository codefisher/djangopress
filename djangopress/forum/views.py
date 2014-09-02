import datetime
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import models
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.http.response import Http404
from djangopress.forum.models import ForumGroup, ForumCategory, Forum, Thread, Post, ForumUser, THREADS_PER_PAGE, POSTS_PER_PAGE
from djangopress.core.util import get_client_ip, get_recaptcha_html, recaptcha_is_valid, has_permission
from djangopress.forum.forms import PostAnonymousForm, PostEditForm, PostForm, ReportForm, ThreadForm

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

def moderator_forum(request):
    #needs to be the same as view_forum, but can move, delete, open or close any topic in batch.
    pass

def view_forum(request, forums_slug, forum_id, page=1):
    forums = get_forum(forums_slug)
    forum = get_object_or_404(Forum.objects.select_related('category__forums'), pk=forum_id)
    
    paginator = Paginator(Thread.objects.filter(forum=forum).select_related(
                'poster', 'last_post__author', 'forum__category__forums'
            ).defer('last_post__message').order_by('-sticky', '-last_post_date'), THREADS_PER_PAGE)
    
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
    if not has_permission(request, 'forum', 'can_post_threads'):
        data = {
                "forums": forums,
                "forum": forum,
                "title": "Permission denied to post thread",
                "anonymous": not request.user.is_authenticated(),
        }
        return render(request, 'forum/thread_new_denied.html' , data)
    recaptcha_error = None
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        if request.user.is_authenticated():
            post_form = PostForm(request.POST)
        else:
            post_form = PostAnonymousForm(request.POST)
        recapatcha = recaptcha_is_valid(request)
        if thread_form.is_valid() and post_form.is_valid() and recapatcha:
            thread = thread_form.save(commit=False)
            if request.user.is_authenticated():
                thread.poster = request.user
            else:
                thread.poster_name = post_form.cleaned_data["poster_name"]
                thread.poster_email = post_form.cleaned_data["poster_email"]
            thread.forum = forum
            thread.save()
            site = Site.objects.get_current()
            for user in forum.subscriptions.all():
                if user == request.user:
                    continue
                # should check here if the last post was after the user last visted
                # in which cause we don't need to email them
                message_data = {
                    "site": site,
                    "user": user,
                    "thread": thread,
                    "forums": forums,
                    "scheme": "https" if request.is_secure() else "http",
                }
                message = render_to_string('forum/forum_subscription_notification.txt', message_data)
                user.email_user("Forum Subscription Notification for %s" % forums.name, message)
            return process_post(request, thread, post_form, forums)
        if not recapatcha:
            recaptcha_error = "The verification failed, please try again."
    else:
        thread_form = ThreadForm()
        if request.user.is_authenticated():
            post_form = PostForm()
        else:
            post_form = PostAnonymousForm()
    data = {
        "forums": forums,
        "forum": forum,
        "title": "%s :: New Thread" % forum.name,
        "thread_form": thread_form,
        "recaptcha": get_recaptcha_html(),
        "recaptcha_error": recaptcha_error,
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
    thread.num_views = models.F('num_views') + 1
    thread.save()
    
    data = {
        "forums": forums,
        "thread": thread,
        "title": thread.subject,
        "posts": posts,
    }
    return render(request, 'forum/thread.html' , data)

def view_post(request, forums_slug, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post_id))

def last_post(request, forums_slug, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    post = Post.objects.filter(thread=thread, is_spam=False, is_public=True
                    ).select_related('author', 'thread').order_by('posted')
    return HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))

def process_post(request, thread, post_form, forums):
    post = post_form.save(commit=False)
    if request.user.is_authenticated():
        forum_profile, created = ForumUser.objects.get_or_create(user=request.user)
        if forum_profile.notify == 'AL' and not request.user.forum_forum_subscriptions.exists():
            thread.subscriptions.add(request.user)
        post.author = request.user    
    post.is_spam = check_askmet_spam(request, post, post_form)
    post.ip = get_client_ip(request)
    post.thread = thread
    post.format = forums.format
    post.save()
    site = Site.objects.get_current()
    for user in thread.subscriptions.all():
        if user == request.user:
            continue
        # should check here if the last post was after the user last visted
        # in which cause we don't need to email them
        message_data = {
            "site": site,
            "user": user,
            "thread": thread,
            "forums": forums,
            "post": post,
            "scheme": "https" if request.is_secure() else "http",
        }
        message = render_to_string('forum/subscription_notification.txt', message_data)
        user.email_user("Topic Subscription Notification for %s" % forums.name, message)
    data = {
            "post": post,
            "title": "Post Submitted",
            "thread": thread,
            "forums": forums,
    }
    responce = render(request, 'forum/posted.html' , data)
    if not post.is_spam and post.is_public:
        responce["Refresh"] = "3;%s" % reverse('forum-view-post', kwargs={"forums_slug": forums.slug, "post_id": post.pk})
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
        return render(request, 'forum/closed.html' , data)
    if not has_permission(request, 'forum', 'can_post_replies'):
        data = {
                "forums": forums,
                "title": "Permission Denied",
                "thread": thread,
                "anonymous": not request.user.is_authenticated(),
        }
        return render(request, 'forum/thread_denied.html' , data)
    recaptcha_error = None
    if request.method == 'POST':
        if request.user.is_authenticated():
            post_form = PostForm(request.POST)
        else:
            post_form = PostAnonymousForm(request.POST)
        recapatcha = recaptcha_is_valid(request)
        if post_form.is_valid() and recapatcha:
            return process_post(request, thread, post_form, forums)
        if not recapatcha:
            recaptcha_error = "The verification failed, please try again."
    else:
        if request.user.is_authenticated():
            post_form = PostForm()
        else:
            post_form = PostAnonymousForm()
    data = {
        "forums": forums,
        "thread": thread,
        "title": "%s :: Post Reply" % thread.subject,
        "recaptcha": get_recaptcha_html(),
        "recaptcha_error": recaptcha_error,
        "post_form": post_form,
    }
    return render(request, 'forum/reply.html' , data)

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
        return HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
    else:
        report_form = ReportForm()
    data = {
            "post": post,
            "title": "Report Post",
            "forums": forums,
            "report_form": report_form
    }
    return render(request, 'forum/report.html' , data)

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
        return render(request, 'forum/post_edit_denied.html' , data)
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
            return HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
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
    return render(request, 'forum/post_edit.html' , data)
    
def post_action(request, forums_slug, post_id, redirect_before, do_action, name, message):
    forums = get_forum(forums_slug)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST' and request.POST.get('post'):
        if redirect_before:
            redirect = HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
        do_action(post)
        post.save()
        if not redirect_before:
            redirect = HttpResponseRedirect("%s#p%s" % (post.thread.get_absolute_url(post.get_page()), post.pk))
        return redirect
    data = {
            "post": post,
            "title": name,
            "forums": forums,
            "message": message,
            "name": name,
    }
    return render(request, 'forum/post_action.html' , data)
    
def delete_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_public = False
    return post_action(request, forums_slug, post_id, True, do_action, "Delete Post", "delete the post")

def restore_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_public = True
    return post_action(request, forums_slug, post_id, False, do_action, "Restore Post", "restore the post")
    
def spam_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_spam = True
        # we we could call upon akismet
    return post_action(request, forums_slug, post_id, True, do_action, "Mark as Spam", "mark the post as spam")
    
def not_spam_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_spam = False
    return post_action(request, forums_slug, post_id, False, do_action, "Mark as Not Spam", "mark the post as not span")
    
def remove_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_removed = True
    return post_action(request, forums_slug, post_id, True, do_action, "Remove", "mark the post as removed")
    
    
def recover_post(request, forums_slug, post_id):
    def do_action(post):
        post.is_removed = False
    return post_action(request, forums_slug, post_id, True, do_action, "Restore", "mark the post as not removed")
    
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
            ).defer('last_post__message').order_by('-sticky', '-last_post_date'), THREADS_PER_PAGE)
    
    try:
        threads = paginator.page(page)
    except (EmptyPage, InvalidPage):
        if not url_args:
            url_args = {}
        url_args["page"] = paginator.num_pages
        return HttpResponseRedirect(reverse(url_name, kwargs=url_args))

    data = {
        "forums": forums,
        "title": title,
        "threads": threads,
        "pages": ThreadListPage(url_name, url_args),
    }
    return render(request, 'forum/thread/list.html' , data)

def moved_forum(request, forums_slug):
    return HttpResponseRedirect(reverse('forum-view', kwargs={'forum_id': request.GET.get('id')}))

def moved_thread(request, forums_slug):
    if request.GET.get('pid'):
            return HttpResponseRedirect(reverse('forum-view-post', kwargs={'post_id': request.GET.get('pid')}))
    return HttpResponseRedirect(reverse('forum-view-thread', kwargs={'thread_id': request.GET.get('id')}))