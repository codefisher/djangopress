from django import template
from django.utils.safestring import mark_safe
from djangopress.iptools.views import get_ip_country_flag
register = template.Library()

@register.simple_tag
def ip_country_flag(ip_address):
    if not ip_address:
        return ''
    flag, iso_code = get_ip_country_flag(ip_address)
    if flag: 
        return mark_safe('<img src="%s" alt="%s"/>' % (flag, iso_code))
    return ''