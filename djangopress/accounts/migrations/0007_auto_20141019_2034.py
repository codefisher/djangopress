# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangopress.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20140928_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to=djangopress.accounts.models.avatar_path, blank=True),
        ),
    ]
