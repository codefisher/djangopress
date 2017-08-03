# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 05:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_auto_20170710_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageblock',
            name='render',
            field=models.CharField(choices=[('plain_text', 'Plain Text'), ('magic_html', 'Magic HTML'), ('markdown', 'Markdown'), ('html', 'HTML'), ('extended_html', 'Extended HTML'), ('sanitized_html', 'Sanitized HTML'), ('bbcode', 'BBcode'), ('template', 'Django Template')], default='extended_html', max_length=30),
        ),
    ]
