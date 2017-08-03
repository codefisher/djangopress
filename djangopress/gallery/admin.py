from .models import GallerySection, Image, GALLERY_SETTINGS, Thumber
from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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

class ThumbnailForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    sizes = GALLERY_SETTINGS.get("sizes").get("thumb")
    width = forms.IntegerField(initial=sizes.get('width'))
    height = forms.IntegerField(initial=sizes.get('height'))

class GalleryAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

    prepopulated_fields = {
        "slug": ("title", )
    }

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description')
        }),
        ("options", {
            'fields': ('position', 'listed')
        }),
    )

    actions = ['as_html']

    form = GalleryAdminForm
    list_display = ('text_title', 'position')
    list_editable = ('position', )
    ordering = ('position', 'title')

    def as_html(self, request, queryset):
        form = None
        thumber = None
        if 'apply' in request.POST:
            form = ThumbnailForm(request.POST)
            if form.is_valid():
                thumber = Thumber(form.cleaned_data['width'], form.cleaned_data['height'])
        if not form:
            form = ThumbnailForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'gallery/admin_gallery_as_html.html', {
            'title': "Gallery as HTML",
            'gallery_form': form,
            'thumber': thumber,
            'galleries': queryset,
            'location': request.get_full_path,
        })

admin.site.register(GallerySection, GalleryAdmin)

class MoveGalleryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    gallery = forms.ModelChoiceField(GallerySection.objects, required=False)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'image', 'gallery', 'description')
    list_filter = ('gallery',)

    actions = ['change_gallery', 'as_html']

    def change_gallery(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = MoveGalleryForm(request.POST)

            if form.is_valid():
                gallery = form.cleaned_data['gallery']
                queryset.update(gallery=gallery)
                if gallery:
                    self.message_user(request, "Moved images to gallery: {}.".format(gallery.title))
                else:
                    self.message_user(request, "Removed images from gallery.")
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = MoveGalleryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'gallery/admin_change_gallery.html', {
            'title': 'Change Image Gallery',
            'images': queryset,
            'gallery_form': form,
        })

    def as_html(self, request, queryset):
        form = None
        thumber = None
        if 'apply' in request.POST:
            form = ThumbnailForm(request.POST)
            if form.is_valid():
                thumber = Thumber(form.cleaned_data['width'], form.cleaned_data['height'])
        if not form:
            form = ThumbnailForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request, 'gallery/admin_images_as_html.html', {
            'title': "Images as HTML",
            'gallery_form': form,
            'thumber': thumber,
            'images': queryset,
            'location': request.get_full_path,
        })

    def thumb(self, obj):
        if obj.thumbnail:
            return '<img src="{}">'.format(obj.thumbnail)
        return obj.image
    thumb.allow_tags = True


admin.site.register(Image, ImageAdmin)
