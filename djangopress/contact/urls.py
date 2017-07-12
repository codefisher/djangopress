from django.conf.urls import url
from djangopress.contact import views

urlpatterns = [
    url(r'^$', views.contact, name='contact-index'),
    url(r'^thanks/$', views.thanks, name='contact-thanks'),
]
