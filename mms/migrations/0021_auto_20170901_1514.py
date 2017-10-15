# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-01 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('mms', '0020_auto_20170901_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfocollect',
            name='registtime',
            field=models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentinfocollect',
            name='sex',
            field=models.CharField(default='\u672a\u8bb0\u5f55', max_length=10),
        ),
    ]