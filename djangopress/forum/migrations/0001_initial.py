# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('download_count', models.IntegerField(default=0)),
                ('comment', models.TextField()),
                ('attachment', models.FileField(upload_to=b'forum/upload/%Y/%m/%d/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('num_threads', models.IntegerField(default=0, verbose_name=b'Number of Threads')),
                ('num_posts', models.IntegerField(default=0, verbose_name=b'Number of Posts')),
                ('position', models.IntegerField(default=1)),
                ('password', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'permissions': (('can_post_threads', 'User is allowed to post new thread'), ('can_close_threads', 'User is allowed to close a thread'), ('can_sticky_threads', 'User is allowed to sticky a thread'), ('can_moderate_forum', 'Has access to all the batch moderation options')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('position', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('tagline', models.TextField(blank=True)),
                ('format', models.CharField(max_length=20)),
                ('properties', models.ManyToManyField(to='core.Property', null=True, blank=True)),
                ('sites', models.ManyToManyField(related_name=b'forums', to='sites.Site')),
            ],
            options={
                'permissions': (('can_read_forum_group', 'User is allowed to read forum'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_threads', models.IntegerField(default=0)),
                ('num_posts', models.IntegerField(default=0)),
                ('notify', models.CharField(default=b'AL', max_length=2, choices=[(b'AL', b'Always Notify'), (b'NV', b'Never Notify')])),
                ('show_simlies', models.BooleanField(default=True, help_text=b'Show smilies in forum posts.')),
                ('show_img', models.BooleanField(default=True, help_text=b'Show images in forum posts.', verbose_name=b'Show Images')),
                ('show_avatars', models.BooleanField(default=True, help_text=b'Show that avatar images of users.')),
                ('show_sig', models.BooleanField(default=True, help_text=b'Show user signature after their posts.', verbose_name=b'Show Signature')),
                ('user', models.OneToOneField(related_name=b'forum_profile', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poster_name', models.CharField(max_length=50, null=True, blank=True)),
                ('poster_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('ip', models.IPAddressField()),
                ('message', models.TextField()),
                ('format', models.CharField(max_length=20)),
                ('show_similies', models.BooleanField(default=True, help_text=b'Show smilies as icons for this post.')),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(null=True, blank=True)),
                ('edit_reason', models.CharField(max_length=200, null=True, blank=True)),
                ('is_public', models.BooleanField(default=True, help_text=b'Uncheck this box to make the post effectively disappear from the site.', verbose_name=b'is public')),
                ('is_removed', models.BooleanField(default=False, help_text=b'Check this box if the post is inappropriate. A "This post has been removed" message will be displayed instead.', verbose_name=b'is removed')),
                ('is_spam', models.BooleanField(default=False, help_text=b'Check this box to flag as spam.', verbose_name=b'is spam')),
                ('author', models.ForeignKey(related_name=b'forum_posts', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('edited_by', models.ForeignKey(related_name=b'forum_posts_edited', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'permissions': (('can_edit_own_posts', 'User is allowed to edit posts they have made'), ('can_edit_others_posts', 'User is allowed to edit posts others have made'), ('can_mark_removed', 'Can mark the post as removed/not removed'), ('can_mark_public', 'Can mark if a post is public or not'), ('can_mark_spam', 'Can mark a post as spam/not spam')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('min_posts', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('moderated', models.BooleanField(default=False)),
                ('moderated_by', models.ForeignKey(related_name=b'forum_moderated_reports', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('post', models.ForeignKey(related_name=b'reports', to='forum.Post', on_delete=models.CASCADE)),
                ('reported_by', models.ForeignKey(related_name=b'forum_reports', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poster_name', models.CharField(max_length=50, null=True, blank=True)),
                ('poster_email', models.EmailField(max_length=75, null=True, blank=True)),
                ('subject', models.CharField(max_length=255)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('last_post_date', models.DateTimeField(null=True, blank=True)),
                ('num_views', models.IntegerField(default=0)),
                ('num_posts', models.IntegerField(default=0)),
                ('closed', models.BooleanField(default=False)),
                ('sticky', models.BooleanField(default=False)),
                ('first_post', models.ForeignKey(related_name=b'thread_first', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='forum.Post', null=True)),
                ('forum', models.ForeignKey(to='forum.Forum', on_delete=models.CASCADE)),
                ('last_post', models.ForeignKey(related_name=b'thread_last', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='forum.Post', null=True)),
                ('moved_to', models.ForeignKey(blank=True, to='forum.Thread', null=True, on_delete=models.CASCADE)),
                ('poster', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('subscriptions', models.ManyToManyField(related_name=b'forum_subscriptions', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'permissions': (('can_post_replies', 'User is allowed to reply to threads'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(related_name=b'posts', to='forum.Thread', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forumcategory',
            name='forums',
            field=models.ForeignKey(related_name=b'category', to='forum.ForumGroup', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(related_name=b'forum', blank=True, to='forum.ForumCategory', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='last_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='forum.Post', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='parent_forum',
            field=models.ForeignKey(related_name=b'children', blank=True, to='forum.Forum', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='forum',
            name='subscriptions',
            field=models.ManyToManyField(related_name=b'forum_forum_subscriptions', null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(related_name=b'attachments', to='forum.Post', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='poster',
            field=models.ForeignKey(related_name=b'forum_attachments', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
