#coding: utf-8
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt

from students.view.activity import ActivityView
from students.view.articles import ArticleView
from students.view.chat import ChatView, NewMessagesView, PostMessageView
from students.view.courses import CourseView, LectureView, MyGroupView, GroupView, LabTaskView, \
    EmailToCourseStudentsView, MarksView, GiveMedalsView, SetMarksView, ExtraGroupView, ActivateStudentView, \
    CreateGroupViewView, LiteratureView, EditLiteratureView, AddLiteratureView, DeleteLiteratureView
from students.view.homework import UploadHomeWorkView
from students.view.profile import TeacherGroupsView, TeacherView, StudentView, TeachersListView
from students.view.auth import HomeView, on_error, on_not_found, auth_logout, \
    auth_profile, register_student, password_change, user_change, reset_password, register_teacher, LoginAsView
from students.view.teaching import LectureFormView, LectureActionView, LabTaskFormView, LabTaskActionView, \
    TaskActionView, TaskFormView, CoursesListView, CourseFormView, CourseActionView, ArticleFormView, ResolutionsView, \
    CheckResolutionView, HomeworksView, HomeworkView
from students.view.todo import TodoActView

handler500 = 'students.view.main.on_error'
handler404 = 'students.view.main.on_not_found'

urlpatterns = [
    url(r'^accounts/login/$', login, name="login"),
    url(r'^accounts/logout/$', auth_logout, name="logout"),
    url(r'^accounts/profile/$', login_required(auth_profile), name="profile"),
    url(r'^accounts/register/student/$', register_student, name="register_student"),
    url(r'^accounts/register/teacher/$', register_teacher, name="register_teacher"),
    url(r'^accounts/password/reset/$', reset_password, name="reset_password"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^accounts/password/change/$', login_required(password_change), name="change_password"),
    url(r'^accounts/profile/edit/$', login_required(user_change), name="change_user_data"),
    url(r'^login-as/(?P<user_id>\d+)$', login_required(LoginAsView.as_view()), name='login_as'),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^my/group/$', login_required(MyGroupView.as_view()), name='my_group'),
    url(r'^course/(?P<id>\d+)/$', login_required(CourseView.as_view()), name='course'),
    url(r'^lecture/(?P<id>\d+)/$', login_required(LectureView.as_view()), name='lecture'),
    url(r'^labtask/(?P<id>\d+)/$', login_required(LabTaskView.as_view()), name='labtask'),
    url(r'^task/(?P<id>\d+)/set_marks/$', login_required(SetMarksView.as_view()), name='set-marks'),
    url(r'^course/(?P<id>\d+)/email_students/$', login_required(EmailToCourseStudentsView.as_view()), name='email-course'),
    url(r'^course/(?P<id>\d+)/give_medals/$', login_required(GiveMedalsView.as_view()), name='give-medals'),
    url(r'^course/(?P<id>\d+)/chat/$', login_required(csrf_exempt(ChatView.as_view())), name='chat'),
    url(r'^course/(?P<id>\d+)/marks/$', login_required(MarksView.as_view()), name='marks'),
    url(r'^course/(?P<id>\d+)/homework/$', login_required(UploadHomeWorkView.as_view()), name='homework'),
    url(r'^course/(?P<id>\d+)/add_group/$', login_required(CreateGroupViewView.as_view()), name='add_group'),

    url(r'^teachers/$', login_required(TeachersListView.as_view()), name='all_teachers'),

    url(r'^courses/$', login_required(CoursesListView.as_view()), name='all_courses'),
    url(r'^courses/new$', login_required(CourseFormView.as_view()), name='add_course'),
    url(r'^courses/(?P<course_id>\d+)/edit$', login_required(CourseFormView.as_view()), name='edit_course'),
    url(r'^courses/(?P<id>\d+)/action', login_required(CourseActionView.as_view()), name='course_action'),

    url(r'^course/(?P<id>\d+)/lectures/new$', login_required(LectureFormView.as_view()), name='add_lecture'),
    url(r'^lectures/(?P<lecture_id>\d+)/edit$', login_required(LectureFormView.as_view()), name='edit_lecture'),
    url(r'^lectures/(?P<id>\d+)/action', login_required(LectureActionView.as_view()), name='lecture_action'),

    url(r'^course/(?P<id>\d+)/articles/new$', login_required(ArticleFormView.as_view()), name='add_article'),
    url(r'^articles/(?P<article_id>\d+)/edit$', login_required(ArticleFormView.as_view()), name='edit_article'),

    url(r'^course/(?P<id>\d+)/literature/$', login_required(LiteratureView.as_view()), name='literature'),
    url(r'^literature/(?P<id>\d+)/add/$', login_required(AddLiteratureView.as_view()), name='add_literature'),
    url(r'^literature/(?P<id>\d+)/edit/$', login_required(EditLiteratureView.as_view()), name='edit_literature'),
    url(r'^literature/(?P<id>\d+)/delete/$', login_required(DeleteLiteratureView.as_view()), name='delete_literature'),

    url(r'^course/(?P<id>\d+)/labtasks/new/$', login_required(LabTaskFormView.as_view()), name='add_labtask'),
    url(r'^course/(?P<id>\d+)/resolutions/$', login_required(ResolutionsView.as_view()), name='resolutions'),
    url(r'^course/(?P<id>\d+)/homeworks/$', login_required(HomeworksView.as_view()), name='homeworks'),
    url(r'^homeworks/(?P<id>\d+)/$', login_required(HomeworkView.as_view()), name='homework'),
    url(r'^labtasks/(?P<labtask_id>\d+)/edit/$', login_required(LabTaskFormView.as_view()), name='edit_labtask'),
    url(r'^labtasks/(?P<id>\d+)/action/$', login_required(LabTaskActionView.as_view()), name='labtask_action'),
    url(r'^resolution/(?P<id>\d+)/check/$', login_required(CheckResolutionView.as_view()), name='check_resolution'),

    url(r'^course/(?P<id>\d+)/tasks/new$', login_required(TaskFormView.as_view()), name='add_task'),
    url(r'^tasks/(?P<task_id>\d+)/edit$', login_required(TaskFormView.as_view()), name='edit_task'),
    url(r'^tasks/(?P<id>\d+)/action', login_required(TaskActionView.as_view()), name='task_action'),

    url(r'^chat/new-messages/$', login_required(NewMessagesView.as_view())),
    url(r'^chat/post/$', login_required(csrf_exempt(PostMessageView.as_view()))),

    url(r'^teacher/groups/$', login_required(TeacherGroupsView.as_view()), name='teacher_groups'),

    url(r'^teacher/(?P<id>\d+)/$', login_required(TeacherView.as_view()), name='teacher'),
    url(r'^student/(?P<id>\d+)/$', login_required(StudentView.as_view()), name='student'),
    url(r'^groups/(?P<id>\d+)$', login_required(GroupView.as_view()), name='group'),
    url(r'^extra_group/(?P<course_id>\d+)$', login_required(ExtraGroupView.as_view()), name='extra_group'),
    url(r'^activity/$', login_required(ActivityView.as_view()), name='activity'),
    url(r'^student/(?P<id>\d+)/activate/$', login_required(ActivateStudentView.as_view()), name='activate_student'),

    url(r'^article/(?P<id>\d+)$', ArticleView.as_view(), name='article'),

    url(r'^todo/act/$', TodoActView.as_view(), name='todo_act'),

    url(r'^error/$', on_error, name='error500'),
    url(r'^not-found/$', on_not_found, name='error404'),
    url(r'^contest/', include('contest.urls')),
    url(r'^api/', include('students.api.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/',  include(admin.site.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

