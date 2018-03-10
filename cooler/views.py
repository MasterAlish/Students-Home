from django.shortcuts import render
from django.views.generic import TemplateView

from cooler.models import CoolSnippet, Puzzle


class CoolerView(TemplateView):
    template_name = "cooler/cooler.html"


class SoldierAndTankView(TemplateView):
    template_name = "cooler/soldier.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            code = request.POST.get("code", "")
            context['code'] = code
            if code:
                task = u"Soldier and Tank"
                if CoolSnippet.objects.filter(user=request.user, task=task).count() > 0:
                    CoolSnippet.objects.filter(user=request.user, task=task).update(code=code)
                else:
                    CoolSnippet.objects.create(user=request.user, code=code, task=task)
        return render(request, self.template_name, context)


class PuzzlesView(TemplateView):
    template_name = "cooler/puzzles.html"

    def get_context_data(self, **kwargs):
        return {
            'puzzles': Puzzle.objects.all()
        }


class PuzzleView(TemplateView):
    template_name = "cooler/puzzle.html"

    def dispatch(self, request, *args, **kwargs):
        puzzle = Puzzle.objects.get(slug=kwargs['slug'])
        if request.user != puzzle.added:
            puzzle.viewed += 1
            puzzle.save()
        return render(request, self.template_name, {'puzzle': puzzle})
