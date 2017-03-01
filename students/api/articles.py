import json

from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, resolve
from django.views import View
from students.model.blog import Article


class JsonView(View):
    def json_response(self, data):
        return HttpResponse(content=json.dumps(data), content_type="application/json")

    def json_error(self, message="Unknown error", code=1):
        data = {
            'result': 'error',
            'message': message,
            'code': code
        }
        return HttpResponse(content=json.dumps(data), content_type="application/json")

    def json_success(self, data):
        data = {
            'result': 'success',
            'data': data
        }
        return HttpResponse(content=json.dumps(data), content_type="application/json")


class GetArticlesApi(JsonView):
    def dispatch(self, request, *args, **kwargs):
        count = request.GET.get("count", 10)
        last_item_id = request.GET.get("last_item_id", None)
        first_item_id = request.GET.get("first_item_id", None)

        qs = Article.objects.filter(published=True).order_by("-datetime")
        if last_item_id:
            qs = qs.filter(pk__gt=last_item_id)
        if first_item_id:
            qs = qs.filter(pk__lt=first_item_id)
        qs = qs[:count]

        articles = []
        for article in qs.all():
            data = {'id': article.id,
                    'title': article.title,
                    'datetime': article.datetime.strftime("%d.%m.%Y %H:%M"),
                    'viewed': article.viewed,
                    'course': None,
                    'preview': article.preview,
                    'body': render_to_string("api/article.html", {'article': article}, request=request),
                    'author': article.author.get_full_name(),
                    'url': "http://" + request.META["HTTP_HOST"] + reverse("article", kwargs={'id': article.id})}
            if article.course:
                data['course'] = {'id': article.course.id, 'name': article.course.name}

            articles.append(data)
        return self.json_response({'articles': articles})


class GetArticleApi(JsonView):
    def dispatch(self, request, *args, **kwargs):
        url = request.POST.get("url", None)
        if url is None:
            return self.json_error("Article not found", 404)
        article_id = self.get_article_id_by_url(request, url)
        if Article.objects.filter(pk=article_id).count() > 0:
            article = Article.objects.get(pk=article_id)

            course_data = {
                'id': article.id,
                'title': article.title,
                'datetime': article.datetime.strftime("%d.%m.%Y %H:%M"),
                'viewed': article.viewed,
                'course': None,
                'preview': article.preview,
                'body': render_to_string("api/article.html", {'article': article}, request=request),
                'author': article.author.get_full_name(),
                'url': "http://" + request.META["HTTP_HOST"] + reverse("article", kwargs={'id': article.id})}
            if article.course:
                course_data['course'] = {'id': article.course.id, 'name': article.course.name}

            return self.json_success({'article': course_data})
        return self.json_error("Article not found", 404)

    def get_article_id_by_url(self, request, url):
        host = request.META['HTTP_HOST']
        url = url[len("http://" + host):]
        article_id = resolve(url).kwargs['id']
        return article_id


class ReadArticleApi(JsonView):
    def dispatch(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(pk=request.GET.get("id", 10))
            article.viewed_mobile += 1
            article.save()
        except:
            pass
        return self.json_response({'result': 'success'})
