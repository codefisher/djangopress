# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140928_1807'),
        ('forum', '0002_auto_20140927_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumgroup',
            name='properties',
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='property',
            field=models.ForeignKey(blank=True, to='core.Property', null=True),
            preserve_default=True,
        ),
    ]
