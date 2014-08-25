from django.conf.urls import patterns, url
from djangopress.blog.feeds import BlogFeed, BlogAtomFeed

urlpatterns = patterns('djangopress.blog.views',
    url(r'^$', 'index', name='blog-index'),
    url(r'^page/(?P<page>\d*)/$', 'index', name='blog-index'),
        
    url(r'^(?P<year>\d{4})/$', 'archive', name='blog-archive'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive', name='blog-archive'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w\-]*)/',
        'post', name='blog-post'),
    url(r'^tag/(?P<slug>[\w\-]+)/', 'tag', name='blog-tag'),
    url(r'^category/(?P<slug>[\w\-]+)/', 'category', name='blog-category'),
    url(r'^feed/$', BlogAtomFeed(), name='blog-feed'),
    url(r'^feed/rss/$', BlogFeed(), name='blog-rss-feed'),

    # rule for backwards compatibility with old site
    url(r'^archive[\-/].*[\-/](?P<post>\d+)/?', 'moved', name='blog-moved'),
)