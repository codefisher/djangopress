# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20140928_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumgroup',
            name='format',
            field=models.CharField(max_length=20, choices=[(b'magic_html', b'Magic HTML'), (b'markdown', b'Markdown'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template'), (b'restructuredtext', b'reStructuredText')]),
        ),
    ]
