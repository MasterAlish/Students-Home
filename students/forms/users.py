# coding=utf-8
from django.contrib.auth import get_user_model
from django.forms import TextInput

from students.model.base import Group
from students.models import MyUser
from students.simplemathcaptcha.fields import MathCaptchaField
from django import forms
from django.utils.translation import ugettext as _

from students.simplemathcaptcha.widgets import MyDateInput


class UserCreateForm(forms.Form):
    name = forms.CharField(min_length=4, label=_(u"ФИО"))
    email = forms.EmailField(label=_(u"Email"))
    birthdate = forms.DateField(label=_(u"Дата рождения"), widget=TextInput)
    phone = forms.CharField(label=_(u"Номер телефона"))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput, label=_(u"Пароль"), required=False)
    password2 = forms.CharField(min_length=4, widget=forms.PasswordInput, label=_(u"Пароль (еще раз)"), required=False)
    captcha = MathCaptchaField(label=_(u"Проверка адекватности"))

    main_fields = ['name', 'email', 'password', 'password2']

    def __init__(self, data=None, editing=False, initial=None):
        super(UserCreateForm, self).__init__(data=data, initial=initial)
        self.editing = editing

    def clean(self):
        super(UserCreateForm, self).clean()
        password1 = self.data['password']
        password2 = self.data['password2']
        if password2 != password1:
            self.add_error("password2", _(u"Пароли не совпадают"))
        if not self.editing and len(password1.strip()) == 0:
            self.add_error("password", _(u"Введите пароль"))
        if not self.editing:
            self.check_uniqueness()

    def check_uniqueness(self):
        User = get_user_model()
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).count() > 0:
                self.add_error("email", _(u"Такой email уже зарегистрирован в системе"))


class StudentCreateForm(UserCreateForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label=_(u"Группа"))


class UserChangeForm(forms.ModelForm):
    date_of_birth = forms.DateField(label=_(u"Дата рождения"), widget=MyDateInput)
    email = forms.EmailField(label=_(u"Email"))
    avatar = forms.ImageField(label=_(u"Загрузить новую аватарку"), required=False)

    def __init__(self, data=None, files=None, instance=None, has_avatar=False):
        super(UserChangeForm, self).__init__(data=data, files=files, instance=instance)
        if not has_avatar:
            del self.fields['avatar']

    class Meta:
        model = MyUser
        fields = ('fullname', 'phone', 'email', 'date_of_birth',)