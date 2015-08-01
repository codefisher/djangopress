from django.contrib import admin
from djangopress.menus.models import Menu, MenuItem

class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Menu, MenuAdmin)
    
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'link', 'menu', 'parent', 'index']
    list_editable = ('index', )
    ordering = ('menu', 'parent', 'index')

admin.site.register(MenuItem, MenuItemAdmin)
    