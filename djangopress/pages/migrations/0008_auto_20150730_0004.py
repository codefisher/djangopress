# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangopress.pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20150426_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload', models.FileField(upload_to=djangopress.pages.models.page_file_path)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.ForeignKey(blank=True, to='pages.PageTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='block_name',
            field=models.CharField(default=b'content', max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='render',
            field=models.CharField(default=b'extended_html', max_length=30, choices=[(b'extended_html', b'Extended HTML'), (b'magic_html', b'Magic HTML'), (b'markdown', b'Markdown'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template'), (b'restructuredtext', b'reStructuredText')]),
        ),
        migrations.AddField(
            model_name='pagefile',
            name='page',
            field=models.ForeignKey(related_name='files', to='pages.Page'),
        ),
    ]
