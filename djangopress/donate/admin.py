from django.contrib import admin
from djangopress.donate.models import Donations

class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'amount', 'validated')
admin.site.register(Donations, DonationAdmin)