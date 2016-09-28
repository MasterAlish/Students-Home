# coding=utf-8
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from students.forms.courses import SolutionUploadForm, EmailForm
from students.mail import StudentsMail
from students.model.base import Course, Lecture, Group, LabWork, Solution
from students.view.common import StudentsView, user_authenticated_to_course, StudentsAndTeachersView, \
    user_authenticated_to_group, TeachersView


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


class LabWorkView(StudentsAndTeachersView):
    template_name = "courses/labwork.html"

    def handle(self, request, *args, **kwargs):
        labwork = LabWork.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, labwork.course):
            self.context['labwork'] = labwork
            self.context['course'] = labwork.course
            form = SolutionUploadForm()
            if request.method == "POST":
                form = SolutionUploadForm(data=request.POST, files=request.FILES)
                if form.is_valid():
                    form.instance.student = request.user.student
                    form.instance.labwork = labwork
                    form.instance.save()
                    StudentsMail().report_new_solution_uploaded(request, form.instance)
                    messages.success(request, u"Решение успешно сохранено")
                    return redirect(reverse("labwork", kwargs={'id': labwork.id}))
            self.context['form'] = form
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


class MarksView(StudentsAndTeachersView):
    template_name = "courses/marks.html"

    def dispatch(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, course):
            self.context['course'] = course
            labworks = course.active_labworks()
            self.context['labs'] = labworks
            self.context['solutions_map'] = self.map_solutions(Solution.objects.filter(labwork__in=labworks))

            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")

    def map_solutions(self, solutions):
        """
        :type solutions: list of students.base.model.Solution
        """
        solutions_map = {}
        for solution in solutions:
            solutions_for_work = {}
            if solution.labwork_id in solutions_map:
                solutions_for_work = solutions_map[solution.labwork.id]

            students_solutions = []
            if solution.student_id in solutions_for_work:
                students_solutions = solutions_for_work[solution.student_id]
            students_solutions.append(solution)

            solutions_for_work[solution.student_id] = students_solutions
            solutions_map[solution.labwork.id] = solutions_for_work
        return solutions_map


class EmailToCourseStudentsView(TeachersView):
    template_name = "courses/email_form.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, course):
            self.context['course'] = course
            form = EmailForm()
            if request.method == 'POST':
                form = EmailForm(request.POST)
                if form.is_valid():
                    subject = form.cleaned_data['subject']
                    body = form.cleaned_data['body']
                    StudentsMail().inform_students_of_course(course, subject, body)
                    messages.success(request, u"Сообщение отправлено успешно")
                    return redirect(reverse("course", kwargs={'id': course.id}))
            self.context['form'] = form
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")