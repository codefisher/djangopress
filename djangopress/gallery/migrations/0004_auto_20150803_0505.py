# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_gallerysection_listed'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 3, 5, 5, 29, 910904), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(height_field=b'height', width_field=b'width', upload_to=b'images/gallery/%y/%m/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='scaled',
            field=models.ImageField(upload_to=b'images/gallery/scaled/%y/%m/', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(upload_to=b'images/gallery/thumbs/%y/%m/', editable=False),
        ),
    ]
