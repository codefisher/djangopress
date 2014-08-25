import random
import os
import datetime
import time
import hashlib

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from djangopress.core.models import Property
from djangopress.core.format import Library

class UserProfile(models.Model):
    """

    """
    
    EMAIL_SETTINGS = (
        ('HI', 'Hide Email'),
        ('SW', 'Show Email'),
        ('HB', 'Use Web Form')
    )
    
    title = models.CharField(max_length=100, default="New member")
    homepage = models.CharField(max_length=100, blank=True, null=True)
    #IM contact (jabber, icq, msn, aim, yahoo, gtalk, twitter, facebook)
    location = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True,
            upload_to=os.path.join(settings.MEDIA_UPLOAD, "avatars"))
    signature = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    registration_ip = models.IPAddressField(blank=True, null=True)
    last_ip_used = models.IPAddressField(blank=True, null=True)
    admin_note = models.TextField(blank=True, null=True)
    activate_key = models.CharField(max_length=127, blank=True, editable=False)
    activate_key_expirary = models.DateTimeField(blank=True, editable=False)
    banned = models.BooleanField(default=False)
    #remember_between_visits = models.BooleanField(default=True)
    user = models.OneToOneField(User, related_name="profile")
    properties = models.ManyToManyField(Property, null=True, blank=True)

    email_settings = models.CharField(choices=EMAIL_SETTINGS, default='HI', max_length=2)

    
    def get_signature(self, *args, **kargs):
        try:
            bbcode = Library.get("bbcode").get("function")
            return bbcode(self.signature, *args, **kargs)
        except:
            return ""

    def set_activate_key(self):
        salt = hashlib.sha1(str(random.random()) + str(random.random())).hexdigest()[:5]
        key = "".join(str(item) for item in (self.user.username,
                self.user.email, datetime.datetime.now()))
        hsh = hashlib.sha1(salt + key).hexdigest()
        self.activate_key = hsh
        self.activate_key_expirary = datetime.datetime.fromtimestamp(time.time() + (7 * 24 * 60 * 60))

    def check_activate_key(self, hsh):
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

