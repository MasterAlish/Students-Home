# coding=utf-8
import os

from django import template
from hashlib import md5

from django.conf import settings
from django.utils import translation
from html2text import html2text

from students.model.base import Student, Teacher

register = template.Library()


@register.filter
def l6e(instance, attr):
    if not instance:
        return ""
    lang = translation.get_language()
    ky = instance.__getattribute__(attr)
    ru = instance.__getattribute__(attr+"_ru")
    if ky and lang == 'ky':
        return ky
    if ru and lang == 'ru':
        return ru
    else:
        return ky or ru


def convert_tag(tag):
    if tag == 'error':
        return 'danger'
    return tag


@register.filter
def gravatar(email):
    return "https://www.gravatar.com/avatar/%s?d=monsterid&s=256" % md5(email).hexdigest()


@register.filter
def bootstrapize(tags, prefix=""):
    result = ""
    if isinstance(tags, list):
        for tag in tags:
            result += prefix + convert_tag(tag)
    else:
        result += prefix + convert_tag(tags)
    return result


@register.filter
def is_student(user):
    try:
        return Student.objects.filter(user=user).count() > 0
    except:
        return False


@register.filter
def is_teacher(user):
    try:
        return Teacher.objects.filter(user=user).count() > 0
    except:
        return False


@register.filter
def url_for_file_resolution(tabtask, student):
    labname = "lab%d" % tabtask.number
    username = student.get_short_name()
    labpath = os.path.join(settings.MEDIA_URL, "sites", labname, username, "index.html")
    return labpath


@register.filter
def resolutions_for_lab(resolutions_map, lab):
    if lab.id in resolutions_map:
        return resolutions_map[lab.id]
    else:
        return {}


@register.filter
def for_student(resolutions_for_lab, student):
    if student.id in resolutions_for_lab:
        return resolutions_for_lab[student.id]
    else:
        return []


@register.filter
def best_mark_of_student(resolutions_for_lab, student):
    if student.id in resolutions_for_lab:
        resolutions = resolutions_for_lab[student.id]
        return get_best_resolution(resolutions).mark
    else:
        return 0


def get_best_resolution(resolutions):
    best = resolutions[0]
    for resolution in resolutions:
        if best.mark < resolution.mark:
            best = resolution
    return best


@register.filter
def comment_of_student(resolutions_for_lab, student):
    if student.id in resolutions_for_lab:
        resolutions = resolutions_for_lab[student.id]
        return get_best_resolution(resolutions).comment
    else:
        return u"Нет комментариев"


@register.filter
def medals_of(medals_by_students, student):
    if student.id in medals_by_students:
        return medals_by_students[student.id]
    else:
        return []
