from django.conf.urls import patterns, url
from djangopress.accounts import views

urlpatterns = patterns('',
    url(r'^$', views.user_profile, name='accounts-profile'),
    url(r'^(?P<username>.+)/$', views.user_profile, name='accounts-profile'),
    url(r'^(?P<username>.+)/(?P<tab>\w+)/$', views.user_profile, name='accounts-profile'),
)