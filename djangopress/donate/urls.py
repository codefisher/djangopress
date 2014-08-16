from django.conf.urls import patterns, url

urlpatterns = patterns('djangopress.donate.views',
    url(r'^$', 'index', name='donate-index'),
    url(r'^thanks$', 'thanks', name='donate-thanks'),
    url(r'^process', 'process', name='donate-process'),
)
