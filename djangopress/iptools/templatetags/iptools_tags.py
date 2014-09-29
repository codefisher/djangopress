from django import template
from djangopress.iptools.views import get_ip_country_flag
register = template.Library()

@register.simple_tag
def ip_country_flag(ip_address):
    if not ip_address:
        return ''
    flag = get_ip_country_flag(ip_address)
    if flag: 
        return '<img src="%s" />' % flag
    return ''