from django.conf.urls.defaults import*

urlpatterns = patterns('djangopress.blog',
    (r'^$', 'index'),
    (r'^(?P<year>\d{4})/(?P<year>\d{1,2})/$', 'archive'),
    (r'^(?P<year>\d{4})/(?P<year>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w\-]*)/',
        'post'),
    (r'^tag/(?P<slug>[\w\-]*)/', 'tag'),
    (r'^category/(?P<slug>[\w\-]*)/', 'category'),

    # rule for backwards compatibility with old site
)