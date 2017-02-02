import json

from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from students.model.blog import Article


class JsonView(View):
    def json_response(self, data):
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


class ReadArticleApi(JsonView):
    def dispatch(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(pk=request.GET.get("id", 10))
            article.viewed_mobile += 1
            article.save()
        except:
            pass
        return self.json_response({'result': 'success'})
