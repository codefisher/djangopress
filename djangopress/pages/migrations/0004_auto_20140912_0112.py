# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20140907_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageblock',
            name='block_name',
            field=models.CharField(max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='page',
            field=models.ForeignKey(related_name=b'blocks', blank=True, to='pages.Page', null=True),
        ),
    ]
