# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20150801_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallerysection',
            name='listed',
            field=models.BooleanField(default=True),
        ),
    ]
