from django.contrib import admin
from djangopress.menus.models import Menu, MenuItem

class MenuAdmin(admin.ModelAdmin):
    pass
admin.site.register(Menu, MenuAdmin)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('link_label', 'link_location', 'tag', 'parent')

    def link_label(self, menuitem):
        return str(menuitem.link.label())

    def link_location(self, menuitem):
        return str(menuitem.link.get_absolute_url())

    def parent(self, menuitem):
        return menuitem.parent_menu.name

admin.site.register(MenuItem, MenuItemAdmin)