# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-08 13:09
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0036_myuser_grouvi_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['-id'], 'verbose_name': '\u041a\u0443\u0440\u0441', 'verbose_name_plural': '\u041a\u0443\u0440\u0441\u044b'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-id'], 'verbose_name': '\u0413\u0440\u0443\u043f\u043f\u0430', 'verbose_name_plural': '\u0413\u0440\u0443\u043f\u043f\u044b'},
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='grouvi_user_id',
        ),
        migrations.AddField(
            model_name='lecture',
            name='copy_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Lecture', verbose_name='\u041a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441 \u043b\u0435\u043a\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='\u0422\u0435\u043a\u0441\u0442'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0422\u0435\u043c\u0430'),
        ),
    ]
