from django.conf.urls import url
from djangopress.donate import views

urlpatterns = [
    url(r'^$', views.index, name='donate-index'),
    url(r'^thanks$', views.thanks, name='donate-thanks'),
]
