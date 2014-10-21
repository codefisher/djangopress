
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