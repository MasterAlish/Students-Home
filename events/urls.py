#coding: utf-8
from django.conf.urls import url
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt

from events.views import RegisterEventView

urlpatterns = [
    url(r'^register/$', csrf_exempt(RegisterEventView.as_view())),
]
