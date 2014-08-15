from django.conf.urls import patterns, url, include

urlpatterns = patterns('djangopress.pages.views',
    url(r'^edit/(?P<page>\d+)/(?P<name>[\w\-]+)/$', 'page_edit', name='page-edit'),
    url(r'^edit-ident/(?P<page>\d+)/(?P<identifier>[\w\-]+)/$', 'page_edit', name='page-edit-ident'),
    url(r'^edit/(?P<page>\d+)/$', 'page_edit_details', name='page-edit-details'),
    url(r'^page-edit.js', 'page_edit_js', name='page-edit-js'),
    url(r'^edit/ajax/', 'page_edit_ajax', name='page-edit-ajax'),
)