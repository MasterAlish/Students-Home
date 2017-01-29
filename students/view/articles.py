from django.views.generic import TemplateView

from students.model.blog import Article


class ArticleView(TemplateView):
    template_name = "articles/article.html"
    article = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.article = Article.objects.get(pk=kwargs['id'])
            self.article.viewed += 1
            self.article.save()
            return super(ArticleView, self).dispatch(request, *args, **kwargs)
        except:
            self.article = None
            return

    def get_context_data(self, **kwargs):
        return {
            'article': self.article
        }