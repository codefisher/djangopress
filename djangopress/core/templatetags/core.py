import unicodedata
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.template import Library

register = Library()


def truncate_chars(s, num, end_text='...'):
    """Truncates a string after a certain number of characters. Takes an
    optional argument of what should be used to notify that the string has been
    truncated, defaulting to ellipsis (...)"""
    s = force_unicode(s)
    length = int(num)

    normalized = unicodedata.normalize('NFC', s)

    # If the text is short enough, we can bail out right now
    if len(normalized) <= length:
        return normalized

    translated_end_text = end_text#_(end_text)
    len_end_text = len(translated_end_text)

    end_index = max(length-len_end_text, 0)
    while unicodedata.combining(normalized[end_index]) and end_index < len(normalized):
        end_index += 1

    return u'%s%s' % (normalized[:end_index], translated_end_text)
truncate_chars = allow_lazy(truncate_chars, unicode)

def truncatechars(value, arg):
    """
    Truncates a string after a certain number of characters.

    Argument: Number of characters to truncate after.
    """
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return truncate_chars(value, length)
truncatechars.is_safe = True
truncatechars = stringfilter(truncatechars)

register.filter(truncatechars)
