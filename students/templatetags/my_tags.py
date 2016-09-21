# coding=utf-8
from django import template
from hashlib import md5
from django.utils import translation
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