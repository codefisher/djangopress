
from djangopress import settings
from django.contrib.auth.models import Group


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR')

def has_permission(request, app, name):
    if request.user.is_authenticated():
        return request.user.has_perm('%s.%s' % (app, name))
    else:
        group = Group.objects.get(name=settings.ANONYMOUS_USER_GROUP)
        return bool(group.permissions.filter(codename=name))

def choose_form(request, authenticated, anonymous, *args, **kargs):
    if request.user.is_authenticated():
        return authenticated(*args, **kargs)
    return anonymous(*args, **kargs)

def smart_truncate_chars(value, max_length):
    max_length = int(max_length)
    if len(value) > max_length:
        # limits the number of characters in value to max_length (blunt cut)
        truncd_val = value[:max_length]
        # check if the next upcoming character after the limit is not a space,
        # in which case it might be a word continuing
        if value[max_length] != ' ':
            # rfind will return the last index where matching the searched character,
            # in this case we are looking for the last space
            # then we only return the number of character up to that last space
            truncd_val = truncd_val[:truncd_val.rfind(' ')]
        return truncd_val + '...'
    return value