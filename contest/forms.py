# coding=utf-8
from django import forms
from django.forms import Form, ModelForm

from contest.models import Contest


class AddProblemForm(Form):
    problem_url = forms.CharField(required=True)


class AddContestForm(ModelForm):
    class Meta:
        model = Contest
        exclude = []


class JudgeIdForm(Form):
    judge_id = forms.CharField(required=True)


class SubmitProblemForm(Form):
    language = forms.ChoiceField(required=True, choices=[
        ['32', "Java 1.8"],
        ['34', "Python 2.7"],
        ['48', "Python 3.4"],
        ['18', "Ruby 1.9"],
        ['33', "Scala 2.11"],
        ['43', "Rust 1.9"],
        ['40', "Visual C++ 2017"],
        ['41', "Visual C# 2017"],
        ['49', "Kotlin 1.1.4"],
    ], label=u"Язык")
    body = forms.CharField(required=True, label=u"Код решения", widget=forms.Textarea(attrs={'style': 'width: 100%; height: 300px; font-family:monospace; font-size:12px;'}))
