# coding=utf-8
from django import forms
from django.forms import Form


class AddProblemForm(Form):
    problem_url = forms.CharField(required=True)


class JudgeIdForm(Form):
    judge_id = forms.CharField(required=True)


class SubmitProblemForm(Form):
    language = forms.ChoiceField(required=True, choices=[
        ['32', "Java 1.8"],
        ['34', "Python 2.7"],
        ['35', "Python 3.4"],
        ['18', "Ruby 1.9"],
        ['33', "Scala 2.11"],
        ['43', "Rust 1.9"],
    ], label=u"Язык")
    body = forms.CharField(required=True, label=u"Код решения", widget=forms.Textarea(attrs={'style': 'width: 100%; height: 300px; font-family:monospace; font-size:12px;'}))