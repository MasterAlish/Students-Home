# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-29 08:36
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0023_myuser_last_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('preview', ckeditor.fields.RichTextField(help_text='\u042d\u0442\u0430 \u0447\u0430\u0441\u0442\u044c \u0431\u0443\u0434\u0435\u0442 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u044c\u0441\u044f \u0432 \u0441\u043f\u0438\u0441\u043a\u0435', verbose_name='\u041f\u0440\u0435\u0432\u044c\u044e')),
                ('body', ckeditor.fields.RichTextField(help_text='\u042d\u0442\u0430 \u0447\u0430\u0441\u0442\u044c \u0431\u0443\u0434\u0435\u0442 \u0434\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435\u043c \u0434\u043b\u044f \u043f\u0440\u0435\u0432\u044c\u044e', verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('published', models.BooleanField(default=True, verbose_name='\u041e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u043d')),
                ('viewed', models.IntegerField(default=0, verbose_name='\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u043d\u043e')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Course', verbose_name='\u041a\u0443\u0440\u0441')),
            ],
            options={
                'verbose_name': '\u0421\u0442\u0430\u0442\u044c\u044f',
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u044c\u0438',
            },
        ),
    ]