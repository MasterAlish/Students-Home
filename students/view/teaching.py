# coding=utf-8
import os

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from students.forms.courses import MedalForm
from students.forms.teaching import LectureForm, LabTaskForm, TaskForm, CourseForm, ArticleForm, CheckResolutionForm
from students.mail import StudentsMail
from students.model.base import Course, Lecture, LabTask, Task, Group, Resolution, HomeWorkSolution, StudentMedal
from students.model.blog import Article
from students.model.checks import FileSizeConstraint
from students.study.points import PointUtil
from students.view.common import TeachersView, user_authorized_to_course
from students.view.courses import GiveMedalsView
from students.view.util import remove_file


class CoursesListView(TeachersView):
    template_name = "courses/courses_list.html"

    def handle(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action == "unbind":
            group_id = request.POST.get("group", None)
            course_id = request.POST.get("course", None)
            if group_id and course_id:
                course = Course.objects.get(pk=course_id)
                Group.objects.get(pk=group_id).courses.remove(course)
        return render(request, self.template_name, {
            'courses': self.teacher.courses.order_by("-year").all()
        })


class CourseActionView(TeachersView):
    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if request.method == 'POST' and user_authorized_to_course(request.user, course):
            action = request.POST.get("action")
            if action == "edit":
                return redirect(reverse("edit_course", kwargs={'course_id': course.id}))
            elif action == 'delete':
                course.delete()
                messages.success(request, u"Курс удален успешно!")
            return redirect(reverse("all_courses"))
        raise Exception(u"User is not authorized")


class CourseFormView(TeachersView):
    template_name = "forms/model_form.html"
    model = u"курс"

    def handle(self, request, *args, **kwargs):
        course = None
        if 'course_id' in kwargs:
            course = Course.objects.get(pk=kwargs['course_id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        else:
            form = CourseForm(instance=course)
            if request.method == 'POST':
                form = CourseForm(request.POST, request.FILES, instance=course)
                if form.is_valid():
                    form.instance.save()
                    form.instance.teachers.add(self.teacher)
                    form.instance.save()
                    if course:
                        messages.success(request, u"Курс изменен успешно!")
                    else:
                        course = form.instance
                        messages.success(request, u"Курс добавлен успешно!")
                    return redirect(reverse("course", kwargs={'id': course.id}))
            return render(request, self.template_name, {'form': form, 'instance': course, 'model': self.model})


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
                if lecture.copies.count() == 0:
                    remove_file(lecture.pptx)
                lecture.delete()
                messages.success(request, u"Лекция удалена успешно!")
            return redirect(reverse("course", kwargs={'id': course.id}))
        raise Exception(u"User is not authorized")


class ResolutionsView(TeachersView):
    template_name = "courses/resolutions.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            context = {
                'course': course,
                'labtasks': course.active_labtasks().reverse()
            }

            if request.method == 'POST':
                solution = Resolution.objects.get(pk=request.POST.get('solution_id', None))
                action = request.POST.get("action", None)
                if action == 'delete':
                    try:
                        remove_file(solution.file.path)
                        solution.delete()
                    except:
                        pass
                    messages.success(request, u"Решение удалено успешно!")
                    return redirect(reverse("resolutions", kwargs={'id': course.id} ))
            return render(request, self.template_name, context)
        raise Exception(u"User is not authorized")


class HomeworksView(TeachersView):
    template_name = "courses/homeworks.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            context = {
                'course': course,
                'homeworks': course.homeworks.all().order_by("-datetime")
            }
            return render(request, self.template_name, context)
        raise Exception(u"User is not authorized")


class HomeworkView(TeachersView):
    template_name = "courses/homework.html"

    def handle(self, request, *args, **kwargs):
        homework = HomeWorkSolution.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, homework.course):
            if not homework.viewed:
                homework.viewed = True
                homework.save()
            form = MedalForm()
            if request.method == "POST":
                form = MedalForm(request.POST)
                if form.is_valid():
                    medal = form.cleaned_data['medal']
                    student = homework.student
                    StudentMedal(student=student, course=homework.course, medal=medal).save()
                    StudentsMail().inform_about_new_medal(student, medal, homework.course, request)
                    messages.success(request, u"Медаль \"%s\" успешна выдана" % medal.name)
                    return redirect(reverse("homework", kwargs={'id': homework.id}))
            context = {
                'homework': homework,
                'form': form
            }
            return render(request, self.template_name, context)
        raise Exception(u"User is not authorized")


class CheckResolutionView(TeachersView):
    template_name = "forms/check_resolution.html"

    def handle(self, request, *args, **kwargs):
        resolution = Resolution.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, resolution.task.course):
            form = CheckResolutionForm(initial={
                'comment': resolution.comment,
                'mark': resolution.mark
            })

            if request.method == 'POST':
                form = CheckResolutionForm(request.POST)
                if form.is_valid():
                    resolution.comment = form.cleaned_data['comment']
                    resolution.mark = form.cleaned_data['mark']
                    resolution.save()
                    if form.cleaned_data['medal']:
                        medal = form.cleaned_data['medal']
                        StudentMedal(student=resolution.student, course=resolution.task.course, medal=medal).save()
                        StudentsMail().inform_about_new_medal(resolution.student, medal, resolution.task.course, request)
                        messages.success(request, u"Медаль \"%s\" успешна выдана" % medal.name)
                        return redirect(reverse("check_resolution", kwargs={'id': resolution.id}))
                    if form.cleaned_data['add_points']:
                        point_util = PointUtil(resolution.student, resolution.task.course)
                        point_util.add_points(u"За выполнение лабы: \"%s\"" % resolution.task.title, resolution.mark)
                    return redirect(reverse("resolutions", kwargs={'id': resolution.task.course_id}))
            context = {
                'course': resolution.task.course,
                'resolution': resolution,
                'form': form
            }
            return render(request, self.template_name, context)
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
                        FileSizeConstraint(task=form.instance).save()
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
                remove_file(labtask.attachment)
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
                    form.save()
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
