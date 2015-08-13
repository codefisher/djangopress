from django.contrib import admin
from django.contrib.sites.models import Site
from django import forms
from djangopress.pages.models import Page, PageTemplate, PageBlock

try:
    from tinymce import widgets as tinymce_widgets
except ImportError:
    tinymce_widgets = None

class BlockAdminForm(forms.ModelForm):
    class Meta:
        model = PageBlock
        if tinymce_widgets:
            widgets = {
                'data': tinymce_widgets.AdminTinyMCE,
            }
        exclude = ()


class BlockInline(admin.StackedInline):
    model = PageBlock
    form = BlockAdminForm
    extra = 0
    min_num = 1
    fieldsets = (
            (None, {
                'fields': ('data',)
            }),
            ('Advanced Options', {
                'classes': ('collapse',),
                'fields': ('block_name', 'position', 'block_id', 'render')
            }),
    )

class PageAdmin(admin.ModelAdmin):

    prepopulated_fields = {
        "slug": ("title", )
    }

    inlines = [BlockInline]
    list_display = ('title', 'page_location', 'posted', 'status', 'visibility')
    list_filter = ('status', 'visibility')
    readonly_fields = ('author', 'posted', 'edited_by', 'edited')
    
    def page_location(self, obj):
        link = obj.get_absolute_url()
        return '<a href="%s">%s</a>' % (link, link)
    page_location.allow_tags = True

    def save_model(self, request, obj, form, change):
        obj.edited_by = request.user
        if not hasattr(obj, 'author'):
            obj.author = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(PageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['sites'].initial = [Site.objects.get_current()]
        return form

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'parent')
        }),
        ('Display Settings', {
            'fields': ('status', 'visibility', 'login_required')
        }),
        ('Authors', {
            'fields': ('author', 'posted', 'edited_by', 'edited')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('template', 'sites', 'override_location', 'head_tags', 'image')
        }),
        ('SEO options', {
            'classes': ('collapse',),
            'fields': ('meta_page_title', 'meta_keywords', 'meta_description')
        }),
    )

class PageBlockAdmin(admin.ModelAdmin):
    form = BlockAdminForm

    fieldsets = (
        (None, {
            'fields': ('data',)
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('block_name', 'position', 'block_id', 'render')
        }),
    )

    list_display = ('block_name', 'position', 'block_id', 'render', 'page', 'page_url')
    
    def page_url(self, obj):
        try:
            return obj.page.get_absolute_url()
        except:
            return ''
    
class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template')
    
admin.site.register(PageTemplate, PageTemplateAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageBlock, PageBlockAdmin)