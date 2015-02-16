from django import template
from djangopress.theme.models import ThemeLibrary
register = template.Library()

@register.simple_tag()
def theme_folder():
    return ThemeLibrary.get_active().slug