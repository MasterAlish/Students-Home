# coding=utf-8
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from students.forms.courses import HomeWorkForm
from students.mail import StudentsMail
from students.model.base import Course
from students.view.common import StudentsView


class UploadHomeWorkView(StudentsView):
    template_name = "students/homework/upload.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        form = HomeWorkForm()
        if request.method == "POST":
            form = HomeWorkForm(request.POST, request.FILES)
            if form.is_valid():
                solution = form.instance
                solution.course = course
                solution.student = self.student
                solution.save()
                messages.success(request, u"Домашнее задание успешно загружено!")
                StudentsMail().report_homework_uploaded(request, solution)
                return redirect(reverse("course", kwargs={'id': course.id}))
        context = {
            'form': form,
            'course': course
        }
        return render(request, self.template_name, context)
