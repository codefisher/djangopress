
from django.shortcuts import Http404, render, get_object_or_404, HttpResponseRedirect
from djangopress.accounts.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from djangopress.accounts.profiles import register as profile_register
from djangopress import settings
from djangopress.core.util import get_client_ip

try:
    from recaptcha.client import captcha
except:
    pass

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
        return HttpResponseRedirect(reverse('accounts-activation-resent', kwargs={"user": user.username}))
    return HttpResponseRedirect(reverse('accounts-registered', kwargs={"user": user.username}))

def registered(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/registered-message.html" , {"user": user})

def activated(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/account_activated.html" , {"user": user})

def already_activated(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/already_activated.html" , {"user": user})

def invalid_activation(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/invalid_activation.html" , {"user": user})

def resent_activation(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/resent_activation.html" , {"user": user})

def register(request):
    if request.user.is_authenticated():
        # logged in users can't register
        return HttpResponseRedirect(reverse('accounts-profile'))
    data = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        recapatcha = recaptcha_is_valid(request)
        if form.is_valid() and recapatcha:
            user = form.save(True)
            user.is_active = False # set to true once they confirm email
            user.set_password(form.cleaned_data["password1"])
            user.save()
            profile = user.get_profile()
            #profile.remember_between_visits = form.cleaned_data["remember_between_visits"]
            profile.timezone = form.cleaned_data["timezone"]
            client_address = get_client_ip(request)
            profile.registration_ip = client_address
            profile.last_ip_used = client_address
            profile.save()
            return send_activate_email(request, user)
        if not recapatcha:
            data["recapatcha_error"] = "The verification failed, please try again."
    else:
        form = UserForm()
    data.update({
        "recapatch": get_recaptcha_html(),
        "form": form
    })
    return render(request, "accounts/register.html" , data)

def activate(request, username, activate_key):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    if user.is_active:
        return HttpResponseRedirect(reverse('accounts-already-activated', kwargs={"user": user.username}))
    if profile.check_activate_key(activate_key):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('accounts-activated', kwargs={'user': user.username}))
    else:
        return HttpResponseRedirect(reverse('accounts-activation-invalid', kwargs={'user': user.username}))

def reactivate(request, username):
    """Resend the users activation email"""
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
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
        "title": "User List",
    }
    return render(request, "accounts/user-list.html" , data)
    
def user_profile(request, username=None, tab=None):
    if username == None:
        if request.user.is_authenticated():
            user = request.user
        else:
            return redirect_to_login(next=reverse("accounts-profile"))
    else:
        user = get_object_or_404(User, username=username)
    profiles = profile_register.get_profiles()
    data = {
        "user": user,
        "title": "User Profile",
    }
    if request.user == user:
        # user is viewing their own profile, let them edit
        profile_data = []
        for _, cls in profiles.items():
            info = cls(user).edit(request)
            profile_data.append(info)
        data["profile_forms"] = [item for sublist in 
                [data.get("forms") for data in sorted(profile_data, key=lambda x: x.get("position", 0))] 
                    for item in sublist]
        return render(request, "accounts/edit-profile.html" , data)
    else:
        # some else's profile, show basic info
        profile_data = []
        for _, cls in profiles.items():
            info = cls(user).info()
            profile_data.append(info)
            data.update(info.get("data", {}))
        data["profile_data"] = sorted(profile_data, key=lambda x: x.get("position", 0))
        return render(request, "accounts/view-profile.html" , data)
    
def user_admin(request, username):
    pass