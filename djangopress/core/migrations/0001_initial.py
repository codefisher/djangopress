# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_name', models.CharField(max_length=50, editable=False, db_index=True)),
                ('property', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntProperty',
            fields=[
                ('property_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Property')),
                ('property_value', models.IntegerField()),
            ],
            options={
            },
            bases=('core.property',),
        ),
        migrations.CreateModel(
            name='CharProperty',
            fields=[
                ('property_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Property')),
                ('property_value', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=('core.property',),
        ),
    ]
