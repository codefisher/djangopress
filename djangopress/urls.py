from django.conf.urls import patterns, url, include
from djangopress.forum import urls as forum_urls
from djangopress.accounts import urls as accounts_urls
from djangopress.blog import urls as blog_urls
from djangopress.pages import urls as pages_urls
from paypal.standard.ipn import urls as paypal_urls
from djangopress.donate import urls as donate_urls
from djangopress.contact import urls as contact_urls
from djangopress.menus import urls as menu_urls
from djangopress.iptools import urls as iptools_urls

# django databrowse application
#from django.contrib import databrowse
#from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # the blog system
    (r'^(?P<blog_slug>[\w\-]+)/blog/', include(blog_urls)),
    (r'^news/', include(blog_urls), {"blog_slug": "news"}),
    
    # the forum system
    (r'^(?P<forums_slug>[\w\-]+)/forum/', include(forum_urls)),
    (r'^forum/', include(forum_urls), {"forums_slug": "codefisher"}),
    
    # the user accounts system
    (r'^accounts/', include(accounts_urls)),

    # the cms pages editing tools etc/
    (r'^pages/', include(pages_urls)),

    (r'^paypal/', include(paypal_urls)),
    (r'^donate/', include(donate_urls)),
    (r'^email/', include(contact_urls)),
    (r'^iptools/', include(iptools_urls)),
)

try:
    from djangopress.core.search import ModelSetSearchForm, ModelSetSearchView, search_view_factory

    urlpatterns += patterns('',
        # the haystack search
        url(r'^search/', search_view_factory(
                view_class=ModelSetSearchView,
                form_class=ModelSetSearchForm,
                results_per_page=10,
                models=["pages.page", "blog.entry"],
            ), name='haystack-search'),
    )
except ImportError:
    pass

from djangopress.sitemap import sitemap_patterns
urlpatterns += sitemap_patterns

from local_urls import urlpatterns as locale_urls
urlpatterns += locale_urls

from codefisher_apps.downloads.urls import urlpatterns as download_urls
urlpatterns += download_urls

from djangopress.core.format.models import autodiscover as format_autodiscover
format_autodiscover()