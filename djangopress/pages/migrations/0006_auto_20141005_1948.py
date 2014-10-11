# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20141001_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageblock',
            name='render',
            field=models.CharField(max_length=30, choices=[(b'magic_html', b'Magic HTML'), (b'markdown', b'Markdown'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template'), (b'restructuredtext', b'reStructuredText')]),
        ),
    ]
