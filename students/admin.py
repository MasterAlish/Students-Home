# coding=utf-8
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as UserGroup

from students.adminactions import unpack_zip_with_index
from students.model.base import Teacher, Student, Course, Group as StudentGroup, Lecture, ChatMessage, \
    Medal, StudentMedal, LabTask, Task, Resolution, FileResolution, UserActivity, ExtraStudent, Todo, Point, \
    HomeWorkSolution, University, Department, Mail, Quiz, QuizAnswer, QuizQuestion, QuizResult, Subject, MustKnowGroup, \
    MustKnow, AlreadyKnow
from students.model.blog import Article
from students.model.checks import FileSizeConstraint, FileNameConstraint, ZipContainsFileConstraint, ZipFileConstraint
from students.model.extra import Feedback
from students.models import MyUser, UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'fullname', 'phone', 'date_of_birth', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'phone', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('-id', 'email', 'is_active')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(UserGroup)

admin.site.register(Teacher)


class StudentAdmin(ModelAdmin):
    list_display = ['name', 'group', 'user']
    ordering = ['group', 'user']


class ResolutionAdmin(ModelAdmin):
    list_display = ['datetime', 'student', 'task', 'mark', 'index_file']
    ordering = ['-datetime']
    actions = [unpack_zip_with_index]


class TaskAdmin(ModelAdmin):
    list_display = ['title', 'short_name', 'course', 'created_at', 'active']
    ordering = ['-created_at']


class LabTaskAdmin(ModelAdmin):
    list_display = ['title', 'short_name', 'course', 'created_at', 'active', 'deadline']
    ordering = ['-created_at']


class MessageAdmin(ModelAdmin):
    list_display = ['datetime', 'user', 'body', 'course']
    ordering = ['-datetime']


class HomeWorkSolutionAdmin(ModelAdmin):
    list_display = ['student', 'task', 'comment']
    ordering = ['-datetime']


class FeedbackAdmin(ModelAdmin):
    list_display = ['datetime', 'text', 'mobile', 'data']
    ordering = ['-datetime']


class FileSizeConstraintAdmin(ModelAdmin):
    list_display = ['task', 'min_size', 'max_size']


class FileNameConstraintAdmin(ModelAdmin):
    list_display = ['task', 'extension', 'file_name']


class ZipFileConstraintAdmin(ModelAdmin):
    list_display = ['task']


class ZipContainsConstraintAdmin(ModelAdmin):
    list_display = ['task', 'file_names']


class QuizAdmin(ModelAdmin):
    list_display = ['name', 'subject']


class SubjectAdmin(ModelAdmin):
    list_display = ['name']


class QuizQuestionAdmin(ModelAdmin):
    list_display = ['quiz', 'text', 'type']


class QuizAnswerAdmin(ModelAdmin):
    list_display = ['question', 'text', 'type']


class QuizResultAdmin(ModelAdmin):
    list_display = ['student', 'result']


class PointAdmin(ModelAdmin):
    list_display = ['student', 'points', 'reason']


admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(StudentGroup)
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Lecture)
admin.site.register(Task, TaskAdmin)
admin.site.register(LabTask, LabTaskAdmin)
admin.site.register(Resolution)
admin.site.register(FileResolution, ResolutionAdmin)
admin.site.register(Medal)
admin.site.register(StudentMedal)
admin.site.register(ChatMessage, MessageAdmin)
admin.site.register(FileSizeConstraint, FileSizeConstraintAdmin)
admin.site.register(FileNameConstraint, FileNameConstraintAdmin)
admin.site.register(ZipFileConstraint, ZipFileConstraintAdmin)
admin.site.register(ZipContainsFileConstraint, ZipContainsConstraintAdmin)
admin.site.register(UserActivity)
admin.site.register(Article)
admin.site.register(ExtraStudent)
admin.site.register(Todo)
admin.site.register(MustKnowGroup)
admin.site.register(MustKnow)
admin.site.register(AlreadyKnow)
admin.site.register(Point, PointAdmin)
admin.site.register(HomeWorkSolution, HomeWorkSolutionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizAnswer, QuizAnswerAdmin)
admin.site.register(QuizResult, QuizResultAdmin)


class MailAdmin(ModelAdmin):
    list_display = ['subject', 'recipients']


admin.site.register(Mail, MailAdmin)

