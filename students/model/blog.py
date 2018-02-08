# coding=utf-8
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models

from students.model.base import Course
from students.utils.slugs import my_unique_slugify


class Article(models.Model):
    title = models.CharField(max_length=1000, verbose_name=u"Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name=u"Ссылка", null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True, verbose_name=u"Курс", on_delete=models.SET_NULL, related_name="articles")
    author = models.ForeignKey(get_user_model(), verbose_name=u"Пользователь", null=True, on_delete=models.SET_NULL)
    preview = RichTextField(config_name="article", verbose_name=u"Превью", help_text=u"Эта часть будет отображаться в списке")
    body = RichTextField(config_name="article", verbose_name=u"Текст", help_text=u"Эта часть будет дополнением для превью")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата создания")
    published = models.BooleanField(default=True, verbose_name=u"Опубликован")
    viewed = models.IntegerField(default=0, verbose_name=u"Просмотрено")
    viewed_mobile = models.IntegerField(default=0, verbose_name=u"Просмотрено через приложение")
    private = models.BooleanField(verbose_name=u"Приватная статья", default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = my_unique_slugify(Article, self.title)
        return super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = u"Статьи"
        verbose_name = u"Статья"
        ordering = ['-datetime']