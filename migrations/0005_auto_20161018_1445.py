# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 14:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance_manager', '0004_auto_20161002_1527'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instance',
            options={'permissions': (('is_owner', 'Is Owner'),)},
        ),
    ]
