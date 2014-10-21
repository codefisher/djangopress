from django import template
from djangopress.forum.views import get_forum
from djangopress.forum.models import Thread
from djangopress.core.util import has_permission
from django.core.urlresolvers import reverse
from djangopress.core.format import Library

register = template.Library()

@register.simple_tag
def format_post(post, user=None):
    formating = Library.get(post.format).get("function")
    smilies = post.show_similies
    show_images = True
    if user and user.is_authenticated() and user.forum_profile.pk:
        smilies = user.forum_profile.show_simlies if not user.forum_profile.show_simlies else smilies
        show_images = user.forum_profile.show_img
    forms = post.thread.forum.category.forums
    show_images = show_images and forms.display_images
    smilies = smilies and forms.show_smilies
    return formating(post.message, smilies=smilies, show_images=show_images, should_urlize=forms.make_links)

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
    threads = Thread.objects.filter(forum__category__forums=forums).exclude(last_post=None).order_by('-last_post_date').select_related('last_post')[0:number]
    return {
        "threads": threads,
    }

@register.inclusion_tag('forum/post/actions.html', takes_context=True)
def post_actions(context, post):
    request = context['request']
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
    
@register.inclusion_tag('forum/thread/actions.html', takes_context=True)
def thread_actions(context, thread):
    request = context['request']
    forum_slug = thread.forum.category.forums.slug
    kwargs = {"forums_slug": forum_slug, "thread_id": thread.pk}
    actions = []
    if request.user.is_authenticated():
        if request.user.forum_subscriptions.exists():
            actions.append({"name": "Unsubscribe", "url": reverse("forum-unsubscribe", kwargs=kwargs)})
        else:
            actions.append({"name": "Subscribe", "url": reverse("forum-subscribe", kwargs=kwargs)})
    return {
            "actions": actions
    }  