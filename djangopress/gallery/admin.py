from .models import GallerySection, Image
from django.contrib import admin
from django import forms

try:
    from tinymce import widgets as tinymce_widgets
except ImportError:
    tinymce_widgets = None

class GalleryAdminForm(forms.ModelForm):
    class Meta:
        model = GallerySection
        if tinymce_widgets:
            widgets = {
                'description': tinymce_widgets.AdminTinyMCE,
            }
        exclude = ()

class GalleryAdmin(admin.ModelAdmin):
    form = GalleryAdminForm
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
