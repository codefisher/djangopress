# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_ip_used',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='registration_ip',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
    ]
