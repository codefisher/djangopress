# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0007_auto_20150829_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallerysection',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
