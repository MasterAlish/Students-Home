# coding=utf-8
import json

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from students.model.base import Mail


class StudentsMail(object):
    def report_new_file_resolution_uploaded(self, request, file_resolution):
        """
        :type file_resolution: students.model.base.FileResolution
        """
        subject = u"Новая лабораторка от %s" % unicode(file_resolution.student)
        link = unicode(request.META["HTTP_HOST"] + reverse("check_resolution", kwargs={'id': file_resolution.id}))
        message = u"Новая лабораторка от %s\n\n\"%s\"\n\nПерейдите по ссылке чтобы проверить решение http://%s" % \
                  (file_resolution.student, file_resolution.comment, link)
        message_html = u"Новая лабораторка от %s<br><br>\"%s\"<br><br>Перейдите по ссылке чтобы проверить решение " \
                       u"<a href=\"http://%s\">Перейти</a>" % \
                       (file_resolution.student, file_resolution.comment, link)
        recipients = map(lambda t: t.user.email, file_resolution.task.course.teachers.all())
        self.save_mail(subject, message, message_html, recipients)

    def report_homework_uploaded(self, request, homework):
        """
        :type homework: students.model.base.HomeworkSolution
        """
        link = unicode(request.META["HTTP_HOST"] + reverse("homeworks", kwargs={'id': homework.course.id}))
        subject = u"Домашнее задание от %s" % unicode(homework.student)
        message = u"Домашнее задание от %s\n\n\"%s\"\n\nПерейдите по ссылке чтобы скачать решение http://%s" % \
                  (homework.student, homework.comment, link)
        message_html = u"Домашнее задание от %s<br><br>\"%s\"<br><br>Перейдите по ссылке чтобы скачать решение " \
                       u"<a href=\"http://%s\">Перейти</a>" % \
                       (homework.student, homework.comment, link)
        recipients = map(lambda t: t.user.email, homework.course.teachers.all())
        self.save_mail(subject, message, message_html, recipients)

    def report_article_added(self, request, article):
        """
        :type article: students.model.blog.Article
        """
        link = unicode(request.META["HTTP_HOST"] + reverse("article", kwargs={'slug': article.slug}))
        subject = u"Новая статья от %s" % unicode(article.author.get_full_name())
        message = u"Новая статья от %s\n\nПерейдите по ссылке http://%s" % \
                  (article.author.get_full_name(), link)
        message_html = u"Новая статья от %s<br><br>Перейдите по ссылке " \
                       u"<a href=\"http://%s\">Перейти</a>" % \
                       (article.author.get_full_name(), link)
        recipients = [settings.EMAIL_ADMIN_EMAIL]
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
        link = unicode(request.META["HTTP_HOST"] + reverse("group", kwargs={'id': student.group_id}))
        message = u"Перейдите по ссылку чтобы активировать аккаунт студента http://%s " % link
        recipients = []
        for course in student.group.courses.all():
            for teacher in course.teachers.all():
                recipients.append(teacher.user.email)
        self.save_mail(subject, message, message, recipients)

    def teacher_registered(self, request, teacher):
        subject = u"Зарегистрировался новый учитель: %s" % unicode(teacher)
        message = u"Перейдите по ссылку чтобы активировать аккаунт учителя http://%s " % unicode(
            request.META["HTTP_HOST"] + "/admin/students/myuser/" + str(teacher.user.id))
        recipients = [settings.EMAIL_ADMIN_EMAIL]
        self.save_mail(subject, message, message, recipients)

    def inform_about_new_event(self, request, event):
        subject = u"Новое событие в приложении Аиды"
        message = u"Перейдите по ссылку чтобы просмотреть все события %s " % unicode(
            request.META["HTTP_HOST"] + "/admin/events/event/")
        recipients = [settings.EMAIL_ADMIN_EMAIL]
        self.save_mail(subject, message, message, recipients)

    def inform_about_new_medal(self, student, medal, course, request):
        """
        :type student: students.model.base.Student
        :type medal: students.model.base.Medal
        :type course: students.model.base.Course
        """
        subject = u"У вас новая медаль!"
        message = u"Уважаемый, %s, поздравляем вас с новой медалью \"%s\"! Перейдите по ссылке чтобы просмотреть свои медали http://%s " % \
                  (student.user.get_full_name(), medal.name,
                   unicode(request.META["HTTP_HOST"] + reverse('marks', kwargs={'id': course.id})))
        recipients = [student.user.email]
        self.save_mail(subject, message, message, recipients)

    def report_account_activated(self, student, request):
        """
        :type student: students.model.base.Student
        """
        subject = u"Ваш аккаунт активирован!"
        message = u"Уважаемый, %s, ваш аккаунт на сайте http://%s успешно активирован!" % \
                  (student.user.get_full_name(), unicode(request.META["HTTP_HOST"]))
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
