# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from students.model.base import Group, Teacher, Student
from students.view.common import TeachersView, StudentsAndTeachersView, user_authorized_to_group


class TeachersListView(TemplateView):
    template_name = "teachers/list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            raise Http404()
        context = {
            'teachers': Teacher.objects.all()
        }
        return render(request, self.template_name, context)


class TeacherGroupsView(TeachersView):
    template_name = "teachers/groups.html"

    def handle(self, request, *args, **kwargs):
        self.context['courses'] = self.teacher.courses
        return render(request, self.template_name, self.context)


class TeacherView(StudentsAndTeachersView):
    template_name = "teachers/teacher.html"

    def dispatch(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(pk=kwargs['id'])
        self.context['teacher'] = teacher
        return render(request, self.template_name, self.context)


class StudentView(StudentsAndTeachersView):
    template_name = "teachers/student.html"

    def dispatch(self, request, *args, **kwargs):
        student = Student.objects.get(pk=kwargs['id'])
        self.context['student'] = student
        return render(request, self.template_name, self.context)