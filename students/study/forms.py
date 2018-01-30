# coding=utf-8
from django import forms


class QuizScoreForm(forms.Form):
    score = forms.FloatField(required=True, label=u"Оценка")
    comment = forms.CharField(required=False, label=u"Комментарий", widget=forms.Textarea)