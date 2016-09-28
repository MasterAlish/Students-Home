# coding=utf-8
from hashlib import md5
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

from image.color import random_bright_color
from image.processing import image_is_big, make_image_small


class AvatarMixin:
    avatar = None
    user = None

    def avatar_url(self):
        if self.avatar.name:
            return self.avatar.url
        else:
            return "https://www.gravatar.com/avatar/%s?d=monsterid&s=256" % md5(self.user.email).hexdigest()


class Teacher(models.Model, AvatarMixin):
    avatar = models.FileField(verbose_name=_(u"Аватар"), upload_to="avatars/", null=True, blank=True)
    user = models.OneToOneField(get_user_model(), related_name="teacher")
    color = models.CharField(max_length=20, verbose_name=_(u"Цвет"), default="#f44336")

    def __unicode__(self):
        return unicode(self.user)

    def save(self, **kwargs):
        super(Teacher, self).save(**kwargs)
        if self.avatar.name and image_is_big(self.avatar.name):
            self.avatar.name = make_image_small(self.avatar.name)
        self.color = random_bright_color()
        return super(Teacher, self).save(**kwargs)


class Course(models.Model):
    SEMESTER_CHOICES=(
        ('spring', _(u"Весенний")),
        ('summer', _(u"Летний")),
        ('fall', _(u'Осенний')),
        ('winter', _(u"Зимний"))
    )
    name = models.CharField(max_length=255, verbose_name=_(u"Название курса"))
    description = RichTextField(verbose_name=_(u"Описание"), null=True, blank=True, config_name="short")
    teachers = models.ManyToManyField(Teacher, blank=True, verbose_name=_(u"Преподаватели"), related_name="courses")
    year = models.IntegerField(verbose_name=_(u"Год"), default=2016)
    semester = models.CharField(max_length=10, verbose_name=_(u"Семестр"), choices=SEMESTER_CHOICES)

    def __unicode__(self):
        return unicode(self.name)

    def active_labworks(self):
        return self.labworks.filter(active=True).all()


class Lecture(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name='lectures')
    title = models.CharField(max_length=255, verbose_name=_(u"Тема"))
    body = RichTextField(verbose_name=_(u"Текст"), config_name="long")
    pptx = models.FileField(verbose_name=_(u"Презентация"))

    def __unicode__(self):
        return unicode(self.title)


class LabWork(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name='labworks')
    title = models.CharField(max_length=255, verbose_name=_(u"Тема"))
    body = RichTextField(verbose_name=_(u"Текст"), config_name="long")
    deadline = models.DateTimeField(verbose_name=_(u"Крайний срок сдачи"))
    active = models.BooleanField(verbose_name=_(u"Активен"), default=True)

    def __unicode__(self):
        return unicode(self.title)


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u"Название"))
    courses = models.ManyToManyField(Course, blank=True, verbose_name=_(u"Курсы"), related_name="groups")

    def __unicode__(self):
        return unicode(self.name)


class Student(models.Model, AvatarMixin):
    avatar = models.FileField(verbose_name=_(u"Аватар"), null=True, blank=True, upload_to="avatars/")
    user = models.OneToOneField(get_user_model(), related_name="student")
    group = models.ForeignKey(Group, verbose_name=_(u"Группа"), related_name="students")
    color = models.CharField(max_length=20, verbose_name=_(u"Цвет"), default="#ff1493")

    def __unicode__(self):
        return self.user.get_full_name()+u" "+unicode(self.group)

    @property
    def name(self):
        return self.user.get_full_name()

    def save(self, **kwargs):
        super(Student, self).save(**kwargs)
        if self.avatar.name and image_is_big(self.avatar.name):
            self.avatar.name = make_image_small(self.avatar.name)
        self.color = random_bright_color()
        return super(Student, self).save(**kwargs)


class Solution(models.Model):
    file = models.FileField(verbose_name=_(u"Файл"))
    comment = RichTextField(verbose_name=_(u"Комментарий"), config_name="default", null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name='solutions')
    labwork = models.ForeignKey(LabWork, verbose_name=_(u"Работа"), related_name='solutions')
    datetime = models.DateTimeField(verbose_name=_(u"Время"), auto_now_add=True, null=True)
    mark = models.IntegerField(verbose_name=_(u"Баллы"), default=0)

    def __unicode__(self):
        return u"Лаба от %s" % unicode(self.student)


class ChatMessage(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name="chats")
    user = models.ForeignKey(get_user_model(), verbose_name=_(u"Пользователь"), null=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(verbose_name=_(u"Время"), auto_now_add=True)
    body = models.CharField(max_length=1000, verbose_name=_(u"Сообщение"))

    def color(self):
        from students.view.common import is_student, is_teacher
        if is_student(self.user):
            return self.user.student.color
        if is_teacher(self.user):
            return self.user.teacher.color
        return "#00000"


class Medal(models.Model):
    image = models.ImageField(verbose_name=_(u"Изображение"))
    name = models.CharField(max_length=255, verbose_name=_(u"Название"))


class StudentMedal(models.Model):
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name="medals")
    medal = models.ForeignKey(Medal, verbose_name=_(u"Медаль"), related_name="medals")
    course = models.ForeignKey(Course, verbose_name=_(u"За курс"), null=True, blank=True, on_delete=models.SET_NULL)