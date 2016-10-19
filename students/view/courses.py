# coding=utf-8
import os
import zipfile

import shutil

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from slugify import slugify_unicode

from students.forms.courses import SolutionUploadForm, EmailForm, MedalForm, GroupStudentsForm
from students.mail import StudentsMail
from students.model.base import Course, Lecture, Group, LabWork, Solution, StudentMedal
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
                    valid, message = self.validate_archive(form.instance)
                    if valid:
                        self.unpack_solution_to_public_dir(form.instance)
                        StudentsMail().report_new_solution_uploaded(request, form.instance)
                        messages.success(request, u"Решение успешно сохранено")
                        return redirect(reverse("labwork", kwargs={'id': labwork.id}))
                    else:
                        form.add_error("file", message)

            self.context['form'] = form
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")

    def validate_archive(self, solution):
        def is_ascii(s):
            return all(ord(c) < 128 for c in s)
        if not zipfile.is_zipfile(solution.file.path):
            solution.delete()
            return False, u"Файл должен быть .zip архивом"
        file_info = os.stat(solution.file.path)
        if file_info.st_size > 5242880L:
            solution.delete()
            return False, u"Файл должен быть не больше 5 МБ (5242880 Б)"
        files = zipfile.ZipFile(solution.file.path).filelist
        has_index_file = False
        not_ascii_file_name = None

        for file in files:
            if file.filename == "index.html":
                has_index_file = True
            if not is_ascii(file.filename):
                not_ascii_file_name = file.filename
                break
        if not_ascii_file_name:
            solution.delete()
            return False, u"В архиве есть файл с неправильным названием %s. Прочитайте условия сдачи." % not_ascii_file_name.decode('utf-8', 'ignore')
        if not has_index_file:
            solution.delete()
            return False, u"В корне архива должен быть файл index.html"
        return True, u""

    def unpack_solution_to_public_dir(self, solution):
        labname = "lab%d" % solution.labwork.number
        username = solution.student.get_short_name()
        labpath = os.path.join(settings.MEDIA_ROOT, "sites", labname, username)
        try:
            os.makedirs(labpath)
        except:
            pass
        try:
            shutil.rmtree(labpath)
        except:
            pass
        try:
            zip_ref = zipfile.ZipFile(solution.file.path)
            zip_ref.extractall(labpath)
            zip_ref.close()
        except Exception as e:
            print "Error: "+repr(e)
        return labpath


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
            self.context['medals_by_students'] = self.get_medals_by_students(course)

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

    def get_medals_by_students(self, course):
        medals_by_students = {}
        medals = StudentMedal.objects.filter(course=course)
        for medal in medals:
            student_medals = []
            if medal.student_id in medals_by_students:
                student_medals = medals_by_students[medal.student_id]
            student_medals.append(medal)
            medals_by_students[medal.student_id] = student_medals
        return medals_by_students


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


class GiveMedalsView(TeachersView):
    template_name = "courses/give_medals.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, course):
            self.context['course'] = course
            medal_form = MedalForm()
            group_forms = map(lambda g: GroupStudentsForm(g), course.groups.all())
            if request.method == 'POST':
                medal_form = MedalForm(request.POST)
                selected_students = []
                for group_form in group_forms:
                    selected_students.extend(group_form.get_selected(request.POST))
                if len(selected_students) == 0:
                    messages.error(request, u"Выберите хотя бы одного студента")
                else:
                    if medal_form.is_valid():
                        medal = medal_form.cleaned_data['medal']
                        for student in selected_students:
                            StudentMedal(student=student, course=course, medal=medal).save()
                            StudentsMail().inform_about_new_medal(student, medal, course, request)
                        messages.success(request, u"Медаль \"%s\" успешна выдана %d студентам" % (medal.name, len(selected_students)))
                        return redirect(reverse("course", kwargs={'id': course.id}))
            self.context['medal_form'] = medal_form
            self.context['group_forms'] = group_forms
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")