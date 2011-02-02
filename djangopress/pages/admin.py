from django.contrib import admin
from djangopress.pages.models import Page, HTMLBlock, TemplateBlock

class PageAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.edited_by = request.user
        if not hasattr(obj, 'author'):
            obj.author = request.user
        obj.save()

admin.site.register(Page, PageAdmin)

class HTMLBlockAdmin(admin.ModelAdmin):
    pass

admin.site.register(HTMLBlock, HTMLBlockAdmin)

class TemplateBlockAdmin(admin.ModelAdmin):
    pass

admin.site.register(TemplateBlock, TemplateBlockAdmin)
