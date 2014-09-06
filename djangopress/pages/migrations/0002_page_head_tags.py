# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='head_tags',
            field=models.TextField(null=True, verbose_name=b'Extra tags to be added to the page header', blank=True),
            preserve_default=True,
        ),
    ]
