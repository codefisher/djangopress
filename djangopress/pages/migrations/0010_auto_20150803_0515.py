# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_page_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagefile',
            name='page',
        ),
        migrations.DeleteModel(
            name='PageFile',
        ),
    ]
