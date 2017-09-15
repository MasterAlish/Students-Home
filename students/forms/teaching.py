# coding=utf-8
from django import forms
from django.forms import ModelForm, Form
from students.model.base import Lecture, LabTask, Task, Course, Group


class LectureForm(ModelForm):

    class Meta:
        model = Lecture
        exclude = ['course']


class CourseForm(ModelForm):

    class Meta:
        model = Course
        exclude = ['teachers']


class SelectGroupForm(Form):
    group = forms.ModelChoiceField(Group.objects.all(), label=u"Группа")


class GroupForm(ModelForm):

    class Meta:
        model = Group
        exclude = ['courses']


class LabTaskForm(ModelForm):
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
