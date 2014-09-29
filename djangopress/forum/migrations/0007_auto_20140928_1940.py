# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20140928_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumgroup',
            name='announcement',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='display_images',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='make_links',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='number_of_posts',
            field=models.IntegerField(default=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='number_of_threads',
            field=models.IntegerField(default=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='show_announcement',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='show_avatars',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='show_quick_post',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='show_signature',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumgroup',
            name='show_smilies',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='forumgroup',
            name='format',
            field=models.CharField(max_length=20, choices=[(b'magic_html', b'Magic HTML'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template')]),
        ),
    ]
