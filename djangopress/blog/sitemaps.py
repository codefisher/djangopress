from django.contrib.sitemaps import Sitemap
from djangopress.blog.models import Entry, Blog, Category, Tag
from djangopress.core.sitemap import register
from django.conf import settings

#todo, add last mod field for Category and Tag

class EntrySitemap(Sitemap):
 
    def items(self):
        return Entry.objects.get_entries(ordered=False).filter(blog__sites__id__exact=settings.SITE_ID)

    def lastmod(self, obj):
        return obj.edited

register('blog-entry', EntrySitemap)

class BlogSitemap(Sitemap):
    lastmod = None

    def items(self):
        return Blog.objects.filter(sites__id__exact=settings.SITE_ID)

    def lastmod(self, obj):
        try:
            return Entry.objects.get_entries(blog=obj)[0].edited
        except:
            return None

register('blog', BlogSitemap)

class CategorySitemap(Sitemap):
    lastmod = None

    def items(self):
        return Category.objects.filter(blog__sites__id__exact=settings.SITE_ID)

register('blog-category', CategorySitemap)

class TagSitemap(Sitemap):
    lastmod = None

    def items(self):
        return Tag.objects.filter(blog__sites__id__exact=settings.SITE_ID)

register('blog-tag', TagSitemap)