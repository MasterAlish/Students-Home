# coding=utf-8
import zipfile

from ckeditor.fields import RichTextFormField
from django import forms
from django.forms import ModelForm, Form

from students.model.base import Medal, FileResolution


class FileResolutionUploadForm(ModelForm):
    class Meta:
        fields = ['file', 'comment']
        model = FileResolution


class EmailForm(Form):
    subject = forms.CharField(label=u"Тема", required=True, strip=True)
    body = RichTextFormField(config_name='long', required=True, label=u"Сообщение")


class MedalForm(Form):
    medal = forms.ModelChoiceField(queryset=Medal.objects.all(), label=u"Медаль", required=True)


class GroupStudentsSelectForm(Form):
    def __init__(self, group):
        super(GroupStudentsSelectForm, self).__init__()
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


class StudentException(Exception):
    def __init__(self, field, error):
        super(StudentException, self).__init__()
        self.field = field
        self.error = error


class GroupStudentsInputForm(Form):
    def __init__(self, group):
        super(GroupStudentsInputForm, self).__init__()
        self.group = group
        for student in group.students.all():
            self.fields[self.field_name(student)] = forms.CharField(label=student.name, required=False)

    def set_vals(self, DATA):
        values = {}
        for student in self.group.students.all():
            field_name = self.field_name(student)
            value = DATA.get(field_name, None)
            if value:
                self.initial[field_name] = value

    def get_ints(self, DATA):
        values = {}
        for student in self.group.students.all():
            field_name = self.field_name(student)
            value = DATA.get(field_name, None)
            if value:
                try:
                    values[student] = int(value.strip())
                except:
                    raise StudentException(field_name, u"Значение должно быть целым числом")
        return values

    def field_name(self, student):
        return u'group_%d_student_%d' % (self.group.id, student.id)

    def add_error(self, field, error):
        self.errors[field] = error

