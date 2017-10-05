# coding=utf-8
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.forms import ModelForm, Form
from students.model.base import Lecture, LabTask, Task, Course, Group, Resolution, Medal
from students.model.blog import Article


class LectureForm(ModelForm):

    class Meta:
        model = Lecture
        exclude = ['course']


class ArticleForm(ModelForm):
    preview = forms.CharField(widget=CKEditorUploadingWidget(config_name="article"), label=u"Превью", help_text=u"Эта часть будет отображаться в списке")
    body = forms.CharField(widget=CKEditorUploadingWidget(config_name="article"), label=u"Текст", help_text=u"Эта часть будет дополнением для превью")

    class Meta:
        model = Article
        exclude = ['course', 'author', 'viewed', 'viewed_mobile']


class CourseForm(ModelForm):

    class Meta:
        model = Course
        exclude = ['teachers']


class CheckResolutionForm(Form):
    comment = forms.CharField(widget=CKEditorUploadingWidget(config_name="default"), label=u"Комментарий", required=False)
    mark = forms.IntegerField(label=u"Баллы", required=True)
    medal = forms.ModelChoiceField(queryset=Medal.objects.all(), label=u"Медаль", required=False)


class SelectGroupForm(Form):
    group = forms.ModelChoiceField(Group.objects.all(), label=u"Группа")


class GroupForm(ModelForm):

    class Meta:
        model = Group
        exclude = ['courses']


class LabTaskForm(ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget(config_name="long"), label=u"Текст")
    field_order = ['title', 'short_name', 'body', 'created_at', 'deadline', 'active', 'important']

    def __init__(self, data=None, files=None, instance=None):
        initial = {}
        if instance:
            initial['created_at'] = instance.created_at.strftime("%d.%m.%Y")
            initial['deadline'] = instance.deadline.strftime("%d.%m.%Y")
        super(LabTaskForm, self).__init__(data=data, files=files, instance=instance, initial=initial)

    class Meta:
        model = LabTask
        exclude = ['course', 'number', 'color']


class TaskForm(ModelForm):
    field_order = ['title', 'short_name', 'body', 'created_at', 'active', 'important']

    def __init__(self, data=None, files=None, instance=None):
        initial = {}
        if instance:
            initial['created_at'] = instance.created_at.strftime("%d.%m.%Y")
        super(TaskForm, self).__init__(data=data, files=files, instance=instance, initial=initial)

    class Meta:
        model = Task
        exclude = ['course', 'color']
