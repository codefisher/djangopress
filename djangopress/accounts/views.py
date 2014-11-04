
from django.shortcuts import Http404, render, get_object_or_404, redirect
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
from django.contrib.auth.signals import user_logged_in, user_login_failed


def user_login(sender, user, request, **kwargs):
    user.profile.last_ip_used = get_client_ip(request)
    user.profile.save()
    if request.POST.get('remember_me', None):
        request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
    else:
        request.session.set_expiry(0)
user_logged_in.connect(user_login)

def login_failed(sender, credentials):
    pass
user_login_failed.connect(login_failed)

def send_activate_email(request, user, resend=False):
    site = Site.objects.get_current()
    message_data = {
        "user": user,
        "profile": user.profile,
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
        return redirect(reverse('accounts-activation-resent', kwargs={"username": user.username}))
    return redirect(reverse('accounts-registered', kwargs={"username": user.username}))

def registered(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/registered-message.html" , {"user": user, "title": "Registered"})

def activated(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/account_activated.html" , {"user": user, "title": "Activated"})

def already_activated(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/already_activated.html" , {"user": user, "title": "Already Activated"})

def invalid_activation(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/invalid_activation.html" , {"user": user, "title": "Invalid Activation"})

def resent_activation(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "accounts/messages/resent_activation.html" , {"user": user, "title": "Resent Activation"})

def register(request):
    if request.user.is_authenticated():
        # logged in users can't register
        return redirect(reverse('accounts-profile'))
    data = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(True)
            user.is_active = False # set to true once they confirm email
            user.set_password(form.cleaned_data["password1"])
            user.save()
            profile = user.profile
            #profile.remember_between_visits = form.cleaned_data["remember_between_visits"]
            profile.timezone = form.cleaned_data["timezone"]
            client_address = get_client_ip(request)
            profile.registration_ip = client_address
            profile.last_ip_used = client_address
            profile.save()
            return send_activate_email(request, user)
    else:
        if 'djangopress.iptools' in settings.INSTALLED_APPS:
            from djangopress.iptools.views import get_request_time_zone
            tzname = get_request_time_zone(request)
            form = UserForm()
            form.fields['timezone'].initial = tzname
        else:
            form = UserForm()
    data.update({
        "form": form, 
        "title": "Register"
    })
    return render(request, "accounts/register.html" , data)

def activate(request, username, activate_key):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    if user.profile.banned:
        return redirect(reverse('accounts-banned', kwargs={"username": username.username}))
    if user.is_active:
        return redirect(reverse('accounts-already-activated', kwargs={"username": user.username}))
    if profile.check_activate_key(activate_key):
        user.is_active = True
        user.save()
        return redirect(reverse('accounts-activated', kwargs={'username': user.username}))
    else:
        return redirect(reverse('accounts-activation-invalid', kwargs={'username': user.username}))

def reactivate(request, username):
    """Resend the users activation email"""
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        if not user.is_active:
            if user.profile.banned:
                return redirect(reverse('accounts-banned', kwargs={"username": username.username}))
            else:
                profile = user.profile
                profile.set_activate_key()
                profile.save()
                return send_activate_email(request, user, resend=True)
    raise Http404("Invalid request")

def you_are_banned(request, username):
    user = get_object_or_404(User, username=username)
    if user.profile.banned:
        return render(request, "accounts/user-list.html" , {"user": user})
    else:
        raise Http404
    

class UserListPage(object):
    def get_absolute_url(self, page=1):
        return reverse('accounts-userlist', kwargs={"page": page})

def user_list(request, page=1):
    user_list = User.objects.filter(is_active=True)
    paginator = Paginator(user_list, 20)

    user_list_page = UserListPage()
    
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            return redirect(user_list_page.get_absolute_url(paginator.num_pages))

    data = {
        "users": users,
        "title": "User List",
        "user_list_page": user_list_page,
    }
    return render(request, "accounts/user-list.html" , data)
    
def user_profile(request, username=None, tab='user'):
    if username == None:
        if request.user.is_authenticated():
            user = request.user
        else:
            return redirect_to_login(next=reverse("accounts-profile"))
    else:
        user = get_object_or_404(User, username=username)
    profiles = profile_register.get_profiles()
    positions = profile_register.get_positions()
    data = {
        "user": user,
        "title": "User Profile",
        "tab": tab,
    }
    if request.user == user:
        # user is viewing their own profile, let them edit
        profile = profiles.get(tab)
        if not profile:
            raise Http404
        data["profile_label"] = profile.label
        data["profile_data"] = profile(user).edit(request)
        data["profiles"] = sorted([(tab, prof(user)) for tab, prof in profiles.items() if prof.show_tab], key=lambda x: positions.get(x[0], 0))
        return render(request, "accounts/edit-profile.html" , data)
    else:
        # some else's profile, show basic info
        profile_data = []
        for name, cls in profiles.items():
            if not cls.show_tab:
                continue
            info = cls(user).info()
            info["position"] = positions.get(name, 0)
            profile_data.append(info)
            data.update(info.get("data", {}))
        data["profile_data"] = sorted(profile_data, key=lambda x: x.get("position", 0))
        return render(request, "accounts/view-profile.html" , data)
    
def user_admin(request, username):
    pass