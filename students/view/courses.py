# coding=utf-8
import json
import logging
import os
import shutil
import zipfile

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView

from students.forms.courses import FileResolutionUploadForm, EmailForm, MedalForm, GroupStudentsSelectForm, \
    GroupStudentsInputForm, StudentException
from students.forms.teaching import GroupForm, SelectGroupForm, LiteratureForm, AddPointForm
from students.mail import StudentsMail
from students.model.base import Course, Lecture, Group, StudentMedal, LabTask, Resolution, Task, \
    GroupMock, Point, Student, Teacher, Literature, MustKnow, AlreadyKnow, MustKnowGroup, AppAd
from students.model.blog import Article
from students.model.checks import ZipContainsFileConstraint, FileNameConstraint
from students.models import MyUser
from students.study.points import get_rating
from students.utils.unpacker import unpack_resolution_to_public_dir
from students.view.common import StudentsView, user_authorized_to_course, StudentsAndTeachersView, \
    user_authorized_to_group, TeachersView, is_teacher
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
            self.context['app_ad'] = AppAd.random()
            exclude_articles = Article.objects.filter(private=True).exclude(course=course)
            if course.subject:
                self.context['articles'] = course.subject.all_articles().exclude(pk__in=exclude_articles)
            else:
                self.context['articles'] = course.articles.all()
            self.context['new_solutions_count'] = Resolution.objects.filter(mark=0, task__course=course).count()
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
        logger = logging.getLogger("django")
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
                        try:
                            if self.is_zip_with_html_index_file(labtask):
                                lab_url = unpack_resolution_to_public_dir(form.instance)
                                form.instance.index_file = lab_url
                                form.instance.save()
                            if self.is_single_html_file(labtask):
                                form.instance.index_file = form.instance.file.url
                                form.instance.save()
                            StudentsMail().report_new_file_resolution_uploaded(request, form.instance)
                            messages.success(request, u"?????????????? ?????????????? ??????????????????")
                            return redirect(reverse("labtask", kwargs={'id': labtask.id}))
                        except Exception as e:
                            logger.exception(repr(e))
                            remove_file(form.instance.file.path)
                            form.instance.delete()
                            form.add_error("file", repr(e))
                    else:
                        try:
                            remove_file(form.instance.file.path)
                            form.instance.delete()
                        except Exception as e:
                            logger.exception(repr(e))
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

    def is_zip_with_html_index_file(self, labtask):
        for constraint in labtask.constraints.instance_of(ZipContainsFileConstraint):
            if u'index.html' in constraint.file_names:
                return True
        return False

    def is_single_html_file(self, labtask):
        for constraint in labtask.constraints.instance_of(FileNameConstraint):
            if u'html' == constraint.extension:
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


class ActivateStudentView(TeachersView):
    def handle(self, request, *args, **kwargs):
        student = Student.objects.get(pk=kwargs['id'])
        student.user.is_active = not student.user.is_active
        student.user.save()
        if student.user.is_active:
            StudentsMail().report_account_activated(student, request)
        return redirect(reverse("group", kwargs={'id': student.group_id}))


class ExpelStudentView(TeachersView):
    def handle(self, request, *args, **kwargs):
        student = Student.objects.get(pk=kwargs['id'])
        student.active = False
        student.save()
        return redirect(reverse("group", kwargs={'id': student.group_id}))


class DeleteStudentView(TeachersView):
    def handle(self, request, *args, **kwargs):
        student = Student.objects.get(pk=kwargs['id'])
        student.user.delete()
        return redirect(reverse("group", kwargs={'id': student.group_id}))


class ActivateTeacherView(TeachersView):
    def handle(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(pk=kwargs['id'])
        teacher.user.is_active = not teacher.user.is_active
        teacher.user.save()
        return redirect(reverse("group", kwargs={'id': teacher.group_id}))


class ExtraGroupView(StudentsAndTeachersView):
    template_name = "courses/group.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['course_id'])
        group = GroupMock(u"??????. ????????????: " + course.name, course, course.extra_students)
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
            xp_by_students[points['student']] = {
                "points": points['xp'],
                "rating": get_rating(points['xp'])
            }
        for group in course.groups_with_extra():
            for student in group.active_students():
                if student.id not in xp_by_students:
                    xp_by_students[student.id] = {
                        "points": 0,
                        "rating": get_rating(0)
                    }
        return xp_by_students


class MarksView(StudentsAndTeachersView, MarksMixin):
    template_name = "courses/marks.html"
    print_template_name = "courses/marks_print.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            self.context['course'] = course
            tasks = course.active_tasks()
            self.context['tasks'] = tasks
            self.context['resolutions_map'] = self.map_resolutions(Resolution.objects.filter(task__in=tasks))
            self.context['medals_by_students'] = self.get_medals_by_students(course)
            self.context['xp_by_students'] = self.get_xp_by_students(course)

            if request.GET.get("print"):
                return render(request, self.print_template_name, self.context)
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
                    messages.success(request, u"?????????????????? ???????????????????? ??????????????")
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
                    messages.error(request, u"???????????????? ???????? ???? ???????????? ????????????????")
                else:
                    if medal_form.is_valid():
                        medal = medal_form.cleaned_data['medal']
                        for student in selected_students:
                            StudentMedal(student=student, course=course, medal=medal).save()
                            StudentsMail().inform_about_new_medal(student, medal, course, request)
                        messages.success(request, u"???????????? \"%s\" ?????????????? ???????????? %d ??????????????????" % (
                        medal.name, len(selected_students)))
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
                    messages.error(request, u"???????????? ???? ??????????????")
                else:
                    if not has_error:
                        for student, value in student_values.items():
                            Resolution.objects.filter(student=student, task=task).delete()
                            Resolution(student=student, task=task, mark=value).save()
                        messages.success(request, u"???????????? ?????????????? ??????????????????????")
                        return redirect(reverse("course", kwargs={'id': course.id}))
            self.context['group_forms'] = group_forms
            return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class CreateGroupViewView(TeachersView):
    template_name = "forms/add_group_form.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        else:
            existing_group_form = SelectGroupForm()
            form = GroupForm()
            if request.method == 'POST':
                if request.POST.get("existing_group", None):
                    existing_group_form = SelectGroupForm(request.POST)
                    if existing_group_form.is_valid():
                        group = existing_group_form.cleaned_data['group']
                        group.courses.add(course)
                        messages.success(request, u"???????????? ?????????????????? ??????????????!")
                        return redirect(reverse("all_courses"))
                else:
                    form = GroupForm(request.POST)
                    if form.is_valid():
                        form.instance.save()
                        form.instance.courses.add(course)
                        form.instance.save()
                        messages.success(request, u"???????????? ?????????????????? ??????????????!")
                        return redirect(reverse("all_courses"))
            return render(request, self.template_name, {
                'form': form,
                'existing_group_form': existing_group_form,
                'course': course
            })


class LiteratureView(StudentsAndTeachersView):
    template_name = "students/literature.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        context = {
            'literature': course.literature.all(),
            'course': course
        }
        return render(request, self.template_name, context)


class AddLiteratureView(TeachersView):
    template_name = "forms/literature_form.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        if not self.teacher:
            raise Exception(u"User is not authorized")
        form = LiteratureForm()
        if request.method == 'POST':
            form = LiteratureForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.course = course
                form.instance.save()
                messages.success(request, u"???????????????????? ?????????????? ??????????????????")
                return redirect(reverse("literature", kwargs={'id': course.id}))

        context = {
            'form': form,
            'course': course
        }
        return render(request, self.template_name, context)


class EditLiteratureView(TeachersView):
    template_name = "forms/literature_form.html"

    def handle(self, request, *args, **kwargs):
        literature = Literature.objects.get(pk=kwargs['id'])
        if not user_authorized_to_course(request.user, literature.course):
            raise Exception(u"User is not authorized")
        if not self.teacher:
            raise Exception(u"User is not authorized")
        form = LiteratureForm(instance=literature)
        if request.method == 'POST':
            form = LiteratureForm(request.POST, request.FILES, instance=literature)
            if form.is_valid():
                form.instance.course = literature.course
                form.instance.save()
                messages.success(request, u"???????????????????? ?????????????? ????????????????")
                return redirect(reverse("literature", kwargs={'id': literature.course.id}))

        context = {
            'literature': literature,
            'form': form,
            'course': literature.course
        }
        return render(request, self.template_name, context)


class DeleteLiteratureView(TeachersView):
    def handle(self, request, *args, **kwargs):
        literature = Literature.objects.get(pk=kwargs['id'])
        course = literature.course
        if not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        if not self.teacher:
            raise Exception(u"User is not authorized")
        literature.delete()
        return redirect(reverse("literature", kwargs={'id': course.id}))


class MustKnowsView(StudentsAndTeachersView):
    template_name = "courses/must_knows.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        if request.POST and is_teacher(request.user):
            group_name = request.POST.get("name", "").strip()
            if group_name:
                MustKnowGroup(course=course, name=group_name).save()
                return redirect(reverse("must_knows", kwargs={'id': course.id}))
        context = {
            'selected_user': request.user,
            'course': course,
            'total_must_knows': MustKnow.objects.filter(group__course=course).count(),
            'already_know': [x[0] for x in request.user.i_know.filter(must_know__group__course=course).values_list("must_know__id")]
        }
        return render(request, self.template_name, context)


class MustKnowOfStudentView(StudentsAndTeachersView):
    template_name = "courses/must_knows.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['course_id'])
        user = MyUser.objects.get(pk=kwargs['id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        context = {
            'selected_user': user,
            'course': course,
            'total_must_knows': MustKnow.objects.filter(group__course=course).count(),
            'already_know': [x[0] for x in user.i_know.filter(must_know__group__course=course).values_list("must_know__id")]
        }
        return render(request, self.template_name, context)


class StudentXPView(StudentsAndTeachersView):
    template_name = "courses/xps.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['course_id'])
        student = Student.objects.get(pk=kwargs['id'])
        if course and not user_authorized_to_course(request.user, course):
            raise Exception(u"User is not authorized")
        form = AddPointForm()
        if request.method == "POST" and is_teacher(request.user):
            form = AddPointForm(request.POST)
            if form.is_valid():
                form.instance.student = student
                form.instance.course = course
                form.instance.save()
                return redirect(request.path)
        xps = Point.objects.filter(course=course, student=student)
        points_sum = xps.aggregate(Sum("points"))["points__sum"] or 0
        context = {
            'student': student,
            'course': course,
            'xps': xps,
            'points_sum': points_sum,
            'rating': get_rating(points_sum),
            'form': form
        }
        return render(request, self.template_name, context)


class MustKnowToggleView(StudentsAndTeachersView):
    def handle(self, request, *args, **kwargs):
        must_know = MustKnow.objects.get(pk=kwargs['id'])
        if not user_authorized_to_course(request.user, must_know.group.course):
            raise Exception(u"User is not authorized")
        done = True
        if AlreadyKnow.objects.filter(user=request.user, must_know=must_know).exists():
            AlreadyKnow.objects.filter(user=request.user, must_know=must_know).delete()
            done = False
        else:
            AlreadyKnow(user=request.user, must_know=must_know).save()

        return JsonResponse({'done': done})


class MustKnowAddView(StudentsAndTeachersView):
    template_name = "blocks/must_know_item.html"

    def handle(self, request, *args, **kwargs):
        must_know_group = MustKnowGroup.objects.get(pk=kwargs['group_id'])
        if not is_teacher(request.user) and not user_authorized_to_course(request.user, must_know_group.course):
            return HttpResponse()
        name = request.GET.get("name", "").strip()
        if name:
            item = MustKnow(group=must_know_group, text=name)
            item.save()

            return render(request, self.template_name, {'item': item})
        return HttpResponse()


class MustKnowActionView(StudentsAndTeachersView):

    def handle(self, request, *args, **kwargs):
        must_know = MustKnow.objects.get(pk=kwargs['id'])
        if not is_teacher(request.user) and not user_authorized_to_course(request.user, must_know.group.course):
            return HttpResponse()
        action = request.GET.get("action")
        if action == "up":
            must_know.up()
        elif action == "down":
            must_know.down()

        return HttpResponse()
