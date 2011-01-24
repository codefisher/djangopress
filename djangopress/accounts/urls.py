from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('djangopress.accounts.views',
    url(r'^register/$', 'register', name='accounts-register'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^register/thanks/$', 'direct_to_template',
        {'template': 'accounts/registered-message.html'}, name='accounts-registered-message'),
)