import random
import os
import datetime
import time

from django.db import models
from django.conf import settings
from django.contrib.auth.models import get_hexdigest, User
from django.db.models.signals import post_save


from djangopress.core.models import Property

# Create your models here.

class UserProfile(models.Model):
    pass
    """

    """
    title = models.CharField(max_length=100, default="New member")
    homepage = models.CharField(max_length=100, blank=True)
    #IM contact (jabber, icq, msn, aim, yahoo, gtalk, twitter, facebook)
    location = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(blank=True,
            upload_to=os.path.join(settings.MEDIA_UPLOAD, "avatars"))
    signature = models.TextField(blank=True)
    timezone = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=20, blank=True)
    registration_ip = models.IPAddressField()
    last_ip_used = models.IPAddressField()
    admin_note = models.TextField(blank=True)
    activate_key = models.CharField(max_length=127, blank=True, editable=False)
    activate_key_expirary = models.DateTimeField(blank=True, editable=False)
    banned = models.BooleanField(default=False)
    remember_between_visits = models.BooleanField(default=True)
    user = models.OneToOneField(User)
    properties = models.ManyToManyField(Property, null=True)

    def set_activate_key(self):
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        key = "".join(str(item) for item in (self.user.username,
                self.user.email, datetime.datetime.now()))
        hsh = get_hexdigest(algo, salt, key)
        self.activate_key = hsh
        self.activate_key_expirary = datetime.datetime.fromtimestamp(time.time() + (7 * 24 * 60 * 60))

    def check_activate_key(self, hsh):
        print self.activate_key_expirary, datetime.datetime.now()
        return (hsh == self.activate_key
                and datetime.datetime.now() <= self.activate_key_expirary)

def create_profile(sender, **kargs):
    if kargs.get("created", False):
        profile = UserProfile(user=kargs.get("instance"))
        profile.set_activate_key()
        profile.save()
post_save.connect(create_profile, User, dispatch_uid="djangopress.accounts.create_profile")

class UsersOnline(models.Model):
    user = models.OneToOneField(User)
    ip = models.IPAddressField()
    logged_date =  models.DateTimeField()
    idle = models.BooleanField(default=False)


class UserBan(models.Model):
    ban_user = models.ForeignKey(User, related_name='banned_users')
    ban_ip = models.IPAddressField()
    ban_email = models.CharField(max_length=100)
    ban_name = models.CharField(max_length=100)

    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True)
    given_reason =models.TextField(blank=True)

