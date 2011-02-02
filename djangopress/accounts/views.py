
from django.shortcuts import Http404, render_to_response, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from djangopress.accounts.forms import UserForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def send_activate_email(request, user, resend=False):
    site = Site.objects.get_current()
    message_data = {
        "user": user,
        "profile": user.get_profile(),
        "site": site,
        "scheme": "https" if request.is_secure() else "http"
    }
    message = render_to_string('accounts/emails/confirm.txt', message_data)
    try:
        send_mail('%s : Activate Membership' % site.name, message,
                  'noreply@%s' % site.domain , [user.email])
    except BadHeaderError:
        return Http404('Invalid header found.')
    if resend:
        HttpResponseRedirect(reverse('accounts-activation-resent'))
    return HttpResponseRedirect(reverse('accounts-registered'))

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(True)
            user.is_active = False # set to true once they confirm email
            user.set_password(form.cleaned_data["password1"])
            user.save()
            profile = user.get_profile()
            profile.remember_between_visits = form.cleaned_data["remember_between_visits"]
            profile.timezone = form.cleaned_data["timezone"]
            client_address = request.META.get('HTTP_X_FORWARDED_FOR',
                    request.META.get("REMOTE_ADDR"))
            profile.registration_ip = client_address
            profile.last_ip_used = client_address
            profile.save()
            return send_activate_email(request, user)
    else:
        form = UserForm()
    data = {
        "form": form
    }
    return render_to_response("accounts/register.html" , data,
            context_instance=RequestContext(request))

def activate(request, user, activate_key):
    user = get_object_or_404(User, username=user)
    profile = user.get_profile()
    if user.is_active:
        return HttpResponseRedirect(reverse('accounts-already-activated'))
    if profile.check_activate_key(activate_key):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('accounts-activated'))
    else:
        return HttpResponseRedirect(reverse('accounts-activation-invalid', kwargs={'user': user}))

def reactivate(request, user):
    """Resend the users activation email"""
    if request.method == 'POST':
        user = get_object_or_404(User, username=user)
        if not user.is_active:
            profile = user.get_profile()
            profile.set_activate_key()
            profile.save()
            return send_activate_email(request, user, resend=True)
    raise Http404("Invalid request")

def user_list(request):
    user_list = User.objects.all()

    paginator = Paginator(user_list, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)

    data = {
        "users": users,
        "page_title": "User List",
    }
    return render_to_response("accounts/user-list.html" , data,
            context_instance=RequestContext(request))
def user_profile(request, username, tab=None):
    pass