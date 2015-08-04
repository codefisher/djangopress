# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charproperty',
            name='property_ptr',
        ),
        migrations.DeleteModel(
            name='CharProperty',
        ),
        migrations.RemoveField(
            model_name='intproperty',
            name='property_ptr',
        ),
        migrations.DeleteModel(
            name='IntProperty',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='property',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='property',
            name='class_name',
        ),
        migrations.AddField(
            model_name='property',
            name='value',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='value_type',
            field=models.CharField(default='s', max_length=1, choices=[(b's', b'string'), (b'i', b'integer'), (b'b', b'boolean'), (b'f', b'float')]),
            preserve_default=False,
        ),
    ]
