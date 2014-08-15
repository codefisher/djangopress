from django.conf.urls import patterns, url

urlpatterns = patterns('djangopress.forum.views',
    url(r'^$', 'index', name='forum-index'),
    url(r'^view-thread//$', 'view_thread', name='forum-view-thread'),
    url(r'^view-forum/(\d+)/$', 'view_forum', name='forum-view'),
    url(r'^new-thread//$', 'new_thead', name='forum-new-thread'),
    url(r'^reply-thread//$', 'reply_thread', name='forum-reply-thread'),
)