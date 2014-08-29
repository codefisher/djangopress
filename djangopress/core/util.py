
from djangopress import settings
from django.contrib.auth.models import Group


try:
    from recaptcha.client import captcha
except:
    pass


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    return request.META.get('REMOTE_ADDR')

def get_recaptcha_html():
    try:
        return captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)
    except:
        return ""
    
def recaptcha_is_valid(request):
    try:
        response = captcha.submit(
                request.POST.get('recaptcha_challenge_field'),
                request.POST.get('recaptcha_response_field'),
                settings.RECAPTCHA_PRIVATE_KEY,
                get_client_ip(request),
            )
        if response.is_valid:
            return True
        return False
    except:
        return True #they don't have the recapacha installed so let it be valid
    
def has_permission(request, app, name):
    if request.user.is_authenticated():
        return request.user.has_perm('%s.%s' % (app, name))
    else:
        group = Group.objects.get(name=settings.ANONYMOUS_USER_GROUP)
        return bool(group.permissions.filter(codename=name))
