# coding=utf-8
import json

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from students.model.base import Mail


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
        self.save_mail(subject, message, message_html, recipients)

    def inform_students_of_course(self, course, subject, html_text):
        """
        :type teacher: students.model.base.Course
        """
        recipients = []
        for group in course.groups.all():
            for student in group.students.all():
                recipients.append(student.user.email)
        self.save_mail(subject, html_text, html_text, recipients)

    def inform_students_of_group(self, group, subject, html_text):
        """
        :type teacher: students.model.base.Group
        """
        recipients = []
        for student in group.students.all():
            recipients.append(student.user.email)
        self.save_mail(subject, html_text, html_text, recipients)

    def student_registered(self, request, student):
        subject = u"Зарегистрировался новый студент: %s" % unicode(student)
        message = u"Перейдите по ссылку чтобы активировать аккаунт студента %s " % unicode(request.META["HTTP_ORIGIN"]+"/admin/students/myuser/"+str(student.user.id))
        recipients = [settings.EMAIL_ADMIN_EMAIL]
        self.save_mail(subject, message, message, recipients)

    def save_mail(self, subject, message, message_html, recipients):
        Mail(subject=subject, body_html=message_html, body_txt=message, recipients=json.dumps(recipients)).save()

    def send_saved_mails(self, stdout):
        import time
        start_time = time.time()
        mails_sent = 0
        while Mail.objects.count() > 0:
            mail = Mail.objects.first()
            send_mail(mail.subject, mail.body_txt, settings.DEFAULT_FROM_EMAIL, json.loads(mail.recipients),
                      html_message=mail.body_html, fail_silently=False)
            mail.delete()
            mails_sent += 1
            current_time = time.time()
            if current_time - start_time > 25.0:
                break
        if stdout:
            stdout.write(u"Mails sent: %d. Mails left: %d" % (mails_sent, Mail.objects.count()))