from djangopress.menus.menu import register
from django.template import Template, RequestContext
from .models import GallerySection

class GalleryRender(object):
    _item = Template("""
            {% load display_menu %}
            <li {% if item.id_tag %} id="{{ item.id_tag }}" {% endif %}{% if item.class_tag %} class="{{ item.class_tag }}"{% endif %}>
                <a href="{{ item.link }}">{{ item.label }}</a>
                <ul>
                    <li><a href="{{ item.link }}">{{ item.label }}</a></li>
                    {% for gallery in galleries %}
                        <li><a href="{{  gallery.get_absolute_url }}">{{ gallery.title }}</a></li>
                    {% endfor %}
                </ul>
            </li>""")
        
    def render_menu(self, context, tree, menu=None, renderer=None):
        return ''
    
    def render_item(self, context, item, sub_menu):
        galleries = GallerySection.objects.filter(
            listed=True).order_by("position")
        return self._item.render(RequestContext(context.get("request"), {"item": item, "galleries": galleries}))

    

register('gallery', GalleryRender())