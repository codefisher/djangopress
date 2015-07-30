from djangopress.menus.menu import register
from django.template import Template, RequestContext

class ListRender(object):
    _menu = Template("""
        {% load display_menu %}
        <ul{% if menu.class_tag%} class="{{ menu.class_tag }}"{% endif %}{% if menu.name %} id="{{ menu.name }}"{% endif %}>
            {% for item, sub_menu in tree %}
                {% display_menu_item item sub_menu %}
            {% endfor %}
        </ul>""")
    _item = Template("""
            {% load display_menu %}
            <li {% if item.id_tag %} id="{{ item.id_tag }}" {% endif %}{% if item.class_tag %} class="{{ item.class_tag }}"{% endif %}>
                <a href="{{ item.link }}">{{ item.label }}</a>
                {% if sub_menu %}
                    {% display_submenu item sub_menu %}
                {% endif %}
            </li>""")
        
    def _tag_active_item(self, context, tree):
        if not context.get("request"):
            return # happes on 500 pages, maybe others
        path = context.get("request").path
        try:
            active_item = max([item for item in tree if path.startswith(item[0].link)], key=lambda x: len(x[0].link))[0]
            active_item.class_tag = "active" if not active_item.class_tag else active_item.class_tag + " active"
        except:
            pass
        
    def render_menu(self, context, tree, menu=None, renderer=None):
        tree = sorted(((item, sub_menu) for item, sub_menu in tree.items()), key=lambda x: x[0].index)
        self._tag_active_item(context, tree)
        return self._menu.render(RequestContext(context.get("request"), {"menu": menu, "tree": tree, 'renderer': renderer}))
    
    def render_item(self, context, item, sub_menu):
        return self._item.render(RequestContext(context.get("request"), {"item": item, "sub_menu": sub_menu}))
    

register('default', ListRender())

class HeadingRender(ListRender):

    _menu = Template("""
        {% load display_menu %}
        <div{% if menu.class_tag%} class="{{ menu.class_tag }}"{% endif %}>
            {% for item, sub_menu in tree %}
                {% display_menu_item item sub_menu renderer %}
            {% endfor %}
        </div>""")
    _item = Template("""
            {% load display_menu %}
            <div class="heading-menu">
            <h2 {% if item.id_tag %} id="{{ item.id_tag }}" {% endif %}{% if item.class_tag %} class="{{ item.class_tag }}"{% endif %}>
                <a href="{{ item.link }}">{{ item.label }}</a></h2>
                {% if sub_menu %}
                    {% display_submenu item sub_menu %}
                {% endif %}
                </div>
            """)

register('headings', HeadingRender())