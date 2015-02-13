from django.contrib import admin
from djangopress.blog.models import Category, Entry, Tag, Blog, Comment, Flag

class BlogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class EntryAdmin(admin.ModelAdmin):
    exclude = ('author',)
    
    list_display = ['title', 'slug', 'author', 'posted']
    
    prepopulated_fields = {
        "slug": ("title", )
    }
    
    fieldsets = (
        (None, {
            'fields': ('blog', 'title', 'slug', 'body')
        }),
        ('Publishing', {
            'fields': ('posted', 'status', 'visibility')
        }),
        ('Settings', {
            'fields': ('sticky', 'comments_open')
        }),
        ('Tagging', {
            'fields': ('tags', 'categories')
        }),
        ('Meta', {
            'fields': ('description', 'post_image')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
admin.site.register(Entry, EntryAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'submit_date', 'is_public', 'is_spam')
admin.site.register(Comment, CommentAdmin)

class FlagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Flag, FlagAdmin)