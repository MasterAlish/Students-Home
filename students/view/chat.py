# coding=utf-8
import json
from httplib import HTTPResponse

from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from students.mobile import is_mobile
from students.model.base import Course, ChatMessage, LastReadMessage
from students.view.common import StudentsAndTeachersView, user_authorized_to_course


class ChatDateMixin(object):
    def add_dates(self, messages, last_message_id=None):
        try:
            prev_message = ChatMessage.objects.get(pk=last_message_id)
        except:
            prev_message = None
        messages_with_dates = []
        for message in messages:
            if prev_message is None or prev_message and prev_message.datetime.date() < message.datetime.date():
                messages_with_dates.append(message.datetime.strftime("%d.%m.%Y"))
            messages_with_dates.append(message)
            prev_message = message

        return messages_with_dates


class ChatView(StudentsAndTeachersView, ChatDateMixin):
    template_name = "chat/chat.html"
    template_name_mobile = "chat/chat_mobile.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course):
            self.context['course'] = course
            if request.method == 'POST':
                message = request.POST.get("message", "").strip()
                if len(message) > 0:
                    message = ChatMessage(body=message, user=request.user, course=course)
                    message.save()
                    return redirect(reverse("chat", kwargs={'id': course.id}))
            messages = ChatMessage.objects.filter(course=course).order_by("-datetime")[:50]
            self.context['messages'] = self.add_dates(reversed(messages))
            last_message_id = messages.first().id if messages.count() > 0 else 0
            self.context['last_message_id'] = last_message_id
            LastReadMessage.register_last_message(course, request.user, last_message_id)
            if is_mobile(request):
                return render(request, self.template_name_mobile, self.context)
            else:
                return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class NewMessagesView(StudentsAndTeachersView, ChatDateMixin):
    template_name = "chat/messages.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=request.GET.get("course_id"))
        if user_authorized_to_course(request.user, course):
            last_message_id = request.GET.get("last_message_id") or 0
            messages = ChatMessage.objects.filter(course=course, pk__gt=last_message_id).order_by("datetime")
            self.context['messages'] = self.add_dates(messages, last_message_id)
            self.context['current_user'] = request.user
            last_message_id = messages.last().id if messages.count() > 0 else last_message_id
            LastReadMessage.register_last_message(course, request.user, last_message_id)
            return HttpResponse(content=json.dumps({
                'last_message_id': last_message_id,
                'new_messages': render_to_string(self.template_name, self.context) if len(messages) > 0 else ""
            }), content_type="application/json")
        raise Exception(u"User is not authenticated")


class PostMessageView(StudentsAndTeachersView, ChatDateMixin):
    template_name = "chat/messages.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=request.POST.get("course_id"))
        if user_authorized_to_course(request.user, course):
            message = request.POST.get("message", "").strip()
            if len(message) > 0:
                message = ChatMessage(body=message, user=request.user, course=course)
                message.save()
            last_message_id = request.POST.get("last_message_id") or 0
            messages = ChatMessage.objects.filter(course=course, pk__gt=last_message_id).order_by("datetime")
            self.context['messages'] = self.add_dates(messages, last_message_id)
            self.context['current_user'] = request.user
            last_message_id = messages.last().id if messages.count() > 0 else last_message_id
            LastReadMessage.register_last_message(course, request.user, last_message_id)
            return HttpResponse(content=json.dumps({
                'last_message_id': last_message_id,
                'new_messages': render_to_string(self.template_name, self.context)
            }), content_type="application/json")
        raise Exception(u"User is not authenticated")