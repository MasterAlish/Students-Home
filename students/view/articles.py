# coding=utf-8
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic import TemplateView

from students.forms.teaching import ArticleForm
from students.mail import StudentsMail
from students.model.base import Subject, Course
from students.model.blog import Article
from students.model.extra import AppAd
from students.view.common import user_authorized_to_course, StudentsAndTeachersView, is_teacher


def user_can_edit_article(user, article):
    return article is None or article.author_id == user.id or user.is_admin


class ArticleRedirectView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(pk=kwargs['id'])
            if not article.private or user_authorized_to_course(request.user, article.course):
                return redirect(reverse("article", kwargs={'slug': article.slug}))
        except:
            pass
        raise Http404()


class ArticleView(TemplateView):
    template_name = "articles/article.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(slug=kwargs['slug'])
            if not article.private or user_authorized_to_course(request.user, article.course):
                if request.user != article.author:
                    article.viewed += 1
                    article.save()
                return render(request, self.template_name, {
                    'host': '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host()),
                    'article': article,
                    'app_ad': AppAd.random()
                })
        except:
            pass
        raise Http404()


class SubjectArticlesView(TemplateView):
    template_name = "articles/subject.html"

    def dispatch(self, request, *args, **kwargs):
        subject = Subject.objects.get(slug=kwargs['slug'])
        return render(request, self.template_name, {
            'articles': subject.public_articles(),
            'app_ad': AppAd.random(),
            'subject': subject
        })


class ArticleFormView(StudentsAndTeachersView):
    template_name = "forms/model_form.html"
    model = u"статью"

    def handle(self, request, *args, **kwargs):
        article = None
        course = None
        if 'article_id' in kwargs:
            article = Article.objects.get(pk=kwargs['article_id'])
            course = article.course
        if 'id' in kwargs:
            course = Course.objects.get(pk=kwargs['id'])
        if user_authorized_to_course(request.user, course) and user_can_edit_article(request.user, article):
            form = ArticleForm(instance=article)
            if request.method == 'POST':
                form = ArticleForm(request.POST, request.FILES, instance=article)
                if form.is_valid():
                    form.instance.course = course
                    if form.instance.author is None:
                        form.instance.author = request.user
                    form.instance.save()
                    if article:
                        messages.success(request, u"Статья изменена успешно!")
                    else:
                        messages.success(request, u"Статья добавлена успешно!")
                        if not request.user.is_admin:
                            StudentsMail().report_article_added(request, form.instance)
                    if request.POST.get("save_and_close", None):
                        return redirect(reverse("course", kwargs={'id': course.id}))
                    else:
                        return redirect(reverse("edit_article", kwargs={'article_id': form.instance.id}))
            return render(request, self.template_name,
                          {'course': course, 'form': form, 'instance': article, 'model': self.model})
        raise Exception(u"User is not authorized")