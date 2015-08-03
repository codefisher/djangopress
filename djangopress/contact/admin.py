from django.contrib import admin
from .models import MailAddress

class MailAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

admin.site.register(MailAddress, MailAddressAdmin)