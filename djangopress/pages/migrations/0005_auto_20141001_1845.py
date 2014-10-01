# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20140912_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='location',
            field=models.CharField(max_length=200, unique=True, null=True, editable=False, blank=True),
        ),
    ]
