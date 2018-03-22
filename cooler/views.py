from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from cooler.exercises.checker import JavaExerciseChecker
from cooler.forms import SubmitExerciseForm
from cooler.models import CoolSnippet, Puzzle, Exercise, ExerciseSubmit


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


class ExercisesView(TemplateView):
    template_name = "cooler/exercises.html"

    def get_context_data(self, **kwargs):
        return {
            'exercises': Exercise.objects.all(),
            'solved': self.get_solved_exercises()
        }

    def get_solved_exercises(self):
        exercises = ExerciseSubmit.objects.filter(user=self.request.user, accepted=True).values_list("exercise")
        return [x[0] for x in exercises]


class ExerciseSubmissionsView(TemplateView):
    template_name = "cooler/exercise_submissions.html"

    def get_context_data(self, **kwargs):
        return {
            'submissions': ExerciseSubmit.objects.all()
        }


class ExerciseView(TemplateView):
    template_name = "cooler/exercise.html"

    def dispatch(self, request, *args, **kwargs):
        exercise = Exercise.objects.get(pk=kwargs['id'])
        form = SubmitExerciseForm()
        context = {
            'exercise': exercise
        }
        if request.method == 'POST':
            form = SubmitExerciseForm(request.POST)
            if form.is_valid():
                exercise.submitted += 1
                code = form.cleaned_data['code']
                submission = ExerciseSubmit(exercise=exercise, code=code, user=request.user)
                checker = JavaExerciseChecker(code)
                try:
                    message, code = checker.check(self.get_test_cases(exercise))
                except UnicodeEncodeError:
                    message = u'Unicode Error!!!'
                    code = 1
                checker.clear_all()
                submission.message = message
                if code == 0:
                    exercise.accepted += 1
                    submission.accepted = True
                else:
                    submission.accepted = False
                submission.save()
                exercise.save()
                return redirect(reverse("exercise_submissions"))

        context['form'] = form
        return render(request, self.template_name, context)

    def get_test_cases(self, exercise):
        test_cases = []
        for test_case in exercise.test_cases.all():
            test_cases.append(
                [test_case.input, test_case.output]
            )
        return test_cases

