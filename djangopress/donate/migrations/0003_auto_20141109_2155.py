# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0002_auto_20140909_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='link_text',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Link Text (optional)', blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='link_url',
            field=models.URLField(null=True, verbose_name=b'Link Url (optional)', blank=True),
        ),
    ]
