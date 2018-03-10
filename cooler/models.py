# coding=utf-8
from ckeditor.fields import RichTextField
from django.db import models

from students.models import MyUser
from students.utils.slugs import my_unique_slugify


class CoolSnippet(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=u"Время")
    user = models.ForeignKey(MyUser, verbose_name=u"Пользователь")
    code = models.TextField(verbose_name=u"Код")
    task = models.CharField(max_length=255, verbose_name=u"Задача")

    @property
    def username(self):
        return self.user.get_full_name()


class Puzzle(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=u"Добавлен")
    added = models.ForeignKey(MyUser, verbose_name=u"Добавил")
    title = models.CharField(max_length=255, verbose_name=u"Заголовок")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name=u"Ссылка")
    body = RichTextField(config_name="article", verbose_name=u"Текст")
    viewed = models.IntegerField(default=0, verbose_name=u"Просмотрено")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = my_unique_slugify(Puzzle, self.title)
        return super(Puzzle, self).save(*args, **kwargs)
