# coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from contest.views import AddProblemView, ProblemsView, ProblemPage, SubmitPage, RegisterAcmView, ContestHomeView, \
    SubmitsView

urlpatterns = [
    url(r'^$', login_required(ContestHomeView.as_view()), name="contest"),
    url(r'^problems/add/$', login_required(AddProblemView.as_view()), name="add_problem"),
    url(r'^problems/$', login_required(ProblemsView.as_view()), name="all_problems"),
    url(r'^problems/(?P<id>\d+)$', login_required(ProblemPage.as_view()), name="problem"),
    url(r'^problems/(?P<id>\d+)/submit/$', login_required(SubmitPage.as_view()), name="submit_problem"),
    url(r'^register-acm/$', login_required(RegisterAcmView.as_view()), name="register_acm"),
    url(r'^submits/$', login_required(SubmitsView.as_view()), name="submits"),
]
