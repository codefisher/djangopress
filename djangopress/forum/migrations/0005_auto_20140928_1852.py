# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20140928_1807'),
        ('forum', '0004_auto_20140928_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumProperty',
            fields=[
                ('property_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Property')),
                ('forums', models.ForeignKey(related_name=b'property', to='forum.ForumGroup')),
            ],
            options={
            },
            bases=('core.property',),
        ),
        migrations.RemoveField(
            model_name='forumgroup',
            name='properties',
        ),
    ]
