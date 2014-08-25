from django.contrib import admin
from djangopress.blog.models import Category, Entry, Tag, Blog, Comment, Flag

class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'posted']
admin.site.register(Entry, EntryAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)

class FlagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Flag, FlagAdmin)