# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-03 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0039_auto_20171020_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='\u041e\u0442\u0432\u0435\u0442')),
                ('type', models.CharField(choices=[[b'wrong', '\u041d\u0435\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 \u043e\u0442\u0432\u0435\u0442'], [b'right', '\u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 \u043e\u0442\u0432\u0435\u0442'], [b'optional', '\u041d\u0435\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043e\u0442\u0432\u0435\u0442']], default=b'wrong', max_length=20, verbose_name='\u0422\u0438\u043f')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441')),
                ('type', models.CharField(choices=[[b'single', b'\xd0\x9e\xd0\xb4\xd0\xb8\xd0\xbd \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82'], [b'multiple', b'\xd0\x9c\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd0\xbe\xd0\xb2'], [b'text', b'\xd0\xa2\xd0\xb5\xd0\xba\xd1\x81\xd1\x82'], [b'bigtext', b'\xd0\x91\xd0\xbe\xd0\xbb\xd1\x8c\xd1\x88\xd0\xbe\xd0\xb9 \xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82'], [b'task', b'\xd0\x97\xd0\xb0\xd0\xb4\xd0\xb0\xd1\x87\xd0\xba\xd0\xb0 \xd1\x81 \xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xbc \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd0\xbe\xd0\xbc']], max_length=20, verbose_name='\u0422\u0438\u043f')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='students.Quiz', verbose_name='\u0422\u0435\u0441\u0442')),
            ],
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.FloatField(verbose_name='\u041e\u0446\u0435\u043d\u043a\u0430')),
                ('answer', models.TextField(null=True, verbose_name='\u041e\u0442\u0432\u0435\u0442\u044b')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043f\u0440\u0435\u043f\u043e\u0434\u0430')),
                ('checked', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0432\u0435\u0440\u0435\u043d')),
                ('attempts', models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u041f\u0440\u0435\u0434\u043c\u0435\u0442',
                'verbose_name_plural': '\u041f\u0440\u0435\u0434\u043c\u0435\u0442\u044b',
            },
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['user__fullname'], 'verbose_name': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442', 'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442\u044b'},
        ),
        migrations.AddField(
            model_name='task',
            name='max_score',
            field=models.FloatField(default=30, verbose_name='\u041c\u0430\u043a. \u0431\u0430\u043b\u043b\u043e\u0432'),
        ),
        migrations.AddField(
            model_name='task',
            name='quiz_attempts',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a \u0432 \u0442\u0435\u0441\u0442\u0435'),
        ),
        migrations.AddField(
            model_name='task',
            name='quiz_count',
            field=models.IntegerField(default=15, verbose_name='\u041a\u043e\u043b-\u0432\u043e \u0432\u043e\u043f\u0440\u043e\u0441\u043e\u0432 \u0432 \u0442\u0435\u0441\u0442\u0435'),
        ),
        migrations.AddField(
            model_name='quizresult',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Task', verbose_name='\u0417\u0430\u0434\u0430\u043d\u0438\u0435'),
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='students.QuizQuestion', verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Subject', verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Subject', verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442'),
        ),
        migrations.AddField(
            model_name='task',
            name='quiz',
            field=models.ManyToManyField(blank=True, to='students.Quiz', verbose_name='\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0442\u0435\u0441\u0442\u044b'),
        ),
    ]
