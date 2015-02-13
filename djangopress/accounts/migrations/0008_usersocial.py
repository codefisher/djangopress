# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_auto_20141019_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSocial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account', models.CharField(max_length=20, choices=[(b'twitter', b'Twitter'), (b'google_plus', b'Google Plus'), (b'facebook', b'Facebook'), (b'linkedin', b'Linked In'), (b'pinterest', b'Pinterest')])),
                ('value', models.CharField(max_length=100)),
                ('user_profile', models.ForeignKey(related_name=b'social', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
