# coding=utf-8
import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from students.forms.teaching import LectureForm, LabTaskForm, TaskForm
from students.model.base import Course, Lecture, LabTask, Task
from students.view.common import TeachersView, user_authorized_to_course
from students.view.util import remove_file


class LectureFormView(TeachersView):
    template_name = "forms/model_form.html"
    model = u"лекцию"

    def handle(self, request, *args, **kwargs):
        lecture = None
        course = None
        if 'lecture_id' in kwargs:
            lecture = Lecture.objects.get(pk=kwargs['lecture_id'])
            course = lecture.course
        if 'id' in kwargs:
            course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            form = LectureForm(instance=lecture)
            if request.method == 'POST':
                form = LectureForm(request.POST, request.FILES, instance=lecture)
                if form.is_valid():
                    form.instance.course = course
                    form.instance.save()
                    if lecture:
                        messages.success(request, u"Лекция изменена успешно!")
                    else:
                        messages.success(request, u"Лекция добавлена успешно!")
                    return redirect(reverse("course", kwargs={'id': course.id}))
            return render(request, self.template_name,
                          {'course': course, 'form': form, 'instance': lecture, 'model': self.model})
        raise Exception(u"User is not authorized")


class LectureActionView(TeachersView):
    def handle(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(pk=kwargs['id'])
        course = lecture.course
        if request.method == 'POST' and user_authorized_to_course(request.user, course):
            action = request.POST.get("action")
            if action == "edit":
                return redirect(reverse("edit_lecture", kwargs={'lecture_id': lecture.id}))
            elif action == 'delete':
                remove_file(lecture.pptx)
                lecture.delete()
                messages.success(request, u"Лекция удалена успешно!")
            return redirect(reverse("course", kwargs={'id': course.id}))
        raise Exception(u"User is not authorized")


class LabTaskFormView(TeachersView):
    template_name = "forms/model_form.html"
    model = u"лабораторную работу"

    def handle(self, request, *args, **kwargs):
        labtask = None
        course = None
        if 'labtask_id' in kwargs:
            labtask = LabTask.objects.get(pk=kwargs['labtask_id'])
            course = labtask.course
        if 'id' in kwargs:
            course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            form = LabTaskForm(instance=labtask)
            if request.method == 'POST':
                form = LabTaskForm(request.POST, request.FILES, instance=labtask)
                if form.is_valid():
                    form.instance.course = course
                    form.instance.save()
                    if labtask:
                        messages.success(request, u"Лабораторная работа изменена успешно!")
                    else:
                        messages.success(request, u"Лабораторная работа добавлена успешно!")
                    return redirect(reverse("course", kwargs={'id': course.id}))
            return render(request, self.template_name,
                          {'course': course, 'form': form, 'instance': labtask, 'model': self.model})
        raise Exception(u"User is not authorized")


class LabTaskActionView(TeachersView):
    def handle(self, request, *args, **kwargs):
        labtask = LabTask.objects.get(pk=kwargs['id'])
        course = labtask.course
        if request.method == 'POST' and user_authorized_to_course(request.user, course):
            action = request.POST.get("action")
            if action == "edit":
                return redirect(reverse("edit_labtask", kwargs={'labtask_id': labtask.id}))
            elif action == 'delete':
                labtask.delete()
                messages.success(request, u"Лабораторная работа удалена успешно!")
            return redirect(reverse("course", kwargs={'id': course.id}))
        raise Exception(u"User is not authorized")


class TaskFormView(TeachersView):
    template_name = "forms/model_form.html"
    model = u"задание"

    def handle(self, request, *args, **kwargs):
        task = None
        course = None
        if 'task_id' in kwargs:
            task = Task.objects.get(pk=kwargs['task_id'])
            course = task.course
        if 'id' in kwargs:
            course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            form = TaskForm(instance=task)
            if request.method == 'POST':
                form = TaskForm(request.POST, request.FILES, instance=task)
                if form.is_valid():
                    form.instance.course = course
                    form.instance.save()
                    if task:
                        messages.success(request, u"Задание изменено успешно!")
                    else:
                        messages.success(request, u"Задание добавлено успешно!")
                    return redirect(reverse("course", kwargs={'id': course.id}))
            return render(request, self.template_name,
                          {'course': course, 'form': form, 'instance': task, 'model': self.model})
        raise Exception(u"User is not authorized")


class TaskActionView(TeachersView):
    def handle(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['id'])
        course = task.course
        if request.method == 'POST' and user_authorized_to_course(request.user, course):
            action = request.POST.get("action")
            if action == "edit":
                return redirect(reverse("edit_task", kwargs={'task_id': task.id}))
            elif action == 'delete':
                task.delete()
                messages.success(request, u"Задание удалено успешно!")
            return redirect(reverse("course", kwargs={'id': course.id}))
        raise Exception(u"User is not authorized")
