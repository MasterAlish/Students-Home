# coding=utf-8
from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group as UserGroup

from students.model.base import Teacher, Student, Course, Group as StudentGroup, Lecture, LabWork, Solution, ChatMessage

from students.models import MyUser, UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'fullname', 'phone', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'phone', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
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
    ordering = ('email',)
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


class SolutionAdmin(ModelAdmin):
    list_display = ['datetime', 'student', 'labwork', 'mark']
    ordering = ['-datetime']


class MessageAdmin(ModelAdmin):
    list_display = ['datetime', 'user', 'body', 'course']
    ordering = ['-datetime']

admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(StudentGroup)
admin.site.register(Lecture)
admin.site.register(LabWork)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(ChatMessage, MessageAdmin)

