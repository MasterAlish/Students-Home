# coding=utf-8
from hashlib import md5
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from polymorphic.models import PolymorphicModel

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

    class Meta:
        verbose_name = u"Преподаватель"
        verbose_name_plural = u"Преподаватели"


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

    def active_tasks(self):
        return self.tasks.filter(active=True).order_by("created_at").all()

    def all_tasks(self):
        return self.tasks.order_by("created_at").all()

    def active_labtasks(self):
        return self.tasks.instance_of(LabTask).filter(active=True).order_by("created_at").all()

    def all_labtasks(self):
        return self.tasks.instance_of(LabTask).order_by("created_at").all()

    class Meta:
        verbose_name = u"Курс"
        verbose_name_plural = u"Курсы"


class Lecture(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name='lectures')
    title = models.CharField(max_length=255, verbose_name=_(u"Тема"))
    body = RichTextField(verbose_name=_(u"Текст"), config_name="long")
    pptx = models.FileField(verbose_name=_(u"Презентация"))

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = u"Лекция"
        verbose_name_plural = u"Лекции"


class Task(PolymorphicModel):
    created_at = models.DateTimeField(verbose_name=u"Дата объявления")
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name='tasks')
    active = models.BooleanField(verbose_name=_(u"Активен"), default=True)
    title = models.CharField(max_length=255, verbose_name=_(u"Тема"))
    short_name = models.CharField(max_length=255, verbose_name=_(u"Краткое название"), blank=True, null=True)
    body = RichTextField(verbose_name=_(u"Текст"), config_name="long")
    color = models.CharField(verbose_name=_(u"Цвет"), max_length=20, default="#dff0d8")
    important = models.BooleanField(verbose_name=_(u"Важное"), default=False)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.title[:5]
        return super(Task, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = u"Задание"
        verbose_name_plural = u"Задания"


class LabTask(Task):
    number = models.IntegerField(verbose_name=u"Номер", default=0)
    deadline = models.DateTimeField(verbose_name=_(u"Крайний срок сдачи"))

    class Meta:
        verbose_name = u"Лабораторная работа"
        verbose_name_plural = u"Лабораторные работы"


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u"Название"))
    courses = models.ManyToManyField(Course, blank=True, verbose_name=_(u"Курсы"), related_name="groups")

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u"Группа"
        verbose_name_plural = u"Группы"


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

    def get_short_name(self):
        return self.user.email[:self.user.email.index("@")]

    def save(self, **kwargs):
        super(Student, self).save(**kwargs)
        if self.avatar.name and image_is_big(self.avatar.name):
            self.avatar.name = make_image_small(self.avatar.name)
        self.color = random_bright_color()
        return super(Student, self).save(**kwargs)

    class Meta:
        verbose_name = u"Студент"
        verbose_name_plural = u"Студенты"


class Resolution(PolymorphicModel):
    comment = RichTextField(verbose_name=_(u"Комментарий"), config_name="default", null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name='resolutions')
    task = models.ForeignKey(Task, verbose_name=_(u"Задание"), related_name='resolutions')
    datetime = models.DateTimeField(verbose_name=_(u"Время"), auto_now_add=True, null=True)
    mark = models.IntegerField(verbose_name=_(u"Баллы"), default=0)

    def __unicode__(self):
        return u"Решение '%s' от %s" % (self.task, unicode(self.student))

    class Meta:
        verbose_name = u"Решение"
        verbose_name_plural = u"Решения"


class FileResolution(Resolution):
    file = models.FileField(verbose_name=_(u"Файл"))

    class Meta:
        verbose_name = u"Решение с файлом"
        verbose_name_plural = u"Решения с файлом"


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

    class Meta:
        verbose_name = u"Сообщение чата"
        verbose_name_plural = u"Сообщения чата"


class Medal(models.Model):
    image = models.ImageField(verbose_name=_(u"Изображение"))
    name = models.CharField(max_length=255, verbose_name=_(u"Название"))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u"Вид медали"
        verbose_name_plural = u"Виды медалей"


class StudentMedal(models.Model):
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name="medals")
    medal = models.ForeignKey(Medal, verbose_name=_(u"Медаль"), related_name="medals")
    course = models.ForeignKey(Course, verbose_name=_(u"За курс"), null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return unicode(self.student) + u" "+unicode(self.medal)

    class Meta:
        verbose_name = u"Медаль"
        verbose_name_plural = u"Медали"


class Mail(models.Model):
    recipients = models.TextField(verbose_name=u"К кому(json array)")
    body_html = models.TextField(verbose_name=u"Тело сообщения (html)")
    body_txt = models.TextField(verbose_name=u"Тело сообщения (txt)")
    subject = models.CharField(max_length=255, verbose_name=u"Тема")

    class Meta:
        verbose_name = u"Почта"
        verbose_name_plural = u"Почты"
