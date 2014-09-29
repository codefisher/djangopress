# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20140928_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default=None, max_length=1, null=True, blank=True, choices=[(b'', b'Private'), (b'M', b'Male'), (b'F', b'Female')]),
            preserve_default=True,
        ),
    ]
