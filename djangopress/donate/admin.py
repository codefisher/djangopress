from django.contrib import admin
from djangopress.donate.models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'amount', 'validated')
admin.site.register(Donation, DonationAdmin)