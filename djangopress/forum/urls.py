from django.conf.urls import patterns, url
from djangopress.forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='forum-index'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.view_thread, name='forum-view-thread'),
    url(r'^thread/(?P<thread_id>\d+)/(?P<page>\d+)/$', views.view_thread, name='forum-view-thread'),
    url(r'^thread/(?P<thread_id>\d+)/last/$', views.last_post, name='forum-last-post'),
    url(r'^post/(?P<post_id>\d+)/$', views.view_post, name='forum-view-post'),

    url(r'^post/report/(?P<post_id>\d+)/$', views.report_post, name='forum-report-post'),
    url(r'^post/edit/(?P<post_id>\d+)/$', views.edit_post, name='forum-edit-post'),
    url(r'^post/delete/(?P<post_id>\d+)/$', views.delete_post, name='forum-delete-post'),
    url(r'^post/recover/(?P<post_id>\d+)/$', views.recover_post, name='forum-recover-post'),
    url(r'^post/spam/(?P<post_id>\d+)/$', views.spam_post, name='forum-spam-post'),
    url(r'^post/not/spam/(?P<post_id>\d+)/$', views.not_spam_post, name='forum-notspam-post'),
    url(r'^post/remove/(?P<post_id>\d+)/$', views.remove_post, name='forum-remove-post'),
    url(r'^post/restore/(?P<post_id>\d+)/$', views.restore_post, name='forum-restore-post'),


    url(r'^(?P<forum_id>\d+)/$', views.view_forum, name='forum-view'),
    url(r'^(?P<forum_id>\d+)/(?P<page>\d+)/$', views.view_forum, name='forum-view'),
    url(r'^new-thread/(?P<forum_id>\d+)/$', views.new_thead, name='forum-new-thread'),
    url(r'^reply-thread/(?P<thread_id>\d+)/$', views.reply_thread, name='forum-reply-thread'),
)