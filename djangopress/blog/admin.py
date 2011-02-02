from django.contrib import admin
from djangopress.blog.models import Category, Entry, Tag, Blog, EntryLink

class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class EntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Entry, EntryAdmin)

class EntryLinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(EntryLink, EntryLinkAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

