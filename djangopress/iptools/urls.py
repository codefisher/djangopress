from django.conf.urls import url
from djangopress.iptools import views

urlpatterns = [
    url(r'^$', views.index, name='iptools-index'),
]
