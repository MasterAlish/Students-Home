# coding=utf-8

from django.db import models
from django.db.models import Model


class Feedback(Model):
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    text = models.CharField(max_length=1000, verbose_name=u'Текст')
    mobile = models.BooleanField(default=False, verbose_name=u"С мобильного")
    data = models.TextField(null=True, blank=True, verbose_name=u"Данные")


class AppAd(Model):
    title = models.CharField(max_length=255, verbose_name=u"Название")
    subtitle = models.CharField(max_length=255, verbose_name=u"Краткое описание")
    url = models.URLField(verbose_name=u"Ссылка")
    icon = models.FileField(upload_to="icons", verbose_name=u"Иконка")

    @staticmethod
    def random():
        try:
            return AppAd.objects.order_by("?").first()
        except:
            return None

    class Meta:
        verbose_name_plural = u"Реклама приложений"
        verbose_name = u"Реклама приложения"
