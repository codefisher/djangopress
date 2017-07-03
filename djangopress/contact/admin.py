from django.contrib import admin
from .models import MailAddress, MailLog

class MailAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

admin.site.register(MailAddress, MailAddressAdmin)

class MailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email')

admin.site.register(MailLog, MailLogAdmin)