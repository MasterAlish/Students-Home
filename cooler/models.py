# coding=utf-8
from django.db import models

from students.models import MyUser


class CoolSnippet(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=u"Время")
    user = models.ForeignKey(MyUser, verbose_name=u"Пользователь")
    code = models.TextField(verbose_name=u"Код")
    task = models.CharField(max_length=255, verbose_name=u"Задача")

    @property
    def username(self):
        return self.user.get_full_name()

