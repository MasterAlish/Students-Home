from django.utils.deprecation import MiddlewareMixin

from students.view.common import is_teacher, is_student


def students(request):
    return {
        'is_teacher': is_teacher(request.user),
        'is_student': is_student(request.user)
    }