# coding=utf-8
from datetime import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import TemplateView

from students.model.base import UserActivity
from students.view.common import TeachersView


class ActivityView(TeachersView):
    template_name = "activity/month.html"
    months = [
        u'Январь',
        u'Февраль',
        u'Март',
        u'Арпель',
        u'Май',
        u'Июнь',
        u'Июль',
        u'Август',
        u'Сентябрь',
        u'Октябрь',
        u'Ноябрь',
        u'Декабрь',
    ]

    def dispatch(self, request, *args, **kwargs):
        year = int(request.GET.get('year', datetime.now().year))
        month = int(request.GET.get('month', datetime.now().month))
        user_id = int(request.GET.get('user_id', request.user.id))
        user = get_user_model().objects.get(pk=user_id)
        activity = UserActivity.get_for_month(user, year, month)
        days = []
        for day in range(31):
            hours = []
            for hour in range(24):
                hour_index = day*24+hour
                hours.append(int(activity.activity[hour_index]))
            days.append(hours)
        context = {
            'days': days,
            'activity_user': user,
            'hours': range(24),
            'month': month,
            'month_name': self.months[month-1],
            'year': year,
            'next_page_year': year+1 if month == 12 else year,
            'next_page_month': 1 if month == 12 else month+1,
            'prev_page_year': year-1 if month == 1 else year,
            'prev_page_month': 12 if month == 1 else month-1,
        }
        return render(request, self.template_name, context)
