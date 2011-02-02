from django.contrib import admin
from djangopress.menus.models import Menu, MenuItem

class MenuAdmin(admin.ModelAdmin):
    pass
admin.site.register(Menu, MenuAdmin)

class MenuItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(MenuItem, MenuItemAdmin)