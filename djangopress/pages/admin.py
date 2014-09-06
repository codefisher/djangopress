from django.contrib import admin
from djangopress.pages.models import Page, PageTemplate
from djangopress.pages.blocks import TextBlock

class PageAdmin(admin.ModelAdmin):

    list_display = ('title', 'location', 'posted', 'status', 'visibility')
    list_filter = ('location', 'status', 'visibility')
    readonly_fields = ('author', 'posted', 'edited_by', 'edited')

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
        ('Content', {
            'fields': ('blocks',)
        }),
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

class TextBlockAdmin(admin.ModelAdmin):

    list_display = ('block_name', 'position', 'block_id')
    
class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template')
    
admin.site.register(PageTemplate, PageTemplateAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(TextBlock, TextBlockAdmin)