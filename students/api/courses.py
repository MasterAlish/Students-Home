# coding=utf-8
from django.template.loader import render_to_string

from students.api.auth import AuthView
from students.model.base import Course, Resolution
from students.view.common import is_teacher, is_student
from students.view.courses import MarksMixin


class CoursesApi(AuthView):
    def handle(self, request, *args, **kwargs):
        courses = []
        if is_teacher(request.user):
            courses = request.user.teacher.courses.all()
        elif is_student(request.user):
            courses = request.user.student.courses
        courses_data = []
        for course in courses:
            course_data = course.to_dict()
            course_data['lectures'] = self.get_lectures(course)
            course_data['labtasks'] = self.get_labtasks(course)
            course_data['all_tasks'] = [task.to_dict() for task in course.all_tasks()]
            courses_data.append(course_data)
        return self.json_success(courses_data)

    def get_lectures(self, course):
        lectures = []
        for lecture in course.lectures.all():
            data = lecture.to_dict()
            context = {
                'text': lecture.body,
                'title': lecture.title,
                'subtitle': lecture.course.name,
            }
            data['file'] = "http://"+self.request.META["HTTP_HOST"]+data['file']
            data['body'] = render_to_string("api/html.html", context, request=self.request)
            lectures.append(data)
        return lectures

    def get_labtasks(self, course):
        tasks = []
        for labtask in course.active_labtasks():
            data = labtask.to_dict()
            context = {
                'text': labtask.body,
                'title': labtask.title,
                'subtitle': u"Дедлайн: "+data['deadline'],
                'datetime': labtask.created_at
            }
            data['body'] = render_to_string("api/html.html", context, request=self.request)
            tasks.append(data)
        return tasks


class MarksApi(AuthView, MarksMixin):
    def handle(self, request, *args, **kwargs):
        course_id = request.GET.get("course", None)
        if course_id and Course.objects.filter(pk=course_id).count() > 0:
            course = Course.objects.get(pk=course_id)
            groups = self.get_groups_data(course.groups_with_extra())
            tasks = course.active_tasks()
            resolutions_map = self.map_resolutions(Resolution.objects.filter(task__in=tasks))
            medals_by_students = self.get_medals_by_students(course)
            xp_by_students = self.get_xp_by_students(course)

            for task_id in resolutions_map:
                for student_id in resolutions_map[task_id]:
                    resolutions_data = []
                    for resolution in resolutions_map[task_id][student_id]:
                        resolutions_data.append(resolution.to_dict())
                    resolutions_map[task_id][student_id] = resolutions_data

            for student_id in medals_by_students:
                medals_data = []
                for medal in medals_by_students[student_id]:
                    data = medal.to_dict()
                    data['image'] = "http://"+request.META["HTTP_HOST"]+data['image']
                    medals_data.append(data)
                medals_by_students[student_id] = medals_data

            return self.json_success({
                'groups': groups,
                'resolutions_map': resolutions_map,
                'medals_by_students': medals_by_students,
            })
        else:
            return self.json_error("Course not found", 404)

    def get_groups_data(self, groups):
        groups_data = []
        for group in groups:
            students = [st.to_dict() for st in group.students.all()]
            data = {
                'id': group.id,
                'name': group.name,
                'students': students
            }
            groups_data.append(data)
        return groups_data