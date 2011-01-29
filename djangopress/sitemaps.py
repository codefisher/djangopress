from django.conf.urls.defaults import patterns, url
from djangopress.blog.sitemaps import (BlogSitemap, CategorySitemap,
            EntrySitemap, TagSitemap)

sitemaps = {
    'blog': BlogSitemap,
    'category': CategorySitemap,
    'entry': EntrySitemap,
    'tag': TagSitemap
}


sitemap_patterns = patterns('django.contrib.sitemaps.views',
    url(r'sitemap\.xml', 'sitemap', {'sitemaps': sitemaps}, name="sitemap")
)