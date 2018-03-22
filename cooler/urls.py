#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from cooler.views import CoolerView, SoldierAndTankView, PuzzlesView, PuzzleView, ExercisesView, ExerciseView, \
    ExerciseSubmissionsView

urlpatterns = [
    url(r'^$', CoolerView.as_view(), name='cooler'),
    url(r'^soldier_and_tank/$', login_required(SoldierAndTankView.as_view()), name='soldier_and_tank'),
    url(r'^puzzles/$', PuzzlesView.as_view(), name='puzzles'),
    url(r'^puzzles/(?P<slug>[\d\w_-]+)/$', PuzzleView.as_view(), name='puzzle'),
    url(r'^exercises/$', login_required(ExercisesView.as_view()), name='exercises'),
    url(r'^exercises/(?P<id>\d+)/$', login_required(ExerciseView.as_view()), name='exercise'),
    url(r'^exercises/submissions/$', login_required(ExerciseSubmissionsView.as_view()), name='exercise_submissions'),
]