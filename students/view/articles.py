from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views.generic import TemplateView

from students.model.base import Subject
from students.model.blog import Article
from students.view.common import user_authorized_to_course


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
                article.viewed += 1
                article.save()
                return render(request, self.template_name, {'article': article})
        except:
            pass
        raise Http404()


class SubjectArticlesView(TemplateView):
    template_name = "articles/subject.html"

    def dispatch(self, request, *args, **kwargs):
        subject = Subject.objects.get(slug=kwargs['slug'])
        return render(request, self.template_name, {
            'articles': subject.public_articles(),
            'subject': subject
        })
