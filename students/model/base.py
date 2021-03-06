# coding=utf-8
from hashlib import md5

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.utils import timesince
from django.utils.translation import ugettext as _
from slugify import slugify

from image.color import random_bright_color
from image.processing import image_is_big, make_image_small
from students.model.checks import *
from students.model.extra import *
from students.utils.slugs import my_unique_slugify


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

    def to_dict(self):
        return {
            'name': self.user.get_full_name(),
            'avatar': self.avatar_url(),
            'email': self.user.email,
            'id': self.user.id,
        }

    def save(self, **kwargs):
        super(Teacher, self).save(**kwargs)
        if self.avatar.name and image_is_big(self.avatar.name):
            self.avatar.name = make_image_small(self.avatar.name)
        self.color = random_bright_color()
        return super(Teacher, self).save(**kwargs)

    class Meta:
        verbose_name = u"Преподаватель"
        verbose_name_plural = u"Преподаватели"


class University(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"Название"))
    description = models.TextField(verbose_name=_(u"Описание"), null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name=_(u"Местоположение"), null=True, blank=True)

    def __unicode__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"Название"))
    description = models.TextField(verbose_name=_(u"Описание"), null=True, blank=True)
    university = models.ForeignKey(University, verbose_name=_(u"Университет"))
    teachers = models.ManyToManyField(Teacher, related_name="departments", blank=True, verbose_name=_(u"Преподаватели"))

    def __unicode__(self):
        return u"%s: %s" % (self.university, self.name)


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u"Название"))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_(u"Ссылка"), null=True, blank=True)

    def public_articles(self):
        from students.model.blog import Article
        return Article.objects.filter(published=True, private=False, course__subject=self)

    def all_articles(self):
        from students.model.blog import Article
        return Article.objects.filter(published=True, course__subject=self)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = my_unique_slugify(Subject, self.name)
        return super(Subject, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"Предметы"
        verbose_name = u"Предмет"


class Course(models.Model):
    SEMESTER_CHOICES = (
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
    archived = models.BooleanField(default=False, verbose_name=_(u"Завершен"))
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=u"Предмет")

    def __unicode__(self):
        return unicode(self.name) + u" ("+self.get_semester_display()+u", "+str(self.year)+u")"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'year': self.year,
            'semester': self.get_semester_display(),
            'teachers': [t.to_dict() for t in self.teachers.all()]
        }

    def active_tasks(self):
        return self.tasks.filter(active=True).order_by("created_at").all()

    def all_tasks(self):
        return self.tasks.order_by("created_at").all()

    def active_labtasks(self):
        return self.tasks.instance_of(LabTask).filter(active=True).order_by("created_at").all()

    def all_labtasks(self):
        return self.tasks.instance_of(LabTask).order_by("created_at").all()

    def non_labtasks(self):
        return self.tasks.not_instance_of(LabTask).order_by("created_at").all()

    def active_articles(self):
        return self.articles.filter(published=True).order_by("-datetime")

    @property
    def extra_students(self):
        return map(lambda es: es.student, self.extra_students_rel.all())

    class Meta:
        verbose_name = u"Курс"
        verbose_name_plural = u"Курсы"
        ordering = ["-id"]

    def groups_with_extra(self):
        groups = list(self.groups.all())
        extra_group = GroupMock(u"Дополнительная группа", self, self.extra_students)
        groups.append(extra_group)
        return groups


class OrderedModel(models.Model):
    order = models.FloatField(default=0, verbose_name=_(u"Порядок"))

    def save(self, *args, **kwargs):
        if self.order == 0:
            if self.__class__.objects.count() > 0:
                self.order = self.__class__.objects.all().last().order + 0.1
            else:
                self.order = 0.1
        return super(OrderedModel, self).save(*args, **kwargs)

    def up(self):
        prevs = self.__class__.objects.filter(order__lt=self.order)
        if prevs.count() > 0:
            previous = prevs.last()
            self.order, previous.order = previous.order, self.order
            self.save()
            previous.save()

    def down(self):
        nexts = self.__class__.objects.filter(order__gt=self.order)
        if nexts.count() > 0:
            next = nexts.first()
            self.order, next.order = next.order, self.order
            self.save()
            next.save()

    class Meta:
        ordering = ['order']
        abstract = True


class MustKnowGroup(OrderedModel):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name="must_know_groups")
    name = models.CharField(max_length=100, verbose_name=_(u"Группа знаний"))

    def __unicode__(self):
        return self.name

    def up(self):
        prevs = MustKnowGroup.objects.filter(order__lt=self.order, course=self.course)
        if prevs.count() > 0:
            previous = prevs.last()
            self.order, previous.order = previous.order, self.order
            self.save()
            previous.save()

    def down(self):
        nexts = MustKnowGroup.objects.filter(order__gt=self.order, course=self.course)
        if nexts.count() > 0:
            next = nexts.first()
            self.order, next.order = next.order, self.order
            self.save()
            next.save()

    class Meta:
        verbose_name = u"Группа знаний курса"
        verbose_name_plural = u"Группы знаний курса"
        ordering = ['order']


class MustKnow(OrderedModel):
    group = models.ForeignKey(MustKnowGroup, verbose_name=_(u"Группа"), related_name="items")
    text = models.CharField(max_length=255, verbose_name=_(u"Что должен знать студент?"))

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = u"То, что должен знать студент"
        verbose_name_plural = u"То, что должен знать студент"
        ordering = ['order']

    def up(self):
        prevs = MustKnow.objects.filter(order__lt=self.order, group=self.group)
        if prevs.count() > 0:
            previous = prevs.last()
            self.order, previous.order = previous.order, self.order
            self.save()
            previous.save()

    def down(self):
        nexts = MustKnow.objects.filter(order__gt=self.order, group=self.group)
        if nexts.count() > 0:
            next = nexts.first()
            self.order, next.order = next.order, self.order
            self.save()
            next.save()


class AlreadyKnow(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_(u"Пользователь"), related_name="i_know")
    datetime = models.DateTimeField(auto_now=True, verbose_name=_(u"Время"))
    must_know = models.ForeignKey(MustKnow, null=True, blank=True)

    def __unicode__(self):
        return self.must_know.text

    class Meta:
        verbose_name = u"Студент уже знает"
        verbose_name_plural = u"То, что студент уже знает"


class Lecture(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name='lectures')
    title = models.CharField(max_length=255, verbose_name=_(u"Тема"), null=True, blank=True)
    body = RichTextField(verbose_name=_(u"Текст"), config_name="long", null=True, blank=True)
    pptx = models.FileField(verbose_name=_(u"Презентация"), null=True, blank=True)
    url = models.URLField(verbose_name=_(u"Ссылка на материал"), null=True, blank=True)
    copy_from = models.ForeignKey("self", verbose_name=u"Копия лекции", null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name="copies")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.title and self.copy_from:
            self.title = self.copy_from.title
        if self.copy_from:
            assert self.id != self.copy_from_id
        return super(Lecture, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.copies.count() > 0:
            new_original = self.copies.all()[0]
            if not new_original.body:
                new_original.body = self.body
            if not new_original.pptx.name:
                new_original.pptx.name = self.pptx.name
            if not new_original.url:
                new_original.url = self.url
            new_original.save()

            for copy in self.copies.all()[1:]:
                copy.copy_from = new_original
                copy.save()
        return super(Lecture, self).delete(using, keep_parents)

    def __unicode__(self):
        return unicode(self.title)

    def to_dict(self):
        return {
            'id': self.id,
            'course': self.course.name,
            'title': self.title,
            'body': self.copy_from.body if not self.body and self.copy_from else self.body,
            'file': self.copy_from.pptx.url if not self.pptx.name and self.copy_from else self.pptx.url,
            'url': self.copy_from.url if not self.url and self.copy_from else self.url
        }

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
    max_score = models.FloatField(verbose_name=_(u"Мак. баллов"), default=30)
    quiz = models.ManyToManyField('Quiz', verbose_name=_(u"Добавить тесты"), blank=True)
    quiz_count = models.IntegerField(verbose_name=_(u"Кол-во вопросов в тесте"), default=15)
    quiz_attempts = models.IntegerField(verbose_name=_(u"Кол-во попыток в тесте"), default=1)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.title[:5]
        return super(Task, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)

    def reversed_resolutions(self):
        return self.resolutions.all().order_by("-datetime")

    def to_dict(self):
        return {
            'id': self.id,
            'created': self.created_at.strftime("%d.%m.%Y %H:%M"),
            'course': self.course.name,
            'active': self.active,
            'title': self.title,
            'short_name': self.short_name,
            'body': self.body,
            'color': self.color,
            'important': self.important
        }

    class Meta:
        verbose_name = u"Задание"
        verbose_name_plural = u"Задания"


class LabTask(Task):
    number = models.IntegerField(verbose_name=u"Номер", default=0)
    deadline = models.DateTimeField(verbose_name=_(u"Крайний срок сдачи"))
    attachment = models.FileField(verbose_name=_(u"Приложение"), null=True, blank=True)

    def to_dict(self):
        data = super(LabTask, self).to_dict()
        data['number'] = self.number
        data['deadline'] = self.deadline.strftime("%d.%m.%Y %H:%M")
        return data

    class Meta:
        verbose_name = u"Лабораторная работа"
        verbose_name_plural = u"Лабораторные работы"


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u"Название"))
    courses = models.ManyToManyField(Course, blank=True, verbose_name=_(u"Курсы"), related_name="groups")
    department = models.ForeignKey(Department, verbose_name=_(u"Факультет"), null=True, blank=True)

    def active_students(self):
        return self.students.filter(active=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u"Группа"
        verbose_name_plural = u"Группы"
        ordering = ["-id"]


class ModelManagerMock(object):
    def __iter__(self):
        return iter(self.data)

    def __init__(self, data):
        self.data = data

    def all(self):
        return self.data

    def count(self):
        return len(self.data)


class GroupMock:
    def __init__(self, name, course, students):
        self.id = 0
        self.name = name
        self.courses = ModelManagerMock([course])
        self.students = ModelManagerMock(students)

    def active_students(self):
        return self.students


class Student(models.Model, AvatarMixin):
    avatar = models.FileField(verbose_name=_(u"Аватар"), null=True, blank=True, upload_to="avatars/")
    user = models.OneToOneField(get_user_model(), related_name="student")
    group = models.ForeignKey(Group, verbose_name=_(u"Группа"), related_name="students")
    color = models.CharField(max_length=20, verbose_name=_(u"Цвет"), default="#ff1493")
    active = models.BooleanField(default=True, verbose_name=u"Активен")

    def __unicode__(self):
        return self.user.get_full_name() + u" " + unicode(self.group)

    @property
    def name(self):
        return self.user.get_full_name()

    def get_short_name(self):
        return self.user.email[:self.user.email.index("@")]

    @property
    def courses(self):
        return list(self.group.courses.all()) + map(lambda ec: ec.course, list(self.extra_courses_rel.all()))

    def save(self, **kwargs):
        super(Student, self).save(**kwargs)
        if self.avatar.name and image_is_big(self.avatar.name):
            self.avatar.name = make_image_small(self.avatar.name)
        self.color = random_bright_color()
        return super(Student, self).save(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.user.get_full_name(),
            'last_seen': u"Был(а): " + (
            timesince.timesince(self.user.last_seen) + u" назад" if self.user.last_seen else u"Никогда")
        }

    class Meta:
        verbose_name = u"Студент"
        verbose_name_plural = u"Студенты"
        ordering = ['user__fullname']


class Todo(models.Model):
    text = models.CharField(verbose_name=_(u"Текст"), max_length=255)
    user = models.ForeignKey(get_user_model(), verbose_name=_(u"Пользователь"), related_name="todos")
    datetime = models.DateTimeField(auto_now=True, verbose_name=_(u"Время"))
    color = models.CharField(verbose_name=_(u"Цвет"), max_length=20, default="#FFFFFF")
    done = models.BooleanField(verbose_name=_(u"Достигнуто"), default=False)


class Point(models.Model):
    reason = models.CharField(verbose_name=_(u"За что"), max_length=255)
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name="points", on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Время"))
    points = models.IntegerField(default=0, verbose_name=_(u"Очки"))
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = u"Очки опыта"
        verbose_name_plural = u"Очки опыта"


class ExtraStudent(models.Model):
    student = models.ForeignKey(Student, verbose_name=u"Студент", related_name="extra_courses_rel")
    course = models.ForeignKey(Course, verbose_name=u"Курс", related_name="extra_students_rel")

    def __unicode__(self):
        return u"%s: %s" % (self.course.name, self.student)

    class Meta:
        verbose_name = u"Студент записавшийся не на свой курс"
        verbose_name_plural = u"Студенты записавшиеся не на свои курсы"


class Resolution(PolymorphicModel):
    comment = RichTextField(verbose_name=_(u"Комментарий"), config_name="default", null=True, blank=True)
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name='resolutions')
    task = models.ForeignKey(Task, verbose_name=_(u"Задание"), related_name='resolutions')
    datetime = models.DateTimeField(verbose_name=_(u"Время"), auto_now_add=True, null=True)
    mark = models.IntegerField(verbose_name=_(u"Баллы"), default=0)

    def __unicode__(self):
        return u"Решение '%s' от %s" % (self.task, unicode(self.student))

    def to_dict(self):
        return {
            'comment': self.comment,
            'student': self.student.user.get_full_name(),
            'task': self.task.short_name,
            'datetime': self.datetime.strftime("%d.%m.%Y %H:%M"),
            'mark': self.mark
        }

    class Meta:
        verbose_name = u"Решение"
        verbose_name_plural = u"Решения"


class FileResolution(Resolution):
    file = models.FileField(verbose_name=_(u"Файл"))
    index_file = models.CharField(verbose_name=_(u"Файл index.html"), null=True, blank=True, max_length=500)

    def to_dict(self):
        data = super(FileResolution, self).to_dict()
        data['index_file'] = self.index_file
        return data

    class Meta:
        verbose_name = u"Решение с файлом"
        verbose_name_plural = u"Решения с файлом"


class HomeWorkSolution(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name="homeworks")
    student = models.ForeignKey(Student, verbose_name=_(u"Студент"), related_name='homeworks')
    task = models.CharField(max_length=255, verbose_name=_(u"Задание"), help_text=_(u"Какое было задание?"))
    comment = RichTextField(verbose_name=_(u"Комментарий"), config_name="default",
                            help_text=u"Опишите как вы решили, что использовали и т.п.")
    datetime = models.DateTimeField(verbose_name=_(u"Время"), auto_now_add=True)
    file = models.FileField(verbose_name=_(u"Файл"))
    viewed = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"Решение ДЗ"
        verbose_name_plural = u"Решения ДЗ"


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


class LastReadMessage(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Чат какого курса"))
    user = models.ForeignKey(get_user_model(), verbose_name=_(u"Пользователь"), null=True, on_delete=models.SET_NULL)
    last_read_message_id = models.IntegerField(blank=True, verbose_name=_(u"Последнее прочитанное сообщение"),
                                               default=0)

    @staticmethod
    def register_last_message(course, user, last_message_id):
        register = LastReadMessage(course=course, user=user)
        try:
            register = LastReadMessage.objects.get(user=user, course=course)
        except:
            pass
        register.last_read_message_id = last_message_id
        register.save()

    @staticmethod
    def get_unread_messages_count(course, user):
        last_read_message_id = 0
        if LastReadMessage.objects.filter(user=user, course=course).count() > 0:
            last_read_message_id = LastReadMessage.objects.get(user=user, course=course).last_read_message_id
        return ChatMessage.objects.filter(course=course, pk__gt=last_read_message_id).count()


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
        return unicode(self.student) + u" " + unicode(self.medal)

    def to_dict(self):
        return {
            'name': self.medal.name,
            'image': self.medal.image.url,
        }

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


class UserActivity(models.Model):
    month = models.IntegerField(verbose_name=u"Месяц")
    year = models.IntegerField(verbose_name=u"Год")
    user = models.ForeignKey(get_user_model(), verbose_name=u"Пользователь")
    activity = models.CharField(verbose_name=u"Активность", max_length=1000)

    @staticmethod
    def get_for_month(user, year, month):
        try:
            return UserActivity.objects.get(user=user, month=month, year=year)
        except:
            activity = UserActivity(user=user, month=month, year=year)
            activity.activity = "0" * 31 * 24
            return activity


class Literature(models.Model):
    course = models.ForeignKey(Course, verbose_name=_(u"Курс"), related_name="literature")
    name = models.CharField(max_length=500, verbose_name=_(u"Название"))
    author = models.CharField(max_length=255, verbose_name=_(u"Автор"), null=True, blank=True)
    link = models.URLField(verbose_name=_(u"Ссылка"), null=True, blank=True)
    file = models.FileField(verbose_name=_(u"Файл"), null=True, blank=True)

    class Meta:
        verbose_name = u"Литература"
        verbose_name_plural = u"Литература"


class Quiz(Model):
    name = models.CharField(verbose_name=u"Название", max_length=255)
    subject = models.ForeignKey(Subject, null=True, blank=True, verbose_name=u"Предмет", on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class QuizQuestion(Model):
    CHOICES = [
        ['single', "Один ответ"],
        ['multiple', "Много ответов"],
        ['text', "Текст"],
        ['bigtext', "Большой текст"],
        ['task', "Задачка с правильным ответом"],
    ]
    text = models.TextField(verbose_name=u"Вопрос")
    quiz = models.ForeignKey(Quiz, verbose_name=u"Тест", related_name="questions")
    type = models.CharField(max_length=20, verbose_name=u"Тип", choices=CHOICES)

    def random_answers(self):
        return self.answers.all().order_by("?")

    def check_answer(self, answer_ids):
        right_answers = map(lambda s: s[0], self.answers.filter(type='right').values_list('id'))
        wrong_answers = map(lambda s: s[0], self.answers.filter(type='wrong').values_list('id'))
        for right in right_answers:
            if right not in answer_ids:
                return False
        for wrong in wrong_answers:
            if wrong in answer_ids:
                return False
        return True

    def check_text_answer(self, answer):
        if self.type == "task":
            return self.answers.filter(type='right', text=answer).exists()
        return True if answer else False

    def __unicode__(self):
        return self.text[:30]


class QuizAnswer(Model):
    CHOICES = [
        ['wrong', u'Неправильный ответ'],
        ['right', u'Правильный ответ'],
        ['optional', u'Необязательный ответ'],
    ]
    question = models.ForeignKey(QuizQuestion, verbose_name=u"Вопрос", related_name="answers")
    text = models.CharField(max_length=255, verbose_name=u"Ответ")
    type = models.CharField(verbose_name=u"Тип", max_length=20, choices=CHOICES, default='wrong')


class QuizResult(Model):
    student = models.ForeignKey(get_user_model(), verbose_name=u"Пользователь")
    task = models.ForeignKey(Task, verbose_name=u"Задание", null=True, blank=True)
    result = models.FloatField(verbose_name=u"Оценка")
    answer = models.TextField(verbose_name=u"Ответы", null=True)
    comment = models.TextField(verbose_name=u"Комментарий препода", null=True, blank=True)
    checked = models.BooleanField(verbose_name=u"Проверен", default=False)
    attempts = models.IntegerField(verbose_name=u"Кол-во попыток", default=0)
