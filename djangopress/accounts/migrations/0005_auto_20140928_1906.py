# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20140928_1906'),
        ('accounts', '0004_auto_20140928_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProperty',
            fields=[
                ('property_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Property')),
                ('user_profile', models.ForeignKey(related_name=b'properties', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=('core.property',),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='properties',
        ),
    ]
