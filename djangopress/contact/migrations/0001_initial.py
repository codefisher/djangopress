# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MailLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=200, verbose_name=b'Subject')),
                ('email', models.CharField(max_length=100, verbose_name=b'E-mail')),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('message', models.TextField(verbose_name=b'Message')),
                ('to', models.ForeignKey(verbose_name=b'To', to='contact.MailAddress', on_delete=models.CASCADE)),
            ],
        ),
    ]
