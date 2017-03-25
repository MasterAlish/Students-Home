# coding=utf-8
import json

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from students.model.base import Mail


class StudentsMail(object):
    def report_new__file_resolution_uploaded(self, request, file_resolution):
        """
        :type file_resolution: students.model.base.FileResolution
        """
        subject = u"Новая лабораторка от %s" % unicode(file_resolution.student)
        message = u"Новая лабораторка от %s\n\n\"%s\"\n\nПерейдите по ссылке чтобы скачать решение %s" % \
                  (file_resolution.student, file_resolution.comment, unicode(request.META["HTTP_ORIGIN"] + "/admin/students/fileresolution/" + str(file_resolution.id)))
        message_html = u"Новая лабораторка от %s<br><br>\"%s\"<br><br>Перейдите по ссылке чтобы скачать решение " \
                       u"<a href=\"%s\">Перейти</a>"  % \
                  (file_resolution.student, file_resolution.comment, unicode(request.META["HTTP_ORIGIN"] + "/admin/students/fileresolution/" + str(file_resolution.id)))
        recipients = map(lambda t:t.user.email, file_resolution.task.course.teachers.all())
        self.save_mail(subject, message, message_html, recipients)

    def report_homework_uploaded(self, request, homework):
        """
        :type homework: students.model.base.HomeworkSolution
        """
        subject = u"Домашнее задание от %s" % unicode(homework.student)
        message = u"Домашнее задание от %s\n\n\"%s\"\n\nПерейдите по ссылке чтобы скачать решение %s" % \
                  (homework.student, homework.comment, unicode(request.META["HTTP_ORIGIN"] + "/admin/students/homeworksolution/" + str(homework.id)))
        message_html = u"Домашнее задание от %s<br><br>\"%s\"<br><br>Перейдите по ссылке чтобы скачать решение " \
                       u"<a href=\"%s\">Перейти</a>"  % \
                  (homework.student, homework.comment, unicode(request.META["HTTP_ORIGIN"] + "/admin/students/homeworksolution/" + str(homework.id)))
        recipients = map(lambda t:t.user.email, homework.course.teachers.all())
        self.save_mail(subject, message, message_html, recipients)

    def inform_students_of_course(self, course, subject, html_text):
        """
        :type course: students.model.base.Course
        """
        recipients = []
        for group in course.groups_with_extra():
            for student in group.students.all():
                recipients.append(student.user.email)
        self.save_mail(subject, html_text, html_text, recipients)

    def inform_students_of_group(self, group, subject, html_text):
        """
        :type group: students.model.base.Group
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

    def teacher_registered(self, request, teacher):
        subject = u"Зарегистрировался новый учитель: %s" % unicode(teacher)
        message = u"Перейдите по ссылку чтобы активировать аккаунт учителя %s " % unicode(request.META["HTTP_ORIGIN"]+"/admin/students/myuser/"+str(teacher.user.id))
        recipients = [settings.EMAIL_ADMIN_EMAIL]
        self.save_mail(subject, message, message, recipients)

    def inform_about_new_medal(self, student, medal, course, request):
        """
        :type student: students.model.base.Student
        :type medal: students.model.base.Medal
        :type course: students.model.base.Course
        """
        subject = u"У вас новая медаль!"
        message = u"Уважаемый, %s, поздравляем вас с новой медалью \"%s\"! Перейдите по ссылке чтобы просмотреть свои медали %s " % \
                  (student.user.get_full_name(), medal.name, unicode(request.META["HTTP_ORIGIN"]+reverse('marks', kwargs={'id': course.id})))
        recipients = [student.user.email]
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