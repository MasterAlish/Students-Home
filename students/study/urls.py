#coding: utf-8
from django.conf.urls import url, include

from students.study.views import TestView, TestResultView, DeleteTestResultView, QuizListView, QuizView

urlpatterns = [
    url(r'^quiz/$', QuizListView.as_view(), name='all_quizes'),
    url(r'^quiz/(?P<id>\d+)/$', QuizView.as_view(), name='quiz'),

    url(r'^test/(?P<task_id>\d+)/$', TestView.as_view(), name='start_quiz'),
    url(r'^test/(?P<task_id>\d+)/results/$', TestResultView.as_view(), name='quiz_results'),
    url(r'^test/results/(?P<id>\d+)/delete/$', DeleteTestResultView.as_view(), name='delete_quiz_result'),
]

