from django.conf.urls import patterns, url
from djangopress.forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='forum-index'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.view_thread, name='forum-view-thread'),
    url(r'^thread/(?P<thread_id>\d+)/(?P<page>\d+)/$', views.view_thread, name='forum-view-thread'),
    url(r'^post/(?P<post_id>\d+)/$', views.view_post, name='forum-view-post'),
    url(r'^(?P<forum_id>\d+)/$', views.view_forum, name='forum-view'),
    url(r'^(?P<forum_id>\d+)/(?P<page>\d+)/$', views.view_forum, name='forum-view'),
    url(r'^new-thread/(?P<forum_id>\d+)/$', views.new_thead, name='forum-new-thread'),
    url(r'^reply-thread/(?P<thread_id>\d+)/$', views.reply_thread, name='forum-reply-thread'),
)