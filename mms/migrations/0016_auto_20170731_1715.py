# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-31 17:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mms', '0015_auto_20170731_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='weekid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mms.Week'),
            preserve_default=False,
        ),
    ]
