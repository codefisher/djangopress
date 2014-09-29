# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140928_1807'),
        ('forum', '0003_auto_20140928_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumgroup',
            name='property',
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='properties',
            field=models.ManyToManyField(to='core.Property', null=True, blank=True),
            preserve_default=True,
        ),
    ]
