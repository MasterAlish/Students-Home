#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from cooler.views import CoolerView, SoldierAndTankView

urlpatterns = [
    url(r'^$', CoolerView.as_view(), name='cooler'),
    url(r'^soldier_and_tank/$', login_required(SoldierAndTankView.as_view()), name='soldier_and_tank'),
]