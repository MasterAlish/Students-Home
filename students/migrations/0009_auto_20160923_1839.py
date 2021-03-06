# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 18:39
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f'),
        ),
        migrations.AddField(
            model_name='solution',
            name='mark',
            field=models.IntegerField(default=0, verbose_name='\u0411\u0430\u043b\u043b\u044b'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='comment',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='labwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='students.LabWork', verbose_name='\u0420\u0430\u0431\u043e\u0442\u0430'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='students.Student', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442'),
        ),
    ]
