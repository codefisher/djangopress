# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_forumgroup_post_redirect_delay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumgroup',
            name='format',
            field=models.CharField(max_length=20, choices=[(b'extended_html', b'Extended HTML'), (b'magic_html', b'Magic HTML'), (b'markdown', b'Markdown'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template'), (b'restructuredtext', b'reStructuredText')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='poster_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='poster_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
