from django.conf.urls import patterns, url
from djangopress.iptools import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='iptools-index'),
)
