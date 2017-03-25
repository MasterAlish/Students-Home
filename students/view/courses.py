# coding=utf-8
import os
import shutil
import zipfile

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse

from students.forms.courses import FileResolutionUploadForm, EmailForm, MedalForm, GroupStudentsSelectForm, \
    GroupStudentsInputForm, StudentException
from students.mail import StudentsMail
from students.model.base import Course, Lecture, Group, StudentMedal, LabTask, FileResolution, Resolution, Task, \
    GroupMock, Point
from students.model.checks import ZipContainsFileConstraint
from students.view.common import StudentsView, user_authorized_to_course, StudentsAndTeachersView, \
    user_authorized_to_group, TeachersView
from students.view.util import remove_file


class MyGroupView(StudentsView):
    template_name = "courses/group.html"

    def handle(self, request, *args, **kwargs):
        self.context['group'] = request.user.student.group
        return render(request, self.template_name, self.context)


class CourseView(StudentsAndTeachersView):
    template_name = "courses/course.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            self.context['course'] = course
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class LectureView(StudentsAndTeachersView):
    template_name = "courses/lecture.html"

    def handle(self, request, *args, **kwargs):
        lecture = Lecture.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, lecture.course):
            self.context['lecture'] = lecture
            self.context['course'] = lecture.course
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class LabTaskView(StudentsAndTeachersView):
    template_name = "courses/labtask.html"

    def handle(self, request, *args, **kwargs):
        labtask = LabTask.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, labtask.course):
            self.context['labtask'] = labtask
            self.context['course'] = labtask.course
            form = FileResolutionUploadForm()
            if request.method == "POST":
                form = FileResolutionUploadForm(data=request.POST, files=request.FILES)
                if form.is_valid():
                    form.instance.student = request.user.student
                    form.instance.task = labtask
                    form.instance.save()
                    valid, message = self.validate_file(form.instance, labtask)
                    if valid:
                        if self.has_html_index_file(labtask):
                            lab_url = self.unpack_resolution_to_public_dir(form.instance)
                            form.instance.index_file = lab_url
                            form.instance.save()
                        StudentsMail().report_new__file_resolution_uploaded(request, form.instance)
                        messages.success(request, u"Решение успешно сохранено")
                        return redirect(reverse("labtask", kwargs={'id': labtask.id}))
                    else:
                        try:
                            remove_file(form.instance.file.path)
                            form.instance.delete()
                        except:pass
                        form.add_error("file", message)

            self.context['form'] = form
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")

    def validate_file(self, resolution, labtask):
        for constraint in labtask.constraints.all():
            valid, message = constraint.test(resolution)
            if not valid:
                return valid, message
        return True, u""

    def unpack_resolution_to_public_dir(self, resolution):
        labname = "lab%d" % resolution.task.number
        username = resolution.student.get_short_name()
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
            zip_ref = zipfile.ZipFile(resolution.file.path)
            zip_ref.extractall(labpath)
            zip_ref.close()
        except Exception as e:
            print "Error: "+repr(e)
        lab_url = os.path.join(settings.MEDIA_URL, "sites", labname, username, "index.html")
        return lab_url

    def has_html_index_file(self, labtask):
        for constraint in labtask.constraints.instance_of(ZipContainsFileConstraint):
            if u'index.html' in constraint.file_names:
                return True
        return False


class GroupView(StudentsAndTeachersView):
    template_name = "courses/group.html"

    def handle(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs['id'])
        if user_authorized_to_group(request.user, group):
            self.context['group'] = group
            return render(request, self.template_name, self.context)
        raise Exception(u"Smth went wrong")


class ExtraGroupView(StudentsAndTeachersView):
    template_name = "courses/group.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['course_id'])
        group = GroupMock(u"Доп. группа: "+course.name, course, course.extra_students)
        if user_authorized_to_course(request.user, course):
            self.context['group'] = group
            return render(request, self.template_name, self.context)
        raise Exception(u"Smth went wrong")


class MarksMixin(object):

    def map_resolutions(self, resolutions):
        """
        :type resolutions: list of students.base.model.Resolution
        """
        resolutions_map = {}
        for resolution in resolutions:
            resolutions_for_work = {}
            if resolution.task_id in resolutions_map:
                resolutions_for_work = resolutions_map[resolution.task.id]

            students_resolutions = []
            if resolution.student_id in resolutions_for_work:
                students_resolutions = resolutions_for_work[resolution.student_id]
            students_resolutions.append(resolution)

            resolutions_for_work[resolution.student_id] = students_resolutions
            resolutions_map[resolution.task.id] = resolutions_for_work
        return resolutions_map

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

    def get_xp_by_students(self, course):
        xp_by_students = {}
        points_map = Point.objects.filter(course=course).values("student").annotate(xp=Sum("points"))
        for points in points_map:
            xp_by_students[points['student']] = points['xp']
        return xp_by_students


class MarksView(StudentsAndTeachersView, MarksMixin):
    template_name = "courses/marks.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            self.context['course'] = course
            tasks = course.active_tasks()
            self.context['tasks'] = tasks
            self.context['resolutions_map'] = self.map_resolutions(Resolution.objects.filter(task__in=tasks))
            self.context['medals_by_students'] = self.get_medals_by_students(course)
            self.context['xp_by_students'] = self.get_xp_by_students(course)

            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")



class EmailToCourseStudentsView(TeachersView):
    template_name = "courses/email_form.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
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
        if user_authorized_to_course(request.user, course):
            self.context['course'] = course
            medal_form = MedalForm()
            group_forms = map(lambda g: GroupStudentsSelectForm(g), course.groups_with_extra())
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


class SetMarksView(TeachersView):
    template_name = "courses/set_marks.html"

    def handle(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['id'])
        course = task.course
        if user_authorized_to_course(request.user, course):
            self.context['task'] = task
            self.context['course'] = course
            group_forms = map(lambda g: GroupStudentsInputForm(g, task), course.groups_with_extra())
            if request.method == 'POST':
                has_error = False
                student_values = {}
                for group_form in group_forms:
                    group_form.set_vals(request.POST)
                    try:
                        student_values.update(group_form.get_ints(request.POST))
                    except StudentException as e:
                        group_form.add_error(e.field, e.error)
                        has_error = True
                if len(student_values) == 0 and not has_error:
                    messages.error(request, u"Ничего не введено")
                else:
                    if not has_error:
                        for student, value in student_values.items():
                            Resolution.objects.filter(student=student, task=task).delete()
                            Resolution(student=student, task=task, mark=value).save()
                        messages.success(request, u"Оценки успешно проставлены")
                        return redirect(reverse("course", kwargs={'id': course.id}))
            self.context['group_forms'] = group_forms
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")