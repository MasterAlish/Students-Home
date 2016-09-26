# coding=utf-8
import json
from httplib import HTTPResponse

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView

from students.mobile import is_mobile
from students.model.base import Course, ChatMessage
from students.view.common import StudentsAndTeachersView, user_authenticated_to_course

# TODO: Сделать всякие награды, медали для студентов


class ChatView(StudentsAndTeachersView):
    template_name = "chat/chat.html"
    template_name_mobile = "chat/chat_mobile.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['id'])
        if user_authenticated_to_course(request.user, course):
            self.context['course'] = course
            if request.method == 'POST':
                message = request.POST.get("message", "").strip()
                if len(message) > 0:
                    message = ChatMessage(body=message, user=request.user, course=course)
                    message.save()
                    return redirect(reverse("chat", kwargs={'id': course.id}))
            messages = ChatMessage.objects.filter(course=course).order_by("-datetime")[:50]
            self.context['messages'] = reversed(messages)
            self.context['last_message_id'] = messages.first().id if messages.count() > 0 else 0
            if is_mobile(request):
                return render(request, self.template_name_mobile, self.context)
            else:
                return render(request, self.template_name, self.context)
        raise Exception(u"User is not authenticated")


class NewMessagesView(StudentsAndTeachersView):
    template_name = "chat/messages.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=request.GET.get("course_id"))
        if user_authenticated_to_course(request.user, course):
            last_message_id = request.GET.get("last_message_id")
            messages = ChatMessage.objects.filter(course=course, pk__gt=last_message_id).order_by("datetime")
            self.context['messages'] = messages
            self.context['current_user'] = request.user
            last_message_id = messages.last().id if messages.count() > 0 else last_message_id
            return HttpResponse(content=json.dumps({
                'last_message_id': last_message_id,
                'new_messages': render_to_string(self.template_name, self.context)
            }), content_type="application/json")
        raise Exception(u"User is not authenticated")


class PostMessageView(StudentsAndTeachersView):
    template_name = "chat/messages.html"

    def handle(self, request, *args, **kwargs):
        course = Course.objects.get(pk=request.POST.get("course_id"))
        if user_authenticated_to_course(request.user, course):
            message = request.POST.get("message", "").strip()
            if len(message) > 0:
                message = ChatMessage(body=message, user=request.user, course=course)
                message.save()

            last_message_id = request.POST.get("last_message_id")
            messages = ChatMessage.objects.filter(course=course, pk__gt=last_message_id).order_by("datetime")
            self.context['messages'] = messages
            self.context['current_user'] = request.user
            last_message_id = messages.last().id if messages.count() > 0 else last_message_id
            return HttpResponse(content=json.dumps({
                'last_message_id': last_message_id,
                'new_messages': render_to_string(self.template_name, self.context)
            }), content_type="application/json")
        raise Exception(u"User is not authenticated")