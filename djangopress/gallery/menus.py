from djangopress.menus.menu import register
from django.template import Template, RequestContext
from .models import GallerySection

class GalleryRender(object):

    _menu = Template("""
            <ul{% if menu.class_tag%} class="{{ menu.class_tag }}"{% endif %}{% if menu.name %} id="{{ menu.name }}"{% endif %}>
                {% for gallery in galleries %}
                    <li><a href="{{  gallery.get_absolute_url }}">{{ gallery.title }}</a></li>
                {% endfor %}
            </ul>""")

    _item = Template("""
            <li {% if item.id_tag %} id="{{ item.id_tag }}" {% endif %}{% if item.class_tag %} class="{{ item.class_tag }}"{% endif %}>
                <a href="{{ item.link }}">{{ item.label }}</a>
                <ul>
                    {% if item and item.label %}<li><a href="{{ item.link }}">{{ item.label }}</a></li>{% endif %}
                    {% for gallery in galleries %}
                        <li><a href="{{  gallery.get_absolute_url }}">{{ gallery.title }}</a></li>
                    {% endfor %}
                </ul>
            </li>""")
        
    def render_menu(self, context, tree, menu=None, renderer=None):
        galleries = GallerySection.objects.filter(
            listed=True).order_by("position")
        return self._menu.render(RequestContext(context.get("request"), {"tree": tree, "galleries": galleries}))

    
    def render_item(self, context, item, sub_menu):
        galleries = GallerySection.objects.filter(
            listed=True).order_by("position")
        return self._item.render(RequestContext(context.get("request"), {"item": item, "galleries": galleries}))

    

register('gallery', GalleryRender())