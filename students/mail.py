# coding=utf-8
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class StudentsMail(object):
    def report_new_solution_uploaded(self, request, solution):
        """
        :type teacher: students.model.base.Solution
        """
        subject = u"Новая лабораторка от %s" % unicode(solution.student)
        message = u"Новая лабораторка от %s\n\n\"%s\"\n\nПерейдите по ссылке чтобы скачать решение %s" % \
                  (solution.student, solution.comment, unicode(request.META["HTTP_ORIGIN"]+"/admin/students/solution/"+str(solution.id)))
        message_html = u"Новая лабораторка от %s<br><br>\"%s\"<br><br>Перейдите по ссылке чтобы скачать решение " \
                       u"<a href=\"%s\">Перейти</a>"  % \
                  (solution.student, solution.comment, unicode(request.META["HTTP_ORIGIN"]+"/admin/students/solution/"+str(solution.id)))
        recipients = map(lambda t:t.user.email, solution.labwork.course.teachers.all())
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, html_message=message_html, fail_silently=False)

    def inform_students_of_course(self, course, subject, html_text):
        """
        :type teacher: students.model.base.Course
        """
        recipients = []
        for group in course.groups.all():
            for student in group.students.all():
                recipients.append(student.user.email)
        send_mail(subject, html_text, settings.DEFAULT_FROM_EMAIL, recipients, html_message=html_text, fail_silently=False)

    def inform_students_of_group(self, group, subject, html_text):
        """
        :type teacher: students.model.base.Group
        """
        recipients = []
        for student in group.students.all():
            recipients.append(student.user.email)
        send_mail(subject, html_text, settings.DEFAULT_FROM_EMAIL, recipients, html_message=html_text, fail_silently=False)