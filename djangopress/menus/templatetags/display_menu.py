from django import template
register = template.Library()
from djangopress.menus.models import Menu, MenuItem

class MenuDisplayNode(template.Node):
    def __init__(self, menu, template=None):
        self._menu = menu
        self._template = template if template else "menu.html"

    def _tags(self, path, item, active_len):
        link = item.link.get_location()
        if path is None or link is None:
            return set(item.tag.split()), None
        tags = set(item.tag.split())
        active = None
        if link == path:
            tags.add("current")
        if path.startswith(link) and (active_len is None or len(link) < active_len):
            tags.add("active")
            active = len(link)
        return tags, active

    def _sort_tags(self, context, items):
        path = context.get("request").path if context.get("request") else None
        tags = []
        active_len = None
        active = None
        for item in items:
            item_tags, active_len = self._tags(path, item, active_len)
            if active_len:
                if active:
                    active.discard("active")
                active = item_tags
            tags.append(item_tags)
        return tags

    def render(self, context, menu=None):
        t = template.loader.get_template(self._template)
        if menu is None:
            menu = Menu.objects.get(name=self._menu)
        items = MenuItem.objects.filter(parent_menu=menu)
        tags = self._sort_tags(context, items)
        menu_items = [(item, self.render(context, Menu.objects.filter(parent_item=item)), tag) for item, tag in zip(items, tags)]
        menu_items.sort()
        data = {
            'menu': menu,
            'menu_items': menu_items,
        }
        return t.render(template.Context(data, autoescape=context.autoescape))


def do_menu_display(parser, token):
    args = token.split_contents()
    if len(args) == 2:
        return MenuDisplayNode(args[1])
    elif len(args) == 3:
        return MenuDisplayNode(args[1], args[2][1:-1])
    else:
        raise template.TemplateSyntaxError, "%s expects 1 or 2 arguments" % args[0]

register.tag('display_menu', do_menu_display)
