from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('djangopress.accounts.views',
    url(r'^register/$', 'register', name='accounts-register'),
    url(r'^register/confirm/(?P<user>.+)/(?P<activate_key>.+)/', 'activate', name='accounts-confirm'),
    url(r'^register/reactivate/(?P<user>.+)/$', 'reactivate', name='accounts-reactivate'),
    url(r'^$', 'user_list', name='accounts-userlist'),
    url(r'^profile/((?P<username>.+)/((?P<tab>\w+)/)?)?$', 'user_profile', name='accounts-user-profile'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='accounts-login'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^register/thanks/$', 'direct_to_template',
        {'template': 'accounts/messages/registered-message.html'}, name='accounts-registered'),
    url(r'^register/activated/$', 'direct_to_template',
        {'template': 'accounts/messages/account_activated.html'}, name='accounts-activated'),
    url(r'^register/already-activated/$', 'direct_to_template',
        {'template': 'accounts/messages/already_activated.html'}, name='accounts-already-activated'),
    url(r'^register/invalid-activation/(?P<user>.+)/$', 'direct_to_template',
        {'template': 'accounts/messages/invalid_activation.html'}, name='accounts-activation-invalid'),
    url(r'^register/resent-activation/$', 'direct_to_template',
        {'template': 'accounts/messages/resent_activation.html'}, name='accounts-activation-resent'),
)