# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_page_head_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textblock',
            name='pageblock_ptr',
        ),
        migrations.RemoveField(
            model_name='page',
            name='blocks',
        ),
        migrations.DeleteModel(
            name='TextBlock',
        ),
        migrations.RemoveField(
            model_name='pageblock',
            name='class_name',
        ),
        migrations.AddField(
            model_name='pageblock',
            name='data',
            field=models.TextField(default='', verbose_name=b'Content', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pageblock',
            name='page',
            field=models.ForeignKey(blank=True, to='pages.Page', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pageblock',
            name='render',
            field=models.CharField(default='html', max_length=30, choices=[(b'magic_html', b'Magic HTML'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template')]),
            preserve_default=False,
        ),
    ]
