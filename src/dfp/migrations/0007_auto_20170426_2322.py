# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-26 23:22
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('dfp', '0006_report_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportType',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='dimension',
            name='report_types',
            field=models.ManyToManyField(to='dfp.ReportType'),
        ),
    ]
