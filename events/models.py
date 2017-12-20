# coding=utf-8
from django.db import models


class Event(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=u"Время")
    name = models.CharField(max_length=255, verbose_name=u"Событие")
    details = models.CharField(max_length=255, verbose_name=u"Детали", null=True, blank=True)
    domain = models.CharField(max_length=255, verbose_name=u"Домен", null=True, blank=True)
