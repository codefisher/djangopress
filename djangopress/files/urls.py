from django.conf.urls import patterns, url, include
from .views import upload

urlpatterns = patterns('',
    url(r'^upload/$', upload, name='files-upload'),
)
