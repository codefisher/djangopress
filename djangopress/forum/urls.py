from django.conf.urls import patterns, url

urlpatterns = patterns('djangopress.forum.views',
    url(r'^$', 'index', name='forum-index'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'view_thread', name='forum-view-thread'),
    url(r'^thread/(?P<thread_id>\d+)/(?P<page>\d+)/$', 'view_thread', name='forum-view-thread'),
    url(r'^post/(?P<post_id>\d+)/$', 'view_post', name='forum-view-post'),
    url(r'^(?P<forum_id>\d+)/$', 'view_forum', name='forum-view'),
    url(r'^(?P<forum_id>\d+)/(?P<page>\d+)/$', 'view_forum', name='forum-view'),
    url(r'^new-thread/(?P<forum_id>\d+)/$', 'new_thead', name='forum-new-thread'),
    url(r'^reply-thread/(?P<thread_id>\d+)/$', 'reply_thread', name='forum-reply-thread'),
)