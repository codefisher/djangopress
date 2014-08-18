from django.conf.urls import patterns, url

urlpatterns = patterns('djangopress.contact.views',
    url(r'^$', 'contact', name='contact-index'),
)
