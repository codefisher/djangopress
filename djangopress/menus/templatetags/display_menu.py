from django import template
from djangopress.menus.menu import register as menu_register
from djangopress.menus.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def display_menu(context, menu_name):
    menu = Menu.objects.get(name=menu_name)
    menu_items = MenuItem.objects.filter(menu=menu).select_related('parent')
    nodes = dict((item, {}) for item in menu_items)
    for item in menu_items:
        if item.parent is not None:
            nodes[item.parent][item] = nodes[item]
    tree = dict((key, value) for key, value in nodes.items() if key.parent is None)
    try:
        return menu_register.get_renderer(menu.renderer).render_menu(context, tree, menu)
    except:
        return ""

@register.simple_tag(takes_context=True)
def display_menu_item(context, item, submenu):
    return menu_register.get_renderer(item.renderer).render_item(context, item, submenu)

@register.simple_tag(takes_context=True)
def display_submenu(context, item, submenu):
    return menu_register.get_renderer(item.renderer).render_menu(context, submenu) 