# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-13 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imgpost', '0007_imgpost_downloads'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imgpost',
            name='height',
        ),
        migrations.RemoveField(
            model_name='imgpost',
            name='width',
        ),
    ]
