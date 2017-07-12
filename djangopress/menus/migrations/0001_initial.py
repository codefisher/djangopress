# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('class_tag', models.CharField(max_length=100, null=True, blank=True)),
                ('renderer', models.CharField(default=b'default', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=255, null=True, blank=True)),
                ('index', models.IntegerField(default=0)),
                ('id_tag', models.CharField(max_length=100, null=True, blank=True)),
                ('class_tag', models.CharField(max_length=100, null=True, blank=True)),
                ('renderer', models.CharField(default=b'default', max_length=100)),
                ('menu', models.ForeignKey(to='menus.Menu', on_delete=models.CASCADE)),
                ('parent', models.ForeignKey(blank=True, to='menus.MenuItem', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
