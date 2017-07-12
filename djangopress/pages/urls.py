from django.conf.urls import url
from djangopress.pages import views

urlpatterns = [
    url(r'^edit/(?P<page>\d+)/(?P<name>[\w\-]+)/$', views.page_edit, name='page-edit'),
    url(r'^edit-ident/(?P<page>\d+)/(?P<identifier>[\w\-]+)/$', views.page_edit, name='page-edit-ident'),
    url(r'^edit/(?P<page>\d+)/$', views.page_edit_details, name='page-edit-details'),
    url(r'^page-edit.js', views.page_edit_js, name='page-edit-js'),
    url(r'^edit/ajax/', views.page_edit_ajax, name='page-edit-ajax'),
]