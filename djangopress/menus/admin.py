from django.contrib import admin
from djangopress.menus.models import Menu, MenuItem

class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Menu, MenuAdmin)
    
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'link', 'menu', 'index', 'parent']
admin.site.register(MenuItem, MenuItemAdmin)
    