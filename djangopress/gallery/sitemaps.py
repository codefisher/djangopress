from django.contrib.sitemaps import Sitemap
from .models import GallerySection
from djangopress.core.sitemap import register

class GallerySitemap(Sitemap):
    lastmod = None
 
    def items(self):
        return GallerySection.objects.all()

register('gallery-section', GallerySitemap)