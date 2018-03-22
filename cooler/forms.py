# coding=utf-8
from django.forms import Form
from django import forms


class SubmitExerciseForm(Form):
    code = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100, 'placeholder': 'class Solution {\n...\n}'}), label=u"Код")