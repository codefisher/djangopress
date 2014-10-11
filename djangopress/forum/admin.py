from django.contrib import admin
from djangopress.forum.models import Forum, ForumCategory, ForumGroup, ForumUser, Attachment, Post, Rank, Report, Thread, ForumProperty
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.admin.utils import get_deleted_objects, model_ngettext
from django.db import router
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.contrib.admin.actions import delete_selected as delete_selected_
from django.contrib.admin import SimpleListFilter
from django.template.defaultfilters import truncatechars
from django.forms import Textarea
from django.db import models

class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_threads', 'num_posts', 'category' , 'parent_forum')
    raw_id_fields = ("last_post", "subscriptions")
admin.site.register(Forum, ForumAdmin)

class ForumCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'forums')
admin.site.register(ForumCategory, ForumCategoriesAdmin)

class PropertiesInline(admin.TabularInline):
    model = ForumProperty
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3})},
    }
    
class ForumGroupAdmin(admin.ModelAdmin):
    inlines = [PropertiesInline]
    list_display = ('name', 'slug', 'tagline')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'tagline', 'sites')
        }),
        ('Settings', {
            'classes': ('collapse',),
            'fields': ('format', 'show_announcement', 'announcement', 'number_of_threads',
                       'number_of_posts', 'show_smilies', 'display_images', 'make_links', 
                       'show_avatars', 'show_signature', 'show_quick_post')
        }),    
    )
admin.site.register(ForumGroup, ForumGroupAdmin)

class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__username', )
admin.site.register(ForumUser, ForumUserAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attachment, AttachmentAdmin)

def post_delete_selected(modeladmin, request, queryset):
    # this is using code copied from the django.contrib.admin.actions
    opts = modeladmin.model._meta
    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    deletable_objects, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)
    
    if not request.POST.get('post'):
        # this will cause the confirmation page to show
        return delete_selected_(modeladmin, request, queryset)
    else:
        # now we jump in an do this our own way
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = force_text(obj)
                modeladmin.log_deletion(request, obj, obj_display)
                obj.delete()
            modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            }, messages.SUCCESS)
        # Return None to display the change list page again.
        return None

class PostAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'thread_subject', 'posted', 'is_spam', 'is_public', 'is_removed')
    list_filter = ('is_spam', 'is_public', 'is_removed')
    search_fields = ('thread__subject', 'poster_name', 'author__username')
    
    actions=['mark_as_spam']
    
    def thread_subject(self, obj):
        return truncatechars(obj.thread.subject, 60)
    
    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        # we do this, because we want to preserve the name "delete_selected"
        # but want to change the action, and we can't name our function
        # delete_selected, because we have two of them in this file
        delete_selected = list(actions.get("delete_selected", []))
        if delete_selected:
            delete_selected[0] = post_delete_selected
            actions["delete_selected"] = tuple(delete_selected)
        return actions
    
    def mark_as_spam(self, request, queryset):
        n = queryset.count()
        for obj in queryset:
            obj.is_spam = True
            obj.save()            
        self.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, messages.SUCCESS)
    mark_as_spam.short_description = "Mark selected as spam"
    
    
admin.site.register(Post, PostAdmin)

class RankAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rank, RankAdmin)

class ReportsAdmin(admin.ModelAdmin):
    list_display = ('post', 'reported_by', 'created_date', 'moderated', 'post_link')
    raw_id_fields = ('post', 'reported_by', 'moderated_by')
    
    def post_link(self, obj):
        return '<a href="%s">View Post</a>' % obj.post.get_absolute_url()
    post_link.allow_tags = True
    
admin.site.register(Report, ReportsAdmin)

def thread_delete_selected(modeladmin, request, queryset):
    # this is using code copied from the django.contrib.admin.actions
    opts = modeladmin.model._meta
    # Check that the user has delete permission for the actual model
    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied

    using = router.db_for_write(modeladmin.model)

    deletable_objects, perms_needed, protected = get_deleted_objects(
        queryset, opts, request.user, modeladmin.admin_site, using)
    
    if not request.POST.get('post'):
        # this will cause the confirmation page to show
        return delete_selected_(modeladmin, request, queryset)
    else:
        # now we jump in an do this our own way
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = force_text(obj)
                modeladmin.log_deletion(request, obj, obj_display)
                for post in Post.objects.filter(thread=obj):
                    post.delete()
                obj.delete()
            modeladmin.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(modeladmin.opts, n)
            }, messages.SUCCESS)
        # Return None to display the change list page again.
        return None
    

class HasPostsListFilter(SimpleListFilter):
    title = 'has posts'
    parameter_name = 'post'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )
        
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(first_post=None, last_post=None)
        if self.value() == 'no':
            return queryset.filter(first_post=None, last_post=None)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('subject', 'num_posts', 'author_name', 'closed', 'sticky')
    raw_id_fields = ("last_post", 'first_post', 'poster', "subscriptions", 'moved_to')
    list_filter = ('closed', 'sticky', HasPostsListFilter)

    actions=['open_threads', 'close_threads', 'sticky_threads', 'unsticky_threads']
    
    def open_threads(self, request, queryset):
        n = queryset.count()
        for obj in queryset:
            obj.closed = False
            obj.save()            
        self.message_user(request, _("Successfully opened %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, messages.SUCCESS)

    def close_threads(self, request, queryset):
        n = queryset.count()
        for obj in queryset:
            obj.closed = True
            obj.save()            
        self.message_user(request, _("Successfully closed %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, messages.SUCCESS)
        
    def sticky_threads(self, request, queryset):
        n = queryset.count()
        for obj in queryset:
            obj.sticky = True
            obj.save()            
        self.message_user(request, _("Successfully stickyed %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, messages.SUCCESS)
        
    def unsticky_threads(self, request, queryset):
        n = queryset.count()
        for obj in queryset:
            obj.sticky = False
            obj.save()            
        self.message_user(request, _("Successfully unstickyed %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, messages.SUCCESS)

    def get_actions(self, request):
        actions = super(ThreadAdmin, self).get_actions(request)
        # see PostAdmin
        delete_selected = list(actions.get("delete_selected", []))
        if delete_selected:
            delete_selected[0] = post_delete_selected
            actions["delete_selected"] = tuple(delete_selected)
        return actions

admin.site.register(Thread, ThreadAdmin)
