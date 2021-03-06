import random
import datetime
import time
import hashlib

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from djangopress.core.models import Property
from django.utils import timezone
from PIL import Image

DEFAULT_USER_GROUP = getattr(settings, 'DEFAULT_USER_GROUP', None)

def avatar_path(instance, filename):
    return ("avatars/%s/%s-%s-%s" % (time.strftime("%y/%m"), instance.user.pk, instance.user.username.lower(), filename.lower()))

class UserProfile(models.Model):
    EMAIL_SETTINGS = (
        ('HI', 'Hide Email'),
        ('SW', 'Show Email'),
        ('HB', 'Use Web Form')
    )
    
    title = models.CharField(max_length=100, default="New member")
    homepage = models.CharField(max_length=100, blank=True, null=True)
    #IM contact (jabber, icq, msn, aim, yahoo, gtalk, twitter, facebook)
    location = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to=avatar_path)
    signature = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    registration_ip = models.GenericIPAddressField(blank=True, null=True, )
    last_ip_used = models.GenericIPAddressField(blank=True, null=True)
    admin_note = models.TextField(blank=True, null=True)
    activate_key = models.CharField(max_length=127, blank=True, editable=False)
    activate_key_expirary = models.DateTimeField(blank=True, editable=False)
    banned = models.BooleanField(default=False)
    #remember_between_visits = models.BooleanField(default=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    email_settings = models.CharField(choices=EMAIL_SETTINGS, default='HI', max_length=2)
    gender = models.CharField(max_length=1, blank=True, null=True, default=None, choices=(('', 'Private'), ('M', 'Male'), ('F', 'Female')))
    date_of_birth = models.DateTimeField(blank=True, null=True)
    
    def get_ip(self):
        if self.last_ip_used:
            return self.last_ip_used
        return self.registration_ip
            
    def __getattr__(self, name):
        if name.startswith("social_"):
            try:
                return self.user.social.filter(account=name[7:])[0]
            except:
                raise AttributeError(name)
        return super(UserProfile, self).__getattr__(name)
    
    def get_absolute_url(self):
        return reverse('accounts-profile', kwargs={"username": self.user.username}) 

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self._banned = self.banned
        self._avatar = self.avatar

    def save(self, force_insert=False, force_update=False):
        if self._banned == False and self.banned == True:
            # if we banned them, they can't then login
            self.user.is_active = False
            self.user.save()
        if self._avatar != self.avatar and self.avatar:
            image = Image.open(self.avatar)
            size = settings.ACCOUNTS_USER_LIMITS.get('avatar', {}).get('size', 50)
            image.resize((size, size), Image.ANTIALIAS)
            image.save(self.avatar.path)
        super(UserProfile, self).save(force_insert, force_update)
        self._banned = self.banned
        self._avatar = self.avatar
    
    def set_activate_key(self):
        salt = hashlib.sha1((str(random.random()) + str(random.random())).encode('utf-8')).hexdigest()[:5]
        key = "".join(str(item) for item in (self.user.username,
                self.user.email, datetime.datetime.now()))
        hsh = hashlib.sha1((salt + key).encode('utf-8')).hexdigest()
        self.activate_key = hsh
        self.activate_key_expirary = datetime.datetime.fromtimestamp(time.time() + (7 * 24 * 60 * 60))

    def check_activate_key(self, hsh):
        return (hsh == self.activate_key
                and timezone.now() <= self.activate_key_expirary)

class UserSocial(models.Model):
    ACCOUNTS = (
        ('twitter', 'Twitter'),
        ('google_plus', 'Google Plus'),
        ('facebook', 'Facebook'),
        ('linkedin', 'Linked In'),
        ('pinterest', 'Pinterest'),
    )
    account = models.CharField(max_length=20, choices=ACCOUNTS)
    value = models.CharField(max_length=100)
    user_profile = models.ForeignKey(User, related_name="social", on_delete=models.CASCADE)

class UserProperty(Property):
    user_profile = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
    
def create_profile(sender, **kargs):
    if kargs.get("created", False):
        profile = UserProfile(user=kargs.get("instance"))
        profile.set_activate_key()
        profile.save()
post_save.connect(create_profile, User, dispatch_uid="djangopress.accounts.create_profile")

def add_to_group(sender, **kargs):
    if DEFAULT_USER_GROUP and kargs.get("created", False):
        user = kargs.get("instance")
        user.groups.add(Group.objects.get(name=DEFAULT_USER_GROUP))
post_save.connect(add_to_group, User, dispatch_uid="djangopress.accounts.add_to_group")