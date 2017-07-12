# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20140928_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumproperty',
            name='forums',
            field=models.ForeignKey(related_name=b'properties', to='forum.ForumGroup', on_delete=models.CASCADE),
        ),
    ]
