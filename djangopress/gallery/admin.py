from .models import GallerySection, Image
from django.contrib import admin


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('text_title', 'position')
    list_editable = ('position', )
    ordering = ('position', 'title')


admin.site.register(GallerySection, GalleryAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'image', 'gallery', 'description')

    def thumb(self, obj):
        return '<img src="{}">'.format(obj.thumbnail.url)
    thumb.allow_tags = True


admin.site.register(Image, ImageAdmin)
