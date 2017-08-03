# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20140928_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='value_type',
            field=models.CharField(choices=[('s', 'string'), ('i', 'integer'), ('b', 'boolean'), ('f', 'float')], max_length=1),
        ),
    ]
