#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt

from students.api.articles import GetArticlesApi, ReadArticleApi, GetArticleApi
from students.api.auth import LoginApi
from students.api.courses import CoursesApi
from students.api.feedback import FeedbackApi

urlpatterns = [
    url(r'^articles$', GetArticlesApi.as_view()),
    url(r'^article/info$', csrf_exempt(GetArticleApi.as_view())),
    url(r'^article$', ReadArticleApi.as_view()),
    url(r'^login$', csrf_exempt(LoginApi.as_view())),
    url(r'^courses$', CoursesApi.as_view()),
    url(r'^feedback$', csrf_exempt(FeedbackApi.as_view())),
]
