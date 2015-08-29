# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_image_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallerysection',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
