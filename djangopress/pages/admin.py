from django.contrib import admin
from djangopress.pages.models import Page, PageTemplate, PageBlock
from django import forms

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

class PageAdmin(admin.ModelAdmin):

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

    fieldsets = (
        (None, {
            'fields': ('slug', 'title', 'template', 'sites', 'parent')
        }),
        ('Display Settings', {
            'fields': ('status', 'visibility', 'login_required')
        }),
        #('Content', {
        #    'fields': ('blocks',)
        #}),
        ('Authors', {
            'fields': ('author', 'posted', 'edited_by', 'edited')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': ('override_location', 'head_tags')
        }),
        ('SEO options', {
            'classes': ('collapse',),
            'fields': ('meta_page_title', 'meta_keywords', 'meta_description')
        }),
    )

class PageBlockAdmin(admin.ModelAdmin):
    form = BlockAdminForm

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