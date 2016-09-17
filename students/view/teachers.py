# coding=utf-8
from django.shortcuts import render
from students.view.common import TeachersView


class TeacherGroupsView(TeachersView):
    template_name = "teachers/groups.html"

    def handle(self, request, *args, **kwargs):
        self.context['courses'] = self.teacher.courses
        return render(request, self.template_name, self.context)