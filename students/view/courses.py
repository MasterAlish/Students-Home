# coding=utf-8
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from students.model.students import Course, Student, Lecture


def is_student(user):
    return Student.objects.filter(user=user).count() > 0

def user_authenticated_to_course(user, course):
    return is_student(user) and course in user.student.group.courses.all()


class MyGroupView(TemplateView):
    template_name = "courses/my_group.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            assert is_student(request.user)
            context = {
                'group': request.user.student.group
            }
            return render(request, self.template_name, context)
        except:
            pass
        messages.error(request, u"Ошибочная страница")
        return redirect("/")


class CourseView(TemplateView):
    template_name = "courses/course.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(pk=kwargs['id'])
            if user_authenticated_to_course(request.user, course):
                context = {
                    'course': course
                }
                return render(request, self.template_name, context)
        except:
            pass
        messages.error(request, u"Такой курс не существует")
        return redirect("/")



class LectureView(TemplateView):
    template_name = "courses/lecture.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            lecture = Lecture.objects.get(pk=kwargs['id'])
            if user_authenticated_to_course(request.user, lecture.course):
                context = {
                    'lecture': lecture,
                    'course': lecture.course
                }
                return render(request, self.template_name, context)
        except:
            pass
        messages.error(request, u"Такая лекция не существует")
        return redirect("/")