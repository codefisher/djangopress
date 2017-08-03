# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='upload',
            field=models.FileField(upload_to=b'files/%y/%m'),
        ),
    ]
