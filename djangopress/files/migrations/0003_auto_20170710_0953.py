# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20150805_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='upload',
            field=models.FileField(upload_to='files/%y/%m'),
        ),
    ]
