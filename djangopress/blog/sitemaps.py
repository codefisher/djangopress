from django.contrib.sitemaps import Sitemap
from djangopress.blog.models import Entry, Blog, Category, Tag
from djangopress.core.sitemap import register

#todo, add last mod field for Category and Tag

class EntrySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.get_entries(sorted=False)

    def lastmod(self, obj):
        return obj.edited

register('blog-entry', EntrySitemap)

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    lastmod = None

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return Entry.get_entries(blog=obj)[0].edited

register('blog', BlogSitemap)

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.1
    lastmod = None

    def items(self):
        return Category.objects.all()

register('blog-category', CategorySitemap)

class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.1
    lastmod = None

    def items(self):
        return Tag.objects.all()

register('blog-tag', TagSitemap)