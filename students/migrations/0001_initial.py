# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-15 11:29
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name=b'email address')),
                ('date_of_birth', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('phone', models.CharField(max_length=100, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430')),
                ('fullname', models.CharField(max_length=255, null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u0438\u043c\u044f')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043a\u0443\u0440\u0441\u0430')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('year', models.IntegerField(default=2016, verbose_name='\u0413\u043e\u0434')),
                ('semester', models.CharField(choices=[(b'fall', '\u041e\u0441\u0435\u043d\u043d\u0438\u0439'), (b'spring', '\u0412\u0435\u0441\u0435\u043d\u043d\u0438\u0439')], max_length=10, verbose_name='\u0421\u0435\u043c\u0435\u0441\u0442\u0440')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('courses', models.ManyToManyField(blank=True, to='students.Course', verbose_name='\u041a\u0443\u0440\u0441\u044b')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Group', verbose_name='\u0413\u0440\u0443\u043f\u043f\u0430')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, to='students.Teacher', verbose_name='\u041f\u0440\u0435\u043f\u043e\u0434\u0430\u0432\u0430\u0442\u0435\u043b\u0438'),
        ),
    ]
