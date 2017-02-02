#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.views import login

from students.api.articles import GetArticlesApi, ReadArticleApi

urlpatterns = [
    url(r'^articles/$', GetArticlesApi.as_view()),
    url(r'^article/$', ReadArticleApi.as_view()),
]