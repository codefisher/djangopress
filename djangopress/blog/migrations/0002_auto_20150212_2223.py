# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangopress.blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='description',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='post_image',
            field=models.ImageField(null=True, upload_to=djangopress.blog.models.post_image_path, blank=True),
            preserve_default=True,
        ),
    ]
