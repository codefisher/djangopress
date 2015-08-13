from django.contrib import admin
from djangopress.blog.models import Category, Entry, Tag, Blog, Comment, Flag
from django import forms
from django.utils.text import slugify

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

    prepopulated_fields = {
        "slug": ("name", )
    }

admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class CategoryInput(forms.TextInput):
    model = Category

    def _format_value(self, value):
        if type(value) == list:
            return ", ".join(self.model.objects.get(pk=val).name for val in value)
        return value

    def value_from_datadict(self, data, files, name):
        result = []
        blog = Blog.objects.get(pk=data.get('blog'))
        if data.get(name) is None:
            return None
        for name in data.get(name).split(','):
            name = name.strip()
            if not name:
                continue
            try:
                result.append(self.model.objects.get(name=name).pk)
            except:
                mod = self.model(name=name, slug=slugify(name), blog=blog)
                mod.save()
                result.append(mod.pk)
        return result

class TagInput(CategoryInput):
    model = Tag

class EntryAdminForm(forms.ModelForm):
    class Meta:
        model = Entry
        widgets = {
            'tags': TagInput,
            'categories': CategoryInput
        }
        if tinymce_widgets:
            widgets.update({
                'body': tinymce_widgets.AdminTinyMCE,
            })
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
            'classes': ('collapse',),
            'fields': ('sticky', 'comments_open')
        }),
        ('Tagging', {
            'classes': ('collapse',),
            'fields': ('tags', 'categories')
        }),
        ('Meta', {
            'classes': ('collapse',),
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