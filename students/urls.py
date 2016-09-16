#coding: utf-8
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login

from students.view.courses import CourseView, LectureView, MyGroupView
from views import HomeView,on_error, on_not_found, auth_logout, \
    auth_profile, auth_register

handler500 = 'students.views.on_error'
handler404 = 'students.views.on_not_found'

urlpatterns = [
    url(r'^accounts/login/$', login, name="login"),
    url(r'^accounts/logout/$', auth_logout, name="logout"),
    url(r'^accounts/profile/$', auth_profile, name="profile"),
    url(r'^accounts/register/$', auth_register, name="register"),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^my/group/$', MyGroupView.as_view(), name='my_group'),
    url(r'^course/(?P<id>\d+)$', CourseView.as_view(), name='course'),
    url(r'^lecture/(?P<id>\d+)$', LectureView.as_view(), name='lecture'),

    url(r'^error/$', on_error, name='error500'),
    url(r'^not-found/$', on_not_found, name='error404'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/',  include(admin.site.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

