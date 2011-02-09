from django.contrib import admin
from djangopress.pages.models import Page
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
            'fields': ('slug', 'title', 'template', 'sites')
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
            'fields': ('override_location', 'parent')
        }),
        ('SEO options', {
            'classes': ('collapse',),
            'fields': ('meta_page_title', 'meta_keywords', 'meta_description')
        }),
    )


admin.site.register(Page, PageAdmin)
admin.site.register(TextBlock)