# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 09:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_auto_20150803_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='edited',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Edited'),
        ),
        migrations.AlterField(
            model_name='page',
            name='head_tags',
            field=models.TextField(blank=True, null=True, verbose_name='Extra tags to be added to the page header'),
        ),
        migrations.AlterField(
            model_name='page',
            name='meta_description',
            field=models.TextField(blank=True, null=True, verbose_name='Description meta tag'),
        ),
        migrations.AlterField(
            model_name='page',
            name='meta_keywords',
            field=models.TextField(blank=True, null=True, verbose_name='Keywords meta tag'),
        ),
        migrations.AlterField(
            model_name='page',
            name='meta_page_title',
            field=models.TextField(blank=True, null=True, verbose_name='Page title tag'),
        ),
        migrations.AlterField(
            model_name='page',
            name='posted',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, editable=False, verbose_name='Publication Date'),
        ),
        migrations.AlterField(
            model_name='page',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PR', 'Pending Review'), ('PB', 'Published')], default='DR', max_length=2),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Page Title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='visibility',
            field=models.CharField(choices=[('VI', 'Visible'), ('PR', 'Private')], default='VI', max_length=2),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='block_id',
            field=models.CharField(blank=True, db_index=True, help_text='Name used to refer to the block in templates', max_length=50, null=True, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='block_name',
            field=models.CharField(db_index=True, default='content', max_length=50),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='data',
            field=models.TextField(blank=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='pageblock',
            name='render',
            field=models.CharField(choices=[('html', 'HTML'), ('template', 'Django Template'), ('bbcode', 'BBcode'), ('plain_text', 'Plain Text'), ('markdown', 'Markdown'), ('extended_html', 'Extended HTML'), ('sanitized_html', 'Sanitized HTML'), ('magic_html', 'Magic HTML')], default='extended_html', max_length=30),
        ),
        migrations.AlterField(
            model_name='pagetemplate',
            name='template',
            field=models.CharField(help_text='The path to any template file accessible to the template loader', max_length=200),
        ),
    ]
