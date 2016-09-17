# coding=utf-8
from django.shortcuts import render
from students.model.base import Course, Lecture, Group
from students.view.common import StudentsView, user_authenticated_to_course, StudentsAndTeachersView, \
    user_authenticated_to_group


class MyGroupView(StudentsView):
    template_name = "courses/group.html"

    def handle(self, request, *args, **kwargs):
        self.context['group'] = request.user.student.group
        return render(request, self.template_name, self.context)


class CourseView(StudentsAndTeachersView):
    template_name = "courses/course.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, course):
            self.context['course'] = course
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class LectureView(StudentsAndTeachersView):
    template_name = "courses/lecture.html"

    def handle(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, lecture.course):
            self.context['lecture'] = lecture
            self.context['course'] = lecture.course
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class GroupView(StudentsAndTeachersView):
    template_name = "courses/group.html"

    def dispatch(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['id'])
        if user_authenticated_to_group(request.user, group):
            self.context['group'] = group
            return render(request, self.template_name, self.context)
        raise Exception(u"Smth went wrong")