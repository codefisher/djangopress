# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ipn', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('amount', models.FloatField(default=0, blank=True)),
                ('link_url', models.URLField(null=True, blank=True)),
                ('link_text', models.CharField(max_length=50, null=True, blank=True)),
                ('validated', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(max_length=50, null=True, blank=True)),
                ('payment', models.ForeignKey(blank=True, to='ipn.PayPalIPN', null=True, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
