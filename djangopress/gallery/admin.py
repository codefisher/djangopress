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

class ImageAdminForm(forms.ModelForm):
    class Meta(object):
        model = Image
        widgets = {
            'description': forms.TextInput
        }
        exclude = ()

class ImageInline(admin.StackedInline):
    model = Image
    form = ImageAdminForm
    extra = 0
    min_num = 1

class GalleryAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

    prepopulated_fields = {
        "slug": ("title", )
    }

    form = GalleryAdminForm
    list_display = ('text_title', 'position')
    list_editable = ('position', )
    ordering = ('position', 'title')

    def save_related(self, request, form, formsets, change):
        super(GalleryAdmin, self).save_related(request, form, formsets, change)
        for formset in formsets:
            for image in formset.queryset.all():
                if not image.thumbnail.file or change:
                    image.save()

admin.site.register(GallerySection, GalleryAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'image', 'gallery', 'description')
    list_filter = ('gallery',)

    def thumb(self, obj):
        if obj.thumbnail:
            return '<img src="{}">'.format(obj.thumbnail.url)
        return obj.image
    thumb.allow_tags = True


admin.site.register(Image, ImageAdmin)
