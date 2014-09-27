# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'New member', max_length=100)),
                ('homepage', models.CharField(max_length=100, null=True, blank=True)),
                ('location', models.CharField(max_length=50, null=True, blank=True)),
                ('avatar', models.ImageField(null=True, upload_to=b'/home/michael/WebSites/dev/codefisher/djangopress/../www/media/avatars', blank=True)),
                ('signature', models.TextField(null=True, blank=True)),
                ('timezone', models.CharField(max_length=20, null=True, blank=True)),
                ('language', models.CharField(max_length=20, null=True, blank=True)),
                ('registration_ip', models.IPAddressField(null=True, blank=True)),
                ('last_ip_used', models.IPAddressField(null=True, blank=True)),
                ('admin_note', models.TextField(null=True, blank=True)),
                ('activate_key', models.CharField(max_length=127, editable=False, blank=True)),
                ('activate_key_expirary', models.DateTimeField(editable=False, blank=True)),
                ('banned', models.BooleanField(default=False)),
                ('email_settings', models.CharField(default=b'HI', max_length=2, choices=[(b'HI', b'Hide Email'), (b'SW', b'Show Email'), (b'HB', b'Use Web Form')])),
                ('properties', models.ManyToManyField(to='core.Property', null=True, blank=True)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
