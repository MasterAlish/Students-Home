# coding=utf-8
from datetime import datetime
from django.db import models
from django.db.models import Model


class Feedback(Model):
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    text = models.CharField(max_length=1000, verbose_name=u'Текст')
    mobile = models.BooleanField(default=False, verbose_name=u"С мобильного")
    data = models.TextField(null=True, blank=True, verbose_name=u"Данные")