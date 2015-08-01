from django.conf.urls import patterns, url, include
from .views import index, gallery

urlpatterns = patterns('',
	url(r'^$', index, name='gallery-index'),
	url(r'^(?P<slug>.+)/$', gallery, name='gallery-gallery'),
)
