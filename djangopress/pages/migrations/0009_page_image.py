# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangopress.pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20150730_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='image',
            field=models.ImageField(null=True, upload_to=djangopress.pages.models.page_file_path, blank=True),
        ),
    ]
