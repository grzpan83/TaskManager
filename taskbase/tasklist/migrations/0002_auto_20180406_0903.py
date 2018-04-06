# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-06 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Highest'), (2, 'High'), (3, 'Medium'), (4, 'Low')], default=4),
        ),
    ]
