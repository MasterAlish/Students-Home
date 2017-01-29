# coding=utf-8
import traceback
import sys

import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from students.model.base import Teacher, Student, Group, UserActivity, LastReadMessage


def is_teacher(user):
    return Teacher.objects.filter(user=user).count() > 0


def is_student(user):
    return Student.objects.filter(user=user).count() > 0


def user_authenticated_to_course(user, course):
    return (is_student(user) and (course in user.student.group.courses.all()) or user.student in course.extra_students.all()) \
            or (is_teacher(user) and course in user.teacher.courses.all())


def user_authenticated_to_group(user, group):
    return (is_student(user) and group.id == user.student.group.id) \
            or (is_teacher(user) and group in reduce(lambda i, c: i + list(c.groups.all()), user.teacher.courses.all(), []))


class UserView(TemplateView):
    def register_user_activity(self, user):
        now = datetime.datetime.now()
        month = now.month
        year = now.year
        current_hour_index = (now.day - 1) * 24 + now.hour
        activity = UserActivity.get_for_month(user, year, month)
        weight = int(activity.activity[current_hour_index])
        weight = weight+1 if weight < 9 else 9
        activity.activity = activity.activity[:current_hour_index] \
                            + str(weight) \
                            + activity.activity[current_hour_index+1:]
        activity.save()
        user.last_seen = now
        user.save()

    def get_context_data(self, **kwargs):
        return {}


class TeachersView(UserView):
    teacher = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        self.context = self.get_context_data(**kwargs)
        self.teacher = None

        if is_teacher(request.user):
            self.teacher = request.user.teacher
            self.context['teacher'] = self.teacher
            try:
                self.register_user_activity(self.teacher.user)
                return self.handle(request, *args, **kwargs)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(type(e), e, exc_traceback)
        messages.error(request, _(u"Что-то пошло не так"))
        return redirect("/")

    def handle(self, request, *args, **kwargs):
        return super(TeachersView, self).dispatch(request, *args, **kwargs)


class StudentsView(UserView):
    student = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        self.context = self.get_context_data(**kwargs)
        self.student = None

        if is_student(request.user):
            self.student = request.user.student
            self.context['student'] = self.student
            try:
                self.register_user_activity(self.student.user)
                return self.handle(request, *args, **kwargs)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(type(e), e, exc_traceback)
        messages.error(request, _(u"Что-то пошло не так"))
        return redirect("/")

    def handle(self, request, *args, **kwargs):
        return super(StudentsView, self).dispatch(request, *args, **kwargs)


class StudentsAndTeachersView(UserView):
    student = None
    teacher = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        self.context = self.get_context_data(**kwargs)
        self.teacher = None
        self.student = None

        if is_student(request.user):
            self.student = request.user.student
            self.context['student'] = self.student
            self.register_user_activity(request.user)
        if is_teacher(request.user):
            self.teacher = request.user.teacher
            self.context['teacher'] = self.teacher
            self.register_user_activity(request.user)
        if self.teacher or self.student:
            try:
                return self.handle(request, *args, **kwargs)
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(type(e), e, exc_traceback)
        messages.error(request, _(u"Что-то пошло не так"))
        return redirect("/")

    def handle(self, request, *args, **kwargs):
        return super(StudentsAndTeachersView, self).dispatch(request, *args, **kwargs)
