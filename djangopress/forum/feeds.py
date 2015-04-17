from djangopress.forum.models import Post, ForumGroup, Forum
from djangopress.forum.templatetags.forum_tags import format_post
from djangopress.forum.views import get_forum
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

class ForumsFeed(Feed):
    def get_object(self, request, forums_slug=None):
        return get_forum(forums_slug)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.tagline

    def items(self, obj):
        return Post.objects.filter(thread__forum__category__forums=obj, is_spam=False, is_public=True
                    ).select_related('author', 'thread', 'thread__forum__category__forums',).order_by('-posted')[0:15]

    def item_title(self, item):
        return item.thread.subject

    def item_description(self, item):
        return format_post(None, item)

    def item_author_name(self, item):
        return item.author_name()

    def item_pubdate(self, item):
        return item.posted

    def item_updateddate(self, item):
        if item.edited:
            return item.edited
        return item.posted

    def item_categories(self, item):
        return [item.thread.forum.name]

class ForumsAtomFeed(ForumsFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return self.description(obj)

class ForumFeed(ForumsFeed):

    def get_object(self, request, forums_slug=None, forum_id=None):
        forums = get_forum(forums_slug)
        return get_object_or_404(Forum.objects.select_related('category', 'category__forums'), pk=forum_id)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return Post.objects.filter(thread__forum=obj, is_spam=False, is_public=True
                    ).select_related('author', 'thread', 'thread__forum__category__forums',).order_by('-posted')[0:15]

class ForumAtomFeed(ForumFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return self.description(obj)