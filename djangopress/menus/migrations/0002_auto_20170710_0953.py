# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='renderer',
            field=models.CharField(default='default', max_length=100),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='renderer',
            field=models.CharField(default='default', max_length=100),
        ),
    ]
