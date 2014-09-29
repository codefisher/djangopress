# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140928_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='value',
            field=models.TextField(),
        ),
    ]
