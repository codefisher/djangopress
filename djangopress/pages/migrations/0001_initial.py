# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Page Title')),
                ('location', models.CharField(db_index=True, max_length=200, null=True, editable=False, blank=True)),
                ('override_location', models.CharField(max_length=200, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('edited', models.DateTimeField(auto_now=True, verbose_name=b'Last Edited')),
                ('posted', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Publication Date', editable=False, blank=True)),
                ('status', models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PR', b'Pending Review'), (b'PB', b'Published')])),
                ('visibility', models.CharField(default=b'VI', max_length=2, choices=[(b'VI', b'Visible'), (b'PR', b'Private')])),
                ('login_required', models.BooleanField(default=False)),
                ('meta_page_title', models.TextField(null=True, verbose_name=b'Page title tag', blank=True)),
                ('meta_keywords', models.TextField(null=True, verbose_name=b'Keywords meta tag', blank=True)),
                ('meta_description', models.TextField(null=True, verbose_name=b'Description meta tag', blank=True)),
                ('author', models.ForeignKey(related_name=b'pages', editable=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_name', models.CharField(max_length=50, editable=False, db_index=True)),
                ('block_name', models.CharField(max_length=50, editable=False, db_index=True)),
                ('position', models.IntegerField(null=True, blank=True)),
                ('block_id', models.CharField(max_length=50, blank=True, help_text=b'Name used to refer to the block in templates', null=True, verbose_name=b'Id', db_index=True)),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('template', models.CharField(help_text=b'The path to any template file accessible to the template loader', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('pageblock_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.PageBlock', on_delete=models.CASCADE)),
                ('data', models.TextField(verbose_name=b'Content', blank=True)),
                ('format', models.CharField(max_length=30, choices=[(b'magic_html', b'Magic HTML'), (b'bbcode', b'BBcode'), (b'sanitized_html', b'Sanitized HTML'), (b'plain_text', b'Plain Text'), (b'html', b'HTML'), (b'template', b'Django Template')])),
            ],
            options={
            },
            bases=('pages.pageblock',),
        ),
        migrations.AddField(
            model_name='page',
            name='blocks',
            field=models.ManyToManyField(related_name=b'pages', null=True, to='pages.PageBlock', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='edited_by',
            field=models.ForeignKey(related_name=b'edited_pages', editable=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(related_name=b'sub_pages', blank=True, to='pages.Page', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(to='pages.PageTemplate', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('slug', 'parent')]),
        ),
    ]
