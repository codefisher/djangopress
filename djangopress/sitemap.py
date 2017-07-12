from django.conf.urls import url
from djangopress.core.sitemap import register, autodiscover
from django.contrib.sitemaps import views

autodiscover()

sitemap_patterns = [
    url(r'sitemap\.xml', views.sitemap, {'sitemaps': register.get_sitemaps()}, 
        name='django.contrib.sitemaps.views.sitemap')
]