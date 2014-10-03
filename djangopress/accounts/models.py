import random
import os
import datetime
import time
import hashlib

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from djangopress.core.models import Property
from djangopress.core.format import Library

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
    avatar = models.ImageField(blank=True, null=True,
            upload_to=os.path.join(settings.MEDIA_UPLOAD, "avatars"))
    signature = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=20, null=True, blank=True)
    registration_ip = models.GenericIPAddressField(blank=True, null=True, )
    last_ip_used = models.GenericIPAddressField(blank=True, null=True)
    admin_note = models.TextField(blank=True, null=True)
    activate_key = models.CharField(max_length=127, blank=True, editable=False)
    activate_key_expirary = models.DateTimeField(blank=True, editable=False)
    banned = models.BooleanField(default=False)
    #remember_between_visits = models.BooleanField(default=True)
    user = models.OneToOneField(User, related_name="profile")
    email_settings = models.CharField(choices=EMAIL_SETTINGS, default='HI', max_length=2)
    gender = models.CharField(max_length=1, blank=True, null=True, default=None, choices=(('', 'Private'), ('M', 'Male'), ('F', 'Female')))
    date_of_birth = models.DateTimeField(blank=True, null=True)
    
    def get_ip(self):
        if self.last_ip_used:
            return self.last_ip_used
        return self.registration_ip
            
    
    def get_absolute_url(self):
        return reverse('accounts-profile', kwargs={"username": self.user.username}) 

    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self._banned = self.banned

    def save(self, force_insert=False, force_update=False):
        if self._banned == False and self.banned == True:
            # if we banned them, they can't then login
            self.user.is_active = False
            self.user.save()
        super(UserProfile, self).save(force_insert, force_update)
        self._banned = self.banned
    
    def get_signature(self, *args, **kargs):
        if not self.signature:
            return ""
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
                and datetime.datetime.utcnow() <= self.activate_key_expirary)

class UserProperty(Property):
    user_profile = models.ForeignKey(User, related_name="properties")
    
def create_profile(sender, **kargs):
    if kargs.get("created", False):
        profile = UserProfile(user=kargs.get("instance"))
        profile.set_activate_key()
        profile.save()
post_save.connect(create_profile, User, dispatch_uid="djangopress.accounts.create_profile")

def add_to_group(sender, **kargs):
    if kargs.get("created", False):
        user = kargs.get("instance")
        user.groups.add(Group.objects.get(name=settings.DEFAULT_USER_GROUP))
post_save.connect(add_to_group, User, dispatch_uid="djangopress.accounts.add_to_group")