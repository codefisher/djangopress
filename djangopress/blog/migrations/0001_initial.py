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
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
                ('tagline', models.TextField(blank=True)),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
            options={
                'verbose_name': 'blog',
                'verbose_name_plural': 'blogs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('blog', models.ForeignKey(related_name=b'categories', to='blog.Blog', on_delete=models.CASCADE)),
                ('parent_category', models.ForeignKey(related_name=b'child_categories', blank=True, to='blog.Category', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=50, verbose_name=b'Name', blank=True)),
                ('user_email', models.EmailField(max_length=75, verbose_name=b'Email address', blank=True)),
                ('user_url', models.URLField(verbose_name=b'Website', blank=True)),
                ('comment_text', models.TextField(max_length=5000)),
                ('rank', models.IntegerField(default=0)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(null=True, verbose_name=b'IP address', blank=True)),
                ('user_agent', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=True, help_text=b'Uncheck this box to make the comment effectively disappear from the site.', verbose_name=b'is public')),
                ('is_removed', models.BooleanField(default=False, help_text=b'Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', verbose_name=b'is removed')),
                ('is_spam', models.BooleanField(default=False, help_text=b'Check this box to flag as spam.', verbose_name=b'is spam')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Post Title')),
                ('slug', models.SlugField(unique_for_date=b'posted')),
                ('body', models.TextField(verbose_name=b'Post Contents')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name=b'Last Edited')),
                ('posted', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Publication Date', blank=True)),
                ('status', models.CharField(default=b'DR', max_length=2, choices=[(b'DR', b'Draft'), (b'PR', b'Pending Review'), (b'PB', b'Published')])),
                ('sticky', models.BooleanField(default=False)),
                ('visibility', models.CharField(default=b'VI', max_length=2, choices=[(b'VI', b'Visible'), (b'PR', b'Private')])),
                ('comments_open', models.BooleanField(default=True)),
                ('author', models.ForeignKey(related_name=b'blog_entries', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('blog', models.ForeignKey(related_name=b'entries', to='blog.Blog', on_delete=models.CASCADE)),
                ('categories', models.ManyToManyField(to='blog.Category')),
                ('edited_by', models.ForeignKey(related_name=b'blog_edited_entries', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'entry',
                'verbose_name_plural': 'entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag', models.CharField(max_length=100, verbose_name=b'flag')),
                ('flag_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(related_name=b'flag', to='blog.Comment', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(related_name=b'comment_flags', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('blog', models.ForeignKey(related_name=b'tags', to='blog.Blog', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('slug', 'blog')]),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(to='blog.Entry', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, to='blog.Comment', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name=b'blog_comments', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('slug', 'blog')]),
        ),
    ]
