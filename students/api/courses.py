# coding=utf-8
from django.template.loader import render_to_string

from students.api.auth import AuthView
from students.view.common import is_teacher, is_student


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