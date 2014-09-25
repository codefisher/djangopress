from django import template
from djangopress.forum.views import get_forum
from djangopress.forum.models import Post
from djangopress.core.util import has_permission
from django.core.urlresolvers import reverse
from djangopress.core.format import Library

register = template.Library()

@register.simple_tag
def format_post(post, user):
    formating = Library.get(post.format).get("function")
    smilies = post.show_similies
    show_images = True
    if user.is_authenticated() and user.forum_profile.pk:
        smilies = user.forum_profile.show_simlies if not user.forum_profile.show_simlies else smilies
        show_images = user.forum_profile.show_img
    return formating(post.message, smilies=smilies, show_images=show_images)

@register.inclusion_tag('forum/post/latest.html')
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

@register.inclusion_tag('forum/post/actions.html')
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