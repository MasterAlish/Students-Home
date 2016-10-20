#coding: utf-8
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt

from students.view.chat import ChatView, NewMessagesView, PostMessageView
from students.view.courses import CourseView, LectureView, MyGroupView, GroupView, LabTaskView, \
    EmailToCourseStudentsView, MarksView, GiveMedalsView
from students.view.teachers import TeacherGroupsView, TeacherView, StudentView
from students.view.main import HomeView,on_error, on_not_found, auth_logout, \
    auth_profile, auth_register, password_change, user_change, reset_password

handler500 = 'students.view.main.on_error'
handler404 = 'students.view.main.on_not_found'

urlpatterns = [
    url(r'^accounts/login/$', login, name="login"),
    url(r'^accounts/logout/$', auth_logout, name="logout"),
    url(r'^accounts/profile/$', login_required(auth_profile), name="profile"),
    url(r'^accounts/register/$', auth_register, name="register"),
    url(r'^accounts/password/reset/$', reset_password, name="reset_password"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/password/change/$', login_required(password_change), name="change_password"),
    url(r'^accounts/profile/edit/$', login_required(user_change), name="change_user_data"),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^my/group/$', login_required(MyGroupView.as_view()), name='my_group'),
    url(r'^course/(?P<id>\d+)/$', login_required(CourseView.as_view()), name='course'),
    url(r'^lecture/(?P<id>\d+)/$', login_required(LectureView.as_view()), name='lecture'),
    url(r'^labtask/(?P<id>\d+)/$', login_required(LabTaskView.as_view()), name='labtask'),
    url(r'^course/(?P<id>\d+)/email_students/$', login_required(EmailToCourseStudentsView.as_view()), name='email-course'),
    url(r'^course/(?P<id>\d+)/give_medals/$', login_required(GiveMedalsView.as_view()), name='give-medals'),
    url(r'^course/(?P<id>\d+)/chat/$', login_required(csrf_exempt(ChatView.as_view())), name='chat'),
    url(r'^course/(?P<id>\d+)/marks/$', login_required(MarksView.as_view()), name='marks'),

    url(r'^chat/new-messages/$', login_required(NewMessagesView.as_view())),
    url(r'^chat/post/$', login_required(csrf_exempt(PostMessageView.as_view()))),

    url(r'^teacher/groups/$', login_required(TeacherGroupsView.as_view()), name='teacher_groups'),

    url(r'^teacher/(?P<id>\d+)/$', login_required(TeacherView.as_view()), name='teacher'),
    url(r'^student/(?P<id>\d+)/$', login_required(StudentView.as_view()), name='student'),
    url(r'^groups/(?P<id>\d+)$', login_required(GroupView.as_view()), name='group'),

    url(r'^error/$', on_error, name='error500'),
    url(r'^not-found/$', on_not_found, name='error404'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/',  include(admin.site.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

