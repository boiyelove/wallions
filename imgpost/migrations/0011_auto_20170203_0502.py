# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-03 10:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgpost', '0010_imgpost_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imgpost',
            name='downloads',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='imgpost',
            name='views',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
