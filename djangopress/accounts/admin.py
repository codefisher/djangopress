from django.contrib import admin
from djangopress.accounts.models import UserProfile, UserProperty
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.admin.util import model_ngettext
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.forms import Textarea
from django.db import models

class PropertiesInline(admin.TabularInline):
    model = UserProperty
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':3})},
    }

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False
    
class UserAdmin(AuthUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')
    actions=['ban_user']

    def ban_user(self, request, queryset):
        n = queryset.count()
        for obj in queryset:
            profile = obj.profile
            profile.banned = True
            profile.save()            
        self.message_user(request, _("Successfully banned %(count)d %(items)s.") % {
                "count": n, "items": model_ngettext(self.opts, n)
            }, messages.SUCCESS)
    ban_user.short_description = "Ban Users"
    
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)
    
    def change_view(self, *args, **kwargs):
        self.inlines = [UserProfileInline, PropertiesInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)