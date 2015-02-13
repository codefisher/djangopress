from django import template
from djangopress.core.util import smart_truncate_chars as _smart_truncate_chars
 
register = template.Library()
 
# truncate chars but leaving last word complete
@register.filter(name='smarttruncatechars')
def smart_truncate_chars(value, max_length):
    return _smart_truncate_chars(value, max_length)