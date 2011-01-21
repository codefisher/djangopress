from django.contrib import admin
from djangopress.accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)