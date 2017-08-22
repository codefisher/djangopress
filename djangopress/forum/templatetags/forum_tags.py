from django import template
from django.conf import settings
from djangopress.forum.models import Thread, Post
from djangopress.core.util import has_permission
from django.urls import reverse
from djangopress.core.format.library import Library
import djangopress.core.format.nodes as nodes

register = template.Library()

class TopicNode(nodes.ArgumentedNode):
    def __init__(self, token, string, arg, kargs, nodelist):
        super(TopicNode, self).__init__(token, string, arg, kargs, nodelist)
        
    def render(self, context, **kwargs):
        try:
            topic = Thread.objects.select_related('forum__category__forums').get(pk=self.arg if self.arg else self.kargs.get('id')).exclude(first_post=None)
        except Thread.DoesNotExist:
            return ''
        return """<a href="%s">%s</a>""" % (topic.get_absolute_url(), self.nodelist.render(context, **kwargs))

nodes.Library.argumented_tag("topic", '', cls=TopicNode)

class PostNode(nodes.ArgumentedNode):
    def __init__(self, token, string, arg, kargs, nodelist):
        super(PostNode, self).__init__(token, string, arg, kargs, nodelist)
        
    def render(self, context, **kwargs):
        try:
            post = Post.objects.select_related('thread__forum__category__forums').get(pk=self.arg if self.arg else self.kargs.get('id'), is_spam=False, is_public=True)
        except Post.DoesNotExist:
            return ''
        return """<a href="%s">%s</a>""" % (post.get_absolute_url(), self.nodelist.render(context, **kwargs))

nodes.Library.argumented_tag("post", '', cls=PostNode)

class QuoteNode(nodes.ArgumentedNode):
    def __init__(self, token, string, arg, kargs, nodelist):
        super(QuoteNode, self).__init__(token, string, arg, kargs, nodelist)
        
    def render(self, context, **kwargs):
        try:
            post = Post.objects.defer('message').select_related('thread__forum__category__forums').get(pk=self.kargs.get('post'), is_spam=False, is_public=True)
            self.kargs["post_url"] = post.get_absolute_url()
        except Post.DoesNotExist:
            pass
        return super(QuoteNode, self).render(context, **kwargs)

nodes.Library.argumented_tag("quote", '<div class="quote"><span class="title">QUOTE: {% if name %}{{ name }}{% endif %}{% if date %} @ {{ date }}{% endif %}{% if post_url %} <a href="{{post_url}}">*</a>{% endif %}</span><blockquote>{{ content }}</blockquote></div>', cls=QuoteNode)


def format_post(context, post, user=None, forums=None):
    formating = Library.get(post.format).get("function")
    smilies = post.show_similies
    show_images = True
    if user and user.is_authenticated() and hasattr(user, 'forum_profile'):
        smilies = user.forum_profile.show_simlies if not user.forum_profile.show_simlies else smilies
        show_images = user.forum_profile.show_img
    if not forums:
        forums = post.thread.forum.category.forums
    show_images = show_images and forums.display_images
    smilies = smilies and forums.show_smilies
    return formating(post.message, context=context, smilies=smilies, show_images=show_images, should_urlize=forums.make_links)

register.simple_tag(format_post, takes_context=True)

@register.inclusion_tag('forum/post/latest.html')
def show_latest_posts(forums_slug, number=5):
    try:
        number = int(number)
    except ValueError:
        number = 5
    threads = Thread.objects.filter(forum__category__forums__slug=forums_slug,
                                    last_post__is_spam=False, last_post__is_public=True,
                                    last_post__is_removed=False,
                                    forum__category__forums__sites__id__exact=settings.SITE_ID).exclude(last_post=None).order_by('-last_post_date').select_related('last_post',
                                    'last_post__thread__forum__category__forums')[0:number]
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
    
class SignatureNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
        
    def render(self, context):
        post = context.get('post')
        user = context.get('user')
        forums = context.get('forums')
        if ((post.author and post.author.profile.signature and forums.show_signature) 
            and (not user.is_authenticated() or not hasattr(user, 'forum_profile') or user.forum_profile.show_sig)): 
            return self.nodelist.render(context)
        return ""
    
def do_should_show_signiture(parser, token):
    nodelist = parser.parse(('end_should_show_signiture',))
    parser.delete_first_token()
    return SignatureNode(nodelist)

register.tag('should_show_signiture', do_should_show_signiture)