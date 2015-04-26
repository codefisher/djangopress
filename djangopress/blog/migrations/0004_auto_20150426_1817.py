# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150216_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_email',
            field=models.EmailField(max_length=254, verbose_name=b'Email address', blank=True),
        ),
    ]
