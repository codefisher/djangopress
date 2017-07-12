# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='scaled',
            field=models.ImageField(upload_to=b'images/gallery/scaled/', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='gallery',
            field=models.ForeignKey(blank=True, to='gallery.GallerySection', null=True, on_delete=models.CASCADE),
        ),
    ]
