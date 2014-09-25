from django.conf.urls import patterns, url
from djangopress.accounts.profiles import autodiscover
from djangopress.accounts import views
from django.contrib.auth import views as auth_views

autodiscover() # find all the parts for the profile pages

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='accounts-register'),
    url(r'^register/confirm/(?P<username>.+)/(?P<activate_key>.+)/', views.activate, name='accounts-confirm'),
    url(r'^register/reactivate/(?P<username>.+)/$', views.reactivate, name='accounts-reactivate'),
    url(r'^$', views.user_list, name='accounts-userlist'),
    url(r'^(?P<page>\d+)/$', views.user_list, name='accounts-userlist'),
    
    url(r'^admin/(?P<username>.+)/$', views.user_admin, name='accounts-admin'),

    url(r'^registered/(?P<username>.+)/$', views.registered, name='accounts-registered'),
    url(r'^register/activated/(?P<username>.+)/$', views.activated, name='accounts-activated'),
    url(r'^register/already-activated/(?P<username>.+)/$', views.already_activated, name='accounts-already-activated'),
    url(r'^register/invalid-activation/(?P<username>.+)/$', views.invalid_activation, name='accounts-activation-invalid'),
    url(r'^register/resent-activation/(?P<username>.+)/$', views.resent_activation, name='accounts-activation-resent'),
    
    # the default location after someone has logged in
    url(r'^profile/$', views.user_profile, name='accounts-profile-alt'),
    
    url(r'^banned/(?P<username>.+)/$', views.you_are_banned, name='accounts-banned'),

    url(r'^user/$', views.user_profile, name='accounts-profile'),
    url(r'^user/(?P<username>.+?)/(?P<tab>.+?)/$', views.user_profile, name='accounts-profile'),
    url(r'^user/(?P<username>.+?)/$', views.user_profile, name='accounts-profile'),
)

urlpatterns += patterns('',
    url(r'^login/$', auth_views.login, {
            "template_name": "accounts/login.html"
        }, name='login'),
    url(r'^logout/$', auth_views.logout, {
            "template_name": "accounts/logged_out.html"
        },  name='logout'),
    url(r'^password_change/$', auth_views.password_change, {
            "post_change_redirect": "/user/",
            "template_name": "accounts/password_change_form.html"
         }, name='password_change'),
    #url(r'^password_change_done/$', 'password_change_done', name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, {
                "template_name": "accounts/password_reset_form.html",
                "email_template_name": "accounts/password_reset_email.html",
                "subject_template_name": "accounts/password_reset_subject.txt",
            }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {
                "template_name": "accounts/password_reset_done.html"
            }, name='password_reset_done'),
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {
                "template_name": "accounts/password_reset_confirm.html"
            }, name='password_reset_confirm'),
    url(r'^password_reset/complete/$', auth_views.password_reset_complete, {
                "template_name": "accounts/password_reset_complete.html"
            }, name='password_reset_complete'),
)