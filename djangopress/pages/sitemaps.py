from django.contrib.sitemaps import Sitemap
from djangopress.pages.models import Page
from djangopress.core.sitemap import register
from django.conf import settings

class PageSitemap(Sitemap):

    def items(self):
        return Page.objects.filter(sites__id__exact=settings.SITE_ID,
                visibility="VI", status="PB")

    def lastmod(self, obj):
        return obj.edited

register('page', PageSitemap)