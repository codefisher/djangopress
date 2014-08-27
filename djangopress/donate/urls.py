from django.conf.urls import patterns, url
from djangopress.donate import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='donate-index'),
    url(r'^thanks$', views.thanks, name='donate-thanks'),
    url(r'^process', views.process, name='donate-process'),
)
