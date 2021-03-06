# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-09 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0037_auto_20170908_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Literature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('author', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0410\u0432\u0442\u043e\u0440')),
                ('link', models.URLField(blank=True, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430')),
                ('file', models.FileField(blank=True, null=True, upload_to=b'', verbose_name='\u0424\u0430\u0439\u043b')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Course', verbose_name='\u041a\u0443\u0440\u0441')),
            ],
            options={
                'verbose_name': '\u041b\u0438\u0442\u0435\u0440\u0430\u0442\u0443\u0440\u0430',
                'verbose_name_plural': '\u041b\u0438\u0442\u0435\u0440\u0430\u0442\u0443\u0440\u0430',
            },
        ),
        migrations.AlterField(
            model_name='homeworksolution',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='students.Course', verbose_name='\u041a\u0443\u0440\u0441'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='copy_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='copies', to='students.Lecture', verbose_name='\u041a\u043e\u043f\u0438\u044f \u043b\u0435\u043a\u0446\u0438\u0438'),
        ),
    ]
