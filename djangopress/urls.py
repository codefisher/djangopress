from django.conf.urls.defaults import *
from django.conf import settings
from djangopress.sitemap import sitemap_patterns

# django databrowse application
#from django.contrib import databrowse
#from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm

class SiteSearchView(SearchView):
    def __name__(self):
        return "SiteSearchView"

    def extra_context(self):
        extra = super(SiteSearchView, self).extra_context()
        extra["query_args"] = {"q": self.get_query()}
        return extra

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # the django comment app
    (r'^comments/', include('django.contrib.comments.urls')),
    # the django databrowse app
    #(r'^databrowse/(.*)', login_required(databrowse.site.root)),


    # the Toolbar Buttons section of the site (custom maker etc.)
    #(r'^toolbar_buttons/',        include('toolbar_buttons.toolbar_buttons_web.tbutton_maker.urls')),

    # the blog system
    (r'^(?:(?P<blog>[\w\-]+)/)?news/', include('djangopress.blog.urls')),

    # the user accounts system
    (r'^accounts/', include('djangopress.accounts.urls')),
)

urlpatterns += patterns('django.views.generic.simple',
    # we don't like the default location for the user page
    ('^user/(?P<username>.+)/$', 'redirect_to', {'url': '/accounts/users/%(username)s/'}),
)

try:
    #import haystack # if this failes, don't configure haystack urls
    urlpatterns += patterns('',
        # the haystack search
        url(r'^search/', search_view_factory(
                view_class=SiteSearchView,
                template='search/search.html',
                form_class=SearchForm,
                results_per_page=10,
            ), name='haystack_search'),
    )
except ImportError:
    pass


urlpatterns += sitemap_patterns

# if debug is enabled use the static server for media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )