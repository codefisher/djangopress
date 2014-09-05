from django.conf.urls import patterns, url
from djangopress.contact import views

urlpatterns = patterns('',
    url(r'^$', views.contact, name='contact-index'),
    url(r'^thanks/$', views.thanks, name='contact-thanks'),
)
