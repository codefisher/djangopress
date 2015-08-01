from django.conf.urls import patterns, url, include
from .views import index, gallery, upload

urlpatterns = patterns('',
	url(r'^$', index, name='gallery-index'),
    url(r'^upload/$', upload, name='gallery-upload'),
	url(r'^(?P<slug>.+)/$', gallery, name='gallery-gallery'),
)
