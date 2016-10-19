# coding=utf-8
import zipfile

from ckeditor.fields import RichTextFormField
from django import forms
from django.forms import ModelForm, Form

from students.model.base import Solution, Medal


class SolutionUploadForm(ModelForm):
    class Meta:
        fields = ['file', 'comment']
        model = Solution


class EmailForm(Form):
    subject = forms.CharField(label=u"Тема", required=True, strip=True)
    body = RichTextFormField(config_name='long', required=True, label=u"Сообщение")


class MedalForm(Form):
    medal = forms.ModelChoiceField(queryset=Medal.objects.all(), label=u"Медаль", required=True)


class GroupStudentsForm(Form):
    def __init__(self, group):
        super(GroupStudentsForm, self).__init__()
        self.group = group
        for student in group.students.all():
            self.fields[self.field_name(student)] = forms.BooleanField(label=student.name, required=False)

    def select_all_button(self):
        all_script = u""
        none_script = u""
        for student in self.group.students.all():
            id = u"id_%s" % self.field_name(student)
            all_script += u"%s.checked = true; " % id
            none_script += u"%s.checked = false; " % id
        return u"<a href='#' class='select-all group%d' value='%s' onclick='%s;return false;'><span class='fa fa-circle'></span></a> " \
               u"<a href='#' class='select-all group%d' value='%s' onclick='%s;return false;'><span class='fa fa-circle-o'></span></a>" \
               % (self.group.id, u"Выбрать всех", all_script, self.group.id, u"Выбрать всех", none_script)

    def get_selected(self, DATA):
        selected = []
        for student in self.group.students.all():
            field_name = self.field_name(student)
            if DATA.get(field_name, False):
                selected.append(student)
        return selected

    def field_name(self, student):
        return u'group_%d_student_%d' % (self.group.id, student.id)

