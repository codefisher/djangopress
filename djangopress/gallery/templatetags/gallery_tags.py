from django import template
from django.utils.safestring import mark_safe
from ..models import GALLERY_SETTINGS

register = template.Library()

@register.simple_tag(takes_context=True)
def gallery_as_html(context, gallery):
    return mark_safe(gallery.as_html(thumber=context.get('thumber')))

@register.simple_tag(takes_context=True)
def gallery_thumbnail(context, image):
    thumber = context.get('thumber')
    sizes = GALLERY_SETTINGS.get("sizes").get("thumb")
    t = template.Template("""<img src="{{ thumbnail }}" width="{{ width }}" alt="{{ image.description|striptags }}" height="{{ height }}">""")
    if thumber:
        context.update({
            "width": thumber.width,
            "height": thumber.height,
            "thumbnail": thumber.thumb(image),
            "image": image
        })
    else:
        context.update({
            "width": sizes.get('width'),
            "height": sizes.get('height'),
            "thumbnail": image.thumbnail,
            "image": image
        })
    return mark_safe(t.render(context).strip())