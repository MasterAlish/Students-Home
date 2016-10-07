# coding=utf-8
import zipfile

from ckeditor.fields import RichTextFormField
from django import forms
from django.forms import ModelForm, Form

from students.model.base import Solution


class SolutionUploadForm(ModelForm):
    class Meta:
        fields = ['file', 'comment']
        model = Solution


class EmailForm(Form):
    subject = forms.CharField(label=u"Тема", required=True, strip=True)
    body = RichTextFormField(config_name='long', required=True, label=u"Сообщение")