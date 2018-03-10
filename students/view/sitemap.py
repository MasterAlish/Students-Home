from django.shortcuts import render
from django.views.generic import TemplateView

from cooler.models import Puzzle
from students.model.blog import Article


class SitemapView(TemplateView):
    template_name = "sitemap.xml"

    def dispatch(self, request, *args, **kwargs):
        context = {
            'host': '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host()),
            'articles': Article.objects.all(),
            'puzzles': Puzzle.objects.all(),
        }
        return render(request, self.template_name, context, content_type="text/xml")
