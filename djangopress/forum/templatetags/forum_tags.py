from django import template
from djangopress.forum.views import get_forum
from djangopress.forum.models import Post
from djangopress.core.util import has_permission
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('forum/latest-posts.html')
def show_latest_posts(forums_slug, number=5):
    try:
        number = int(number)
    except ValueError:
        number = 5
    try:
        forums = get_forum(forums_slug)
    except:
        return {} # the forum must not exist, so we fail quitely
    posts = Post.objects.filter(thread__forum__category__forums=forums, is_spam=False, is_public=True
                    ).select_related('thread').order_by('-posted')
    try:
        # we force to a list to see if the NotImplementedError error happens
        # only works in PostgreSQL
        posts = list(posts.distinct('thread__subject'))
    except NotImplementedError:
        posts = posts[0:number]
    return {
        "posts": posts,
    }

    url(r'^post/report/(?P<post_id>\d+)/$', views.report_post, name='forum-report-post'),
    url(r'^post/edit/(?P<post_id>\d+)/$', views.edit_post, name='forum-edit-post'),
    url(r'^post/delete/(?P<post_id>\d+)/$', views.delete_post, name='forum-delete-post'),
    url(r'^post/restore/(?P<post_id>\d+)/$', views.restore_post, name='forum-restore-post'),
    url(r'^post/spam/(?P<post_id>\d+)/$', views.spam_post, name='forum-spam-post'),
    url(r'^post/not/spam/(?P<post_id>\d+)/$', views.not_spam_post, name='forum-notspam-post'),
    url(r'^post/remove/(?P<post_id>\d+)/$', views.remove_post, name='forum-remove-post'),
    url(r'^post/recover/(?P<post_id>\d+)/$', views.recover_post, name='forum-recover-post'),


@register.inclusion_tag('forum/post_actions.html')
def post_actions(post, request):
    forum_slug = post.thread.forum.category.forums.slug
    kwargs = {"forums_slug": forum_slug, 'post_id': post.id}
    actions = [{"name": "Report", "url": reverse("forum-report-post", kwargs=kwargs)}]
    if request.user.is_authenticated():
        if post.author == request.user and has_permission(request, 'forum', 'can_edit_own_posts'):
            actions.append({"name": "Edit", "url": reverse("forum-edit-post", kwargs=kwargs)})
        elif has_permission(request, 'forum', 'can_edit_others_posts'):
            actions.append({"name": "Edit", "url": reverse("forum-edit-post", kwargs=kwargs)})
        if has_permission(request, 'forum', 'can_mark_removed'):
            if post.is_removed:
                actions.append({"name": "Mark Not Removed", "url": reverse("forum-recover-post", kwargs=kwargs)})
            else:
                actions.append({"name": "Mark Removed", "url": reverse("forum-remove-post", kwargs=kwargs)})
        if has_permission(request, 'forum', 'can_mark_public'):
            if post.is_public:
                actions.append({"name": "Delete", "url": reverse("forum-delete-post", kwargs=kwargs)})
            else:
                actions.append({"name": "Restore", "url": reverse("forum-restore-post", kwargs=kwargs)})
        if has_permission(request, 'forum', 'can_mark_spam'):
            if post.is_spam:
                actions.append({"name": "Not Spam", "url": reverse("forum-notspam-post", kwargs=kwargs)})
            else:
                actions.append({"name": "Spam", "url": reverse("forum-spam-post", kwargs=kwargs)})
    return {
            "actions": actions
    }