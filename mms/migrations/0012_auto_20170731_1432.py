# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-31 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mms', '0011_auto_20170731_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completion',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='reason',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
