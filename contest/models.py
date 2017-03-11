# coding=utf-8
from __future__ import unicode_literals

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from students.models import MyUser


class Problem(models.Model):
    title = models.CharField(max_length=255, verbose_name=_(u"Название"))
    body = RichTextField(verbose_name=_(u"Описание"), config_name='article')
    limits = RichTextField(verbose_name=_(u"Ограничения"), null=True, blank=True)
    acm_id = models.IntegerField(verbose_name=_(u"Номер задачи"))
    difficulty = models.IntegerField(verbose_name=_(u"Сложность"), default=0)
    url = models.CharField(max_length=500, verbose_name=_(u"Ссылка"))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Задача"
        verbose_name_plural = u"Задачи"


class Contestant(models.Model):
    judge_id = models.CharField(max_length=20, verbose_name=_(u"ACM Timus Judge ID"), primary_key=True)
    username = models.CharField(max_length=100, verbose_name=_(u"ACM username"))
    user = models.ForeignKey(MyUser, verbose_name=_(u"Пользователь"), related_name="contestant")
    url = models.CharField(max_length=500, verbose_name=_(u"Ссылка"), null=True, blank=True)

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = u"Участник"
        verbose_name_plural = u"Участники"


class ProblemSolution(models.Model):
    problem = models.ForeignKey(Problem, verbose_name=_(u"Задача"), on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, verbose_name=_(u"Участник"), on_delete=models.CASCADE)
    acm_id = models.IntegerField(verbose_name=_(u"Номер попытки"), null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Время"))
    check_result = models.CharField(max_length=100, verbose_name=_(u"Результат проверки"), null=True, blank=True)
    language = models.CharField(max_length=100, verbose_name=_(u"Язык"))
    test_number = models.IntegerField(verbose_name=_(u"Номер теста"), null=True, blank=True)
    time = models.CharField(max_length=20, verbose_name=_(u"Время работы"), null=True, blank=True)
    memory = models.CharField(max_length=20, verbose_name=_(u"Выделено памяти"), null=True, blank=True)
    body = models.TextField(verbose_name=_(u"Код"), null=True, blank=True)
    success = models.BooleanField(verbose_name=_(u"Решено"), default=False)
    checked = models.BooleanField(verbose_name=_(u"Проверено"), default=False)

    def __unicode__(self):
        return self.problem.title

    class Meta:
        verbose_name = u"Решение"
        verbose_name_plural = u"Решения"
