# coding=utf-8
from students.forms import UserCreateForm
from django.contrib import messages
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View

from students.model.base import Student
from students.models import MyUser


def on_error(request):
    return render(request, "students/500.html")


def on_not_found(request):
    return render(request, "students/404.html")


def auth_logout(request):
    logout(request)
    return redirect(reverse("home"))


def auth_profile(request):
    return redirect(reverse("home"))


def create_user(form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = MyUser.objects.create_user(email, password)
    user.fullname = form.cleaned_data['name']
    user.phone = form.cleaned_data['phone']
    user.date_of_birth = form.cleaned_data['birthdate']
    user.save()
    student = Student(user=user)
    student.group = form.cleaned_data['group']
    student.save()


def auth_register(request):
    template_name = "registration/register.html"
    context = {}
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            create_user(form)
            messages.success(request, _(u"Регистрация прошла успешно! Войдите используя свой email и пароль."))
            return redirect(reverse("home"))

    context['form'] = form
    return render(request, template_name, context=context)


class HomeView(TemplateView):
    template_name = "students/home.html"

    def dispatch(self, request, *args, **kwargs):
        context = {

        }

        return render(request, self.template_name, context)
