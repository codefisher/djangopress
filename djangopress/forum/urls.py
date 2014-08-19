from django.conf.urls import patterns, url

urlpatterns = patterns('djangopress.forum.views',
    url(r'^$', 'index', name='forum-index'),
    url(r'^thread//$', 'view_thread', name='forum-view-thread'),
    url(r'^(?P<forum_id>\d+)/$', 'view_forum', name='forum-view'),
    url(r'^(?P<forum_id>\d+)/(?P<page>\d+)/$', 'view_forum', name='forum-view-page'),
    url(r'^new-thread/(?P<forum_id>\d+)/$', 'new_thead', name='forum-new-thread'),
    url(r'^reply-thread//$', 'reply_thread', name='forum-reply-thread'),
)