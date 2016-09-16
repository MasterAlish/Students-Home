# coding=utf-8
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="teacher")

    def __unicode__(self):
        return unicode(self.user)


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name=u"Название курса")
    description = RichTextField(verbose_name=u"Описание", null=True, blank=True, config_name="short")
    teachers = models.ManyToManyField(Teacher, blank=True, verbose_name=u"Преподаватели", related_name="courses")
    year = models.IntegerField(verbose_name=u"Год", default=2016)
    semester = models.CharField(max_length=10, verbose_name=u"Семестр", choices=(('fall', u'Осенний'), ('spring', u"Весенний")))

    def __unicode__(self):
        return unicode(self.name)


class Lecture(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"Курс", related_name='lectures')
    title = models.CharField(max_length=255, verbose_name=u"Тема")
    body = RichTextField(verbose_name=u"Текст", config_name="long")
    pptx = models.FileField(verbose_name=u"Презентация")

    def __unicode__(self):
        return unicode(self.title)


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"Название")
    courses = models.ManyToManyField(Course, blank=True, verbose_name=u"Курсы")

    def __unicode__(self):
        return unicode(self.name)


class Student(models.Model):
    avatar = models.FileField(verbose_name=u"Аватар")
    user = models.OneToOneField(get_user_model(), related_name="student")
    group = models.ForeignKey(Group, verbose_name=u"Группа", related_name="students")

    def __unicode__(self):
        return unicode(self.user)+u" "+unicode(self.group)