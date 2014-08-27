from django.conf.urls import patterns, url
from djangopress.accounts.profiles import autodiscover

autodiscover() # find all the parts for the profile pages

urlpatterns = patterns('djangopress.accounts.views',
    url(r'^register/$', 'register', name='accounts-register'),
    url(r'^register/confirm/(?P<username>.+)/(?P<activate_key>.+)/', 'activate', name='accounts-confirm'),
    url(r'^register/reactivate/(?P<username>.+)/$', 'reactivate', name='accounts-reactivate'),
    url(r'^$', 'user_list', name='accounts-userlist'),
    
    url(r'^admin/(?P<username>.+)/$', 'user_admin', name='accounts-admin'),

    url(r'^registered/(?P<username>.+)/$', 'registered', name='accounts-registered'),
    url(r'^register/activated/(?P<username>.+)/$', 'activated', name='accounts-activated'),
    url(r'^register/already-activated/(?P<username>.+)/$', 'already_activated', name='accounts-already-activated'),
    url(r'^register/invalid-activation/(?P<username>.+)/$', 'invalid_activation', name='accounts-activation-invalid'),
    url(r'^register/resent-activation/(?P<username>.+)/$', 'resent_activation', name='accounts-activation-resent'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^password_change/$', 'password_change', {
            "post_change_redirect": "../profile/",
            "template_name": "accounts/password_change_form.html"
         }, name='password_change'),
    #url(r'^password_change_done/$', 'password_change_done', name='password_change_done'),
    url(r'^password_reset/$', 'password_reset', {
                "template_name": "accounts/password_reset_form.html",
                "email_template_name": "accounts/password_reset_email.html",
                "subject_template_name": "accounts/password_reset_subject.txt",
            }, name='password_reset'),
    url(r'^password_reset/done/$', 'password_reset_done', {
                "template_name": "accounts/password_reset_done.html"
            }, name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'password_reset_confirm', {
                "template_name": "accounts/password_reset_confirm.html"
            }, name='password_reset_confirm'),
    url(r'^password_reset/complete/$', 'password_reset_complete', {
                "template_name": "accounts/password_reset_complete.html"
            }, name='password_reset_complete'),
)