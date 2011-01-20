from djangopress.blog.models import Blog, Entry
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed

class BlogFeed(Feed):

    def get_object(self, request, blog=None):
        return get_object_or_404(Blog, slug=blog)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        kwargs = {}
        if obj.slug:
            kwargs["blog"] = obj.slug
        return reverse("blog-index", kwargs=kwargs)

    def description(self, obj):
        return obj.tagline

    def items(self, obj):
        return Entry.objects.filter(blog=obj).order_by('-sticky', '-posted')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.perma_link()

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return item.posted

    def item_categories(self, item):
        return (str(category) for category in item.categories.all())

class BlogAtomFeed(BlogFeed):
    feed_type = Atom1Feed

    def subtitle(self, obj):
        return self.description(obj)