from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # the Toolbar Buttons section of the site (custom maker etc.)
    (r'^toolbar_buttons/',        include('toolbar_buttons_web.tbutton_maker.urls')),

    # the blog system
    (r'^(?:(?P<slug>[\w\-]*)/)?/news/', include('djangopress.blog'))
)

# if debug is enabled use the static server for media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )