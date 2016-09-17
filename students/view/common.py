# coding=utf-8
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from students.model.base import Teacher, Student, Group


def is_teacher(user):
    return Teacher.objects.filter(user=user).count() > 0


def is_student(user):
    return Student.objects.filter(user=user).count() > 0


def user_authenticated_to_course(user, course):
    return (is_student(user) and course in user.student.group.courses.all()) \
            or (is_teacher(user) and course in user.teacher.courses.all())


def user_authenticated_to_group(user, group):
    return (is_student(user) and group.id == user.student.group.id) \
            or (is_teacher(user) and group in reduce(lambda i, c: i + list(c.groups.all()), user.teacher.courses.all(), []))


class TeachersView(TemplateView):
    teacher = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        if is_teacher(request.user):
            self.teacher = request.user.teacher
            self.context['teacher'] = self.teacher
            try:
                return self.handle(request, *args, **kwargs)
            except:
                pass
        messages.error(request, _(u"Что-то пошло не так"))
        return redirect("/")

    def handle(self, request, *args, **kwargs):
        return super(TeachersView, self).dispatch(request, *args, **kwargs)


class StudentsView(TemplateView):
    student = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        if is_student(request.user):
            self.student = request.user.student
            self.context['student'] = self.student
            try:
                return self.handle(request, *args, **kwargs)
            except:
                pass
        messages.error(request, _(u"Что-то пошло не так"))
        return redirect("/")

    def handle(self, request, *args, **kwargs):
        return super(StudentsView, self).dispatch(request, *args, **kwargs)


class StudentsAndTeachersView(TemplateView):
    student = None
    teacher = None
    context = {}

    def dispatch(self, request, *args, **kwargs):
        if is_student(request.user):
            self.student = request.user.student
            self.context['student'] = self.student
        if is_teacher(request.user):
            self.teacher = request.user.teacher
            self.context['teacher'] = self.teacher
        if self.teacher or self.student:
            try:
                return self.handle(request, *args, **kwargs)
            except:
                pass
        messages.error(request, _(u"Что-то пошло не так"))
        return redirect("/")

    def handle(self, request, *args, **kwargs):
        return super(StudentsAndTeachersView, self).dispatch(request, *args, **kwargs)


class GroupView(StudentsAndTeachersView):
    template_name = "courses/group.html"

    def dispatch(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['id'])
        if user_authenticated_to_group(request.user, group):
            self.context['group'] = group
            return render(request, self.template_name, self.context)
        raise Exception(u"Smth went wrong")

