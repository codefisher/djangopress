from django.conf.urls import patterns, url, include
from django.conf import settings
from djangopress.sitemap import sitemap_patterns
from django.core.exceptions import ImproperlyConfigured

# django databrowse application
#from django.contrib import databrowse
#from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # the blog system
    (r'^(?:(?P<blog>[\w\-]+)/)?news/', include('djangopress.blog.urls')),
    
    # the forum system
    (r'^(?:(?P<forums>[\w\-]+)/)?forum/', include('djangopress.forum.urls')),
    
    # the user accounts system
    (r'^accounts/', include('djangopress.accounts.urls')),

    # the cms pages editing tools etc/
    (r'^pages/', include('djangopress.pages.urls')),

    (r'^download/', include('codefisher_apps.downloads.urls')),
    (r'^paypal/', include('paypal.standard.ipn.urls')),
    (r'^donate/', include('djangopress.donate.urls')),
    (r'^email/', include('djangopress.contact.urls')),
    (r'^xslt_svn/', include('codefisher_apps.svn_xslt.urls')),
)
""" needs to be updated for 1.6 
urlpatterns += patterns('django.views.generic.simple',
    # we don't like the default location for the user page
    ('^user/(?P<username>.+)/$', 'redirect_to', {'url': '/accounts/users/%(username)s/'}),
)
"""
try:
    try:
        import haystack
    except ImproperlyConfigured:
        pass
except ImportError:
    pass
else:
    from haystack.views import SearchView, search_view_factory
    from haystack.forms import SearchForm

    class SiteSearchView(SearchView):
        def __name__(self):
            return "SiteSearchView"

        def extra_context(self):
            extra = super(SiteSearchView, self).extra_context()
            extra["query_args"] = {"q": self.get_query()}
            return extra
    urlpatterns += patterns('',
        # the haystack search
        url(r'^search/', search_view_factory(
                view_class=SiteSearchView,
                template='search/search.html',
                form_class=SearchForm,
                results_per_page=10,
            ), name='haystack_search'),
    )

urlpatterns += sitemap_patterns

from local_urls import urlpatterns as locale_urls
urlpatterns += locale_urls


# if debug is enabled use the static server for media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
            (r'^admin/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/usr/share/pyshared/django/contrib/admin/static/admin/'}),
    )
