# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20150426_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='subscriptions',
            field=models.ManyToManyField(related_name='forum_forum_subscriptions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='subscriptions',
            field=models.ManyToManyField(related_name='forum_subscriptions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
