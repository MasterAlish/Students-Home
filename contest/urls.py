# coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from contest.views import AddProblemView, ProblemsView, ProblemPage, SubmitPage, RegisterAcmView, ContestHomeView, \
    SubmitsView, ContestsView, AddContestView, ContestView, DeleteContestView, RanklistView

urlpatterns = [
    url(r'^$', login_required(ContestHomeView.as_view()), name="contests"),
    url(r'^problems/add/$', login_required(AddProblemView.as_view()), name="add_problem"),
    url(r'^problems/$', login_required(ProblemsView.as_view()), name="all_problems"),
    url(r'^problems/(?P<id>\d+)$', login_required(ProblemPage.as_view()), name="problem"),
    url(r'^problems/(?P<id>\d+)/submit/$', login_required(SubmitPage.as_view()), name="submit_problem"),
    url(r'^contests/$', login_required(ContestsView.as_view()), name="all_contests"),
    url(r'^contests/add/$', login_required(AddContestView.as_view()), name="add_contest"),
    url(r'^contests/(?P<id>\d+)/$', login_required(ContestView.as_view()), name="contest"),
    url(r'^contests/(?P<id>\d+)/delete/$', login_required(DeleteContestView.as_view()), name="delete_contest"),
    url(r'^register-acm/$', login_required(RegisterAcmView.as_view()), name="register_acm"),
    url(r'^submits/$', login_required(SubmitsView.as_view()), name="submits"),
    url(r'^ranklist/$', login_required(RanklistView.as_view()), name="ranklist"),
]
