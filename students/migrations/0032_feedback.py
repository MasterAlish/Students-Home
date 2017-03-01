# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-27 00:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0031_homeworksolution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000, verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('mobile', models.BooleanField(default=False, verbose_name='\u0421 \u043c\u043e\u0431\u0438\u043b\u044c\u043d\u043e\u0433\u043e')),
                ('data', models.TextField(blank=True, null=True, verbose_name='\u0414\u0430\u043d\u043d\u044b\u0435')),
            ],
        ),
    ]
