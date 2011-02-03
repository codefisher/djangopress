from django.conf.urls.defaults import patterns, url
from djangopress.core.sitemap import register, autodiscover

autodiscover()

sitemap_patterns = patterns('django.contrib.sitemaps.views',
    url(r'sitemap\.xml', 'sitemap', {'sitemaps': register.get_sitemaps()}, name="sitemap")
)