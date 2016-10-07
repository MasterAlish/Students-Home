# coding=utf-8
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.core.mail import send_mail

from students.forms.users import UserCreateForm, UserChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View

from students.mail import StudentsMail
from students.model.base import Student
from students.models import MyUser
from students.view.common import is_student, is_teacher


def on_error(request):
    return render(request, "students/500.html")


def on_not_found(request):
    return render(request, "students/404.html")


def auth_logout(request):
    logout(request)
    return redirect(reverse("home"))


def auth_profile(request):
    return render(request, "registration/profile.html")


def create_student(form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = MyUser.objects.create_user(email, password)
    user.fullname = form.cleaned_data['name']
    user.phone = form.cleaned_data['phone']
    user.date_of_birth = form.cleaned_data['birthdate']
    user.is_active = False
    user.save()
    student = Student(user=user)
    student.group = form.cleaned_data['group']
    student.save()
    return student


def auth_register(request):
    template_name = "registration/register.html"
    context = {}
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            student = create_student(form)
            messages.success(request, _(u"Регистрация прошла успешно! После проверки ваш аккаунт станет доступным."))
            StudentsMail().student_registered(request, student)
            return redirect(reverse("home"))

    context['form'] = form
    return render(request, template_name, context=context)


def reset_password(request):
    template_name = "registration/form.html"
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save(request=request, from_email=settings.DEFAULT_FROM_EMAIL)
            messages.success(request, u"Ссылка на восстановление пароля была отправлена на указанную почту")
            return redirect(reverse("login"))
    context = {
        'form': form,
        'title': _(u'Восстановить пароль')
    }
    return render(request, template_name, context=context)


def password_change(request):
    template_name = "registration/form.html"
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u"Пароль успешно изменен! Войдите снова используя новый пароль")
            return redirect(reverse("login"))
    context = {
        'form': form,
        'title': _(u'Изменить пароль')
    }
    return render(request, template_name, context=context)


def user_change(request):
    template_name = "registration/form.html"
    has_avatar = is_student(request.user) or is_teacher(request.user)
    form = UserChangeForm(instance=request.user, has_avatar=has_avatar)
    if request.method == 'POST':
        form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES, has_avatar=has_avatar)
        if form.is_valid():
            form.save()
            if 'avatar' in form.cleaned_data and form.cleaned_data['avatar']:
                avatar = form.cleaned_data['avatar']
                if is_student(request.user):
                    request.user.student.avatar = avatar
                    request.user.student.save()
                if is_teacher(request.user):
                    request.user.teacher.avatar = avatar
                    request.user.teacher.save()
            messages.success(request, u"Данные успешно изменены!")
            return redirect(reverse("profile"))
    context = {
        'form': form,
        'title': _(u'Изменить данные')
    }
    return render(request, template_name, context=context)


class HomeView(TemplateView):
    template_name = "students/home.html"

    def dispatch(self, request, *args, **kwargs):
        context = {

        }

        return render(request, self.template_name, context)
