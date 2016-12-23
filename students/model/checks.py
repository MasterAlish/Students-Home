# coding=utf-8
import os
import re
import zipfile

from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class UploadConstraint(PolymorphicModel):
    task = models.ForeignKey("LabTask", verbose_name=_(u"Лабораторная работа"), related_name="constraints")

    def test(self, resolution):
        return True, u""

    def __unicode__(self):
        return u"%s" % self.task


class FileSizeConstraint(UploadConstraint):
    max_size = models.CharField(max_length=100, verbose_name=_(u"Максимальный размер файла"), default="5M", help_text=_(u"Форматы: 12K, 300B, 5M"))
    min_size = models.CharField(max_length=100, verbose_name=_(u"Миниимальный размер файла"), null=True, blank=True)

    def test(self, resolution):
        file_info = os.stat(resolution.file.path)
        max_bytes = self.get_max_bytes()
        if file_info.st_size > max_bytes:
            return False, _(u"Файл должен быть не больше %s (%d B)") % (self.max_size, max_bytes)
        return True, u""

    def get_max_bytes(self):
        mb = re.compile("^(\d+)[Mm]$")
        kb = re.compile("^(\d+)[Kk]$")
        b = re.compile("^(\d+)[Bb]$")
        if mb.match(self.max_size):
            return 1024L * 1024L * long(mb.match(self.max_size).group(1))
        if kb.match(self.max_size):
            return 1024L * long(kb.match(self.max_size).group(1))
        if b.match(self.max_size):
            return long(b.match(self.max_size).group(1))
        return 1024L*1024L*5L

    def __unicode__(self):
        return u"%s %s - %s" % (self.task, self.min_size or "0", self.max_size)


class FileNameConstraint(UploadConstraint):
    extension = models.CharField(max_length=20, verbose_name=_(u"Требуемое расширение файла"), null=True, blank=True, help_text=_(u"Оставьте пустым, если нет ограничений"))
    file_name = models.CharField(max_length=255, verbose_name=_(u"Требуемое название файла"), null=True, blank=True, help_text=_(u"Оставьте пустым, если нет ограничений"))

    def test(self, resolution):
        if self.extension:
            if not resolution.file.name.endswith("."+self.extension):
                return False, _(u"Файл должен иметь расширение .%s") % self.extension
        if self.file_name:
            if not resolution.file.name.startswith(self.file_name):
                return False, _(u"Файл должен иметь название %s") % self.file_name
        return True, u""

    def __unicode__(self):
        return u"%s %s %s" % (self.task, self.file_name or "*", self.extension or "*")


class ZipFileConstraint(UploadConstraint):
    def test(self, resolution):
        return ZipFileConstraint.test_zip(resolution)

    @staticmethod
    def test_zip(resolution):
        if not zipfile.is_zipfile(resolution.file.path):
            return False, _(u"Файл должен быть .zip архивом")
        files = zipfile.ZipFile(resolution.file.path).filelist
        not_ascii_file_name = None

        for file in files:
            if not is_ascii(file.filename):
                not_ascii_file_name = file.filename
                break
        if not_ascii_file_name:
            return False, _(u"В архиве есть файл с неправильным названием %s. Все файлы должны быть названы латинскими буквами.") % not_ascii_file_name.decode('utf-8', 'ignore')
        return True, u""


class ZipContainsFileConstraint(UploadConstraint):
    file_names = models.CharField(max_length=1000, verbose_name=_(u"Какие файлы должен содержать zip-архив"), help_text=_(u"Введите название файлов через запятую"))

    def test(self, resolution):
        valid, message = ZipFileConstraint.test_zip(resolution)
        if not valid:
            return valid, message
        files = zipfile.ZipFile(resolution.file.path).filelist

        existing_files = set([])
        for file in files:
            existing_files.add(file.filename)

        not_existing_files = []
        for file_name in self.file_names.split(","):
            if not file_name.strip() in existing_files:
                not_existing_files.append(file_name)

        if len(not_existing_files) > 0:
            return False, u"В корне архива должны быть следующие файлы %s" % unicode(not_existing_files)
        return True, u""

    def __unicode__(self):
        return u"%s wis files [%s]" % (self.task, self.file_names)