from django.conf.urls import url
from .views import index, gallery, upload

urlpatterns = [
	url(r'^$', index, name='gallery-index'),
    url(r'^upload/$', upload, name='gallery-upload'),
	url(r'^(?P<slug>.+)/$', gallery, name='gallery-gallery'),
]
