from django.conf.urls import patterns, url
from djangopress.blog.feeds import BlogFeed, BlogAtomFeed
from djangopress.blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='blog-index'),
    url(r'^page/(?P<page>\d*)/$', views.index, name='blog-index'),
        
    url(r'^(?P<year>\d{4})/$', views.archive, name='blog-archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.archive, name='blog-archive'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w\-]*)/',
        views.post, name='blog-post'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', views.tag, name='blog-tag'),
    url(r'^tag/(?P<slug>[\w\-]+)/(?P<page>\d*)/$', views.tag, name='blog-tag'),
    url(r'^category/(?P<slug>[\w\-]+)/$', views.category, name='blog-category'),
    url(r'^category/(?P<slug>[\w\-]+)/(?P<page>\d*)/$', views.category, name='blog-category'),

    url(r'^feed/$', BlogAtomFeed(), name='blog-feed'),
    url(r'^feed/rss/$', BlogFeed(), name='blog-rss-feed'),

    # rule for backwards compatibility with old site
    url(r'^archive[\-/].*[\-/](?P<post>\d+)/?', views.moved, name='blog-moved'),
)