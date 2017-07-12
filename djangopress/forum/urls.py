from django.conf.urls import url
from djangopress.forum import views
from djangopress.forum.feeds import ForumsAtomFeed, ForumsFeed, ForumAtomFeed, ForumFeed

urlpatterns = [
    url(r'^$', views.index, name='forum-index'),

    url(r'^feed/$', ForumsAtomFeed(), name='forum-feed'),
    url(r'^rss/$', ForumsFeed(), name='forum-rss-feed'),

    url(r'^feed/(?P<forum_id>\d+)/$', ForumAtomFeed(), name='forum-feed'),
    url(r'^rss/(?P<forum_id>\d+)/$', ForumFeed(), name='forum-rss-feed'),

    url(r'^category/(?P<category_id>\d+)/$', views.index, name='forum-category'),

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
    url(r'^new-thread/(?P<forum_id>\d+)/$', views.new_thread, name='forum-new-thread'),
    url(r'^reply-thread/(?P<thread_id>\d+)/$', views.reply_thread, name='forum-reply-thread'),
    
    url(r'^thread/(?P<thread_id>\d+)/subscribe/$', views.subscribe, name='forum-subscribe'),
    url(r'^thread/(?P<thread_id>\d+)/unsubscribe/$', views.unsubscribe, name='forum-unsubscribe'),
    
    url(r'^post/recent/$', views.show_recent, name='forum-recent-posts'),
    url(r'^post/new/$', views.show_new, name='forum-since-last-visit-posts'),
    url(r'^post/unanswered/$', views.show_unanswered, name='forum-unanswered-posts'),
    url(r'^post/user/$', views.show_user_posts, name='forum-user-posts'),
    url(r'^post/user/(?P<user_id>\d+)/$', views.show_user_posts, name='forum-user-posts'),
    url(r'^post/recent/(?P<page>\d+)/$', views.show_recent, name='forum-recent-posts'),
    url(r'^post/unanswered/(?P<page>\d+)/$', views.show_unanswered, name='forum-unanswered-posts'),
    url(r'^post/user/page/(?P<page>\d+)/$', views.show_user_posts, name='forum-user-posts'),
    url(r'^post/user/(?P<user_id>\d+)/(?P<page>\d+)/$', views.show_user_posts, name='forum-user-posts'),
    
    # examples of supporting a legacy forum
    url(r'^viewforum.php', views.moved_forum, name='forum-moved'),
    url(r'^viewtopic.php', views.moved_thread, name='forum-thread-moved'),
]

try:
    from djangopress.core.search import ModelSetSearchForm, search_view_factory
    from djangopress.forum.search import ForumSearchView

    urlpatterns += [
        # the haystack search
        url(r'^search/', search_view_factory(
                view_class=ForumSearchView,
                form_class=ModelSetSearchForm,
                results_per_page=10,
                template='forum/search.html',
                models=["forum.post"],
            ), name='haystack-forum-search'),
    ]
except ImportError:
    pass
