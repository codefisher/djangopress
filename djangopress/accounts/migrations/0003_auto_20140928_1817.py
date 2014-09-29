# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140928_1807'),
        ('accounts', '0002_auto_20140927_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='properties',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='property',
            field=models.ForeignKey(blank=True, to='core.Property', null=True),
            preserve_default=True,
        ),
    ]
