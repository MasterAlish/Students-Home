# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-13 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0035_auto_20170327_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='grouvi_user_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Grouvi User ID'),
        ),
    ]