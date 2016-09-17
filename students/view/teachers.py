# coding=utf-8
from django.shortcuts import render

from students.model.base import Group, Teacher
from students.view.common import TeachersView, StudentsAndTeachersView, user_authenticated_to_group


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