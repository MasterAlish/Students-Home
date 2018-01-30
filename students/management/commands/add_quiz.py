# coding=utf-8
import os

from django.conf import settings
from django.core.management import BaseCommand

from students.mail import StudentsMail
from students.management.commands.tests import Type
from students.model.base import FileResolution, Quiz, QuizQuestion, QuizAnswer, Subject
from students.model.checks import ZipContainsFileConstraint

preextra = [
    {
        'question': u'Как тебя зовут? Как дела?',
        'type': Type.Text,
        'answers': [
            '___________________________________________________________________________________________________'
        ]
    },
]

postextra = [
    {
        'question': u'Что ты приобрел(-а) или узнал(-а) нового для себя этот курс?',
        'type': Type.BigText,
        'answers': [
            '___________________________________________________________________________________________________',
            '___________________________________________________________________________________________________',
            '___________________________________________________________________________________________________',
        ]
    }, {
        'question': u'Какие есть пожелания или мысли?',
        'type': Type.Text,
        'answers': [
            '___________________________________________________________________________________________________'
        ]
    },
]

from students.management.commands.tests import get_random_questions, Type
from students.management.commands.tests.android import questions as android_quiz
from students.management.commands.tests.java_basic import questions as java_quiz
from students.management.commands.tests.java_forms import questions as jframes_quiz
from students.management.commands.tests.python import questions as python_quiz
from students.management.commands.tests.django import questions as django_quiz
from students.management.commands.tests.web import questions as web_quiz
from students.management.commands.tests.funny import questions as funny_quiz


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create(None, u"Начальные вопросы", preextra)
        self.create(None, u"Конечные вопросы", postextra)
        self.create(u"Веб-программирование", u"Основы Веб", web_quiz)
        self.create(u"Веб-программирование", u"Основы Python", python_quiz)
        self.create(u"Веб-программирование", u"Основы фреймворка Django", django_quiz)
        self.create(None, u"Веселые вопросы", funny_quiz)
        self.create(u"Java", u"Основы Java", java_quiz)
        self.create(u"Java", u"Основы Android", android_quiz)
        self.create(u"Java", u"Java: JFrames", jframes_quiz)

    def create(self, subject_name, name, questions):
        subject = None
        if subject_name:
            (subject, created) = Subject.objects.get_or_create(name=subject_name)
        (quiz, created) = Quiz.objects.get_or_create(name=name, subject=subject)
        for question in questions:
            ques = QuizQuestion.objects.create(quiz=quiz, type=question['type'], text=question['question'])
            if ques.type in [Type.Single, Type.Multiple]:
                for answer in question['answers']:
                    type = "wrong"
                    if answer.startswith("##"):
                        type = "right"
                        answer = answer[2:]
                    if answer.startswith("**"):
                        type = "optional"
                        answer = answer[2:]
                    QuizAnswer(question=ques, text=answer, type=type).save()
