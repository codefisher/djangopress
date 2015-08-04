from django.contrib import admin
from djangopress.blog.models import Category, Entry, Tag, Blog, Comment, Flag
from django import forms

try:
    from tinymce import widgets as tinymce_widgets
except ImportError:
    tinymce_widgets = None

class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        if tinymce_widgets:
            widgets = {
                'tagline': tinymce_widgets.AdminTinyMCE,
            }
        exclude = ()

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = Entry
        if tinymce_widgets:
            widgets = {
                'body': tinymce_widgets.AdminTinyMCE,
            }
        exclude = ('author',)

class EntryAdmin(admin.ModelAdmin):
    form = EntryAdminForm
    exclude = ('author',)
    
    list_display = ('title', 'slug', 'author', 'posted')
    
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