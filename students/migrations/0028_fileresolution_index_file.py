# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-10 23:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0027_auto_20170206_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileresolution',
            name='index_file',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='\u0424\u0430\u0439\u043b index.html'),
        ),
    ]
