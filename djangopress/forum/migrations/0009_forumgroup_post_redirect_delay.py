# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20141005_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumgroup',
            name='post_redirect_delay',
            field=models.IntegerField(default=3, help_text=b'How long to show the successful post page, before redirecting.  Set to 0 to disable.'),
            preserve_default=True,
        ),
    ]
