# coding=utf-8
import os

from django import template
from hashlib import md5

from django.conf import settings
from django.utils import translation
from html2text import html2text

from students.model.base import Student, Teacher, FileResolution, Resolution, LastReadMessage

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
def has_url(resolution):
    return isinstance(resolution, FileResolution)


@register.filter
def url_for_file_resolution(resolution):
    labname = "lab%d" % resolution.task.number
    username = resolution.student.get_short_name()
    labpath = os.path.join(settings.MEDIA_URL, "sites", labname, username, "index.html")
    return labpath


@register.filter
def resolutions_for_task(resolutions_map, task):
    if task.id in resolutions_map:
        return resolutions_map[task.id]
    else:
        return {}


@register.assignment_tag
def best_solution_of(resolutions_for_task, student):
    if student.id in resolutions_for_task:
        resolutions = resolutions_for_task[student.id]
        return get_best_resolution(resolutions)
    else:
        return None


def get_best_resolution(resolutions):
    best = resolutions[0]
    for resolution in resolutions:
        if best.mark < resolution.mark:
            best = resolution
    return best


@register.filter
def medals_of(medals_by_students, student):
    if student.id in medals_by_students:
        return medals_by_students[student.id]
    else:
        return []


@register.assignment_tag
def get_unread_chats(user):
    courses = []
    if is_teacher(user):
        courses = user.teacher.courses.all()
    elif is_student(user):
        courses = user.student.courses
    total = 0
    course_chats = []
    for course in courses:
        count = LastReadMessage.get_unread_messages_count(course=course, user=user)
        course_chats.append({
            'id': course.id,
            'name': course.name,
            'unread_count': "50+" if count > 50 else (count or '')
        })
        total += count
    return {
        'total': "50+" if total > 50 else (total or ''),
        'courses': course_chats
    }


@register.filter
def min_length(data, req_length):
    length = len(str(data))
    if length < req_length:
        return "0" * (req_length - length) + str(data)
    else:
        return data


@register.filter
def get(collection, index):
    if index in collection:
        return collection[index]
    return None
