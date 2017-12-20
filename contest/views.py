# coding=utf-8
from datetime import datetime

import requests
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from lxml import html

from contest.forms import AddProblemForm, SubmitProblemForm, JudgeIdForm, AddContestForm
from contest.models import Problem, ProblemSolution, Contestant, Contest
from contest.parse.problems import ProblemParser
from contest.parse.solutions import SolutionParser


class ContestHomeView(TemplateView):
    template_name = "contest/home.html"


class RanklistView(TemplateView):
    template_name = "contest/ranklist.html"

    def get_context_data(self, **kwargs):
        contest_id = self.request.GET.get("contest", None)
        solutions = ProblemSolution.objects.filter(contest_id=contest_id).order_by("contestant")
        results = []
        results_by_contestant = {}
        for solution in solutions:
            if solution.contestant_id not in results_by_contestant:
                results_by_contestant[solution.contestant_id] = {}
            results_by_problem = results_by_contestant[solution.contestant_id]
            if solution.problem_id not in results_by_problem:
                results_by_problem[solution.problem_id] = []
        return {}


class SubmitsView(TemplateView):
    template_name = "contest/submits.html"

    def dispatch(self, request, *args, **kwargs):
        not_finished_submits = ProblemSolution.objects.filter(checked=False).order_by("datetime")[:3]
        for submit in not_finished_submits:
            response = requests.get("http://acm.timus.ru/status.aspx?space=1&from=%d" % submit.acm_id)
            if response.status_code == 200:
                submit = SolutionParser(response.text).parse_and_fill(submit)
                submit.checked = submit.check_result not in ["Compiling", "Running"]
                submit.save()
        solutions = ProblemSolution.objects.all()
        if request.GET.get("contest", None):
            solutions = solutions.filter(contest=request.GET.get("contest", None))
        context = {
            'solutions': solutions.order_by("-datetime")
        }
        return render(request, self.template_name, context)


class RegisterAcmView(TemplateView):
    template_name = "contest/register_acm.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        contestant = None
        try:
            contestant = Contestant.objects.get(user=self.request.user)
            context['judge_id'] = contestant.judge_id
        except: pass
        if request.method == "POST":
            form = JudgeIdForm(request.POST)
            if form.is_valid():
                judge_id = form.cleaned_data['judge_id']
                if contestant is None:
                    contestant = Contestant(user=request.user, username=judge_id)
                contestant.judge_id = judge_id
                contestant.save()
                messages.success(request, u"Ваши данные успешно сохранены")
                return redirect(reverse("register_acm"))
            context['form'] = form
        return render(request, self.template_name, context)


class ContestsView(TemplateView):
    template_name = "contest/contests.html"

    def get_context_data(self, **kwargs):
        return {
            'contests': Contest.objects.all().order_by("-start"),
            'now': datetime.now()
        }


class AddContestView(TemplateView):
    template_name = "contest/add_contest.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        form = AddContestForm()
        if request.method == 'POST':
            form = AddContestForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, u"Соревнование добавлено успешно!")
                return redirect(reverse("contest", kwargs={'id': form.instance.id}))
        context['form'] = form
        return render(request, self.template_name, context)


class ContestView(TemplateView):
    template_name = "contest/contest.html"

    def get_context_data(self, **kwargs):
        return {
            'contest': Contest.objects.get(pk=kwargs['id']),
            'now': datetime.now()
        }


class DeleteContestView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        Contest.objects.get(pk=kwargs['id']).delete()
        return redirect(reverse("all_contests"))


class ProblemsView(TemplateView):
    template_name = "contest/problems.html"

    def get_context_data(self, **kwargs):
        return {
            'problems': Problem.objects.all().order_by("acm_id")
        }


class ProblemPage(TemplateView):
    template_name = "contest/problem.html"

    def get_context_data(self, **kwargs):
        return {
            'problem': Problem.objects.get(pk=kwargs['id'])
        }


def get_current_contest():
    now = datetime.now()
    try:
        return Contest.objects.filter(start__lt=now, end__gt=now, active=True)[0]
    except:
        return None


class SubmitPage(TemplateView):
    template_name = "contest/submit.html"

    def dispatch(self, request, *args, **kwargs):
        problem = Problem.objects.get(pk=kwargs['id'])
        form = SubmitProblemForm()
        if Contestant.objects.filter(user=request.user).count() == 0:
            messages.warning(request, u"У вас не указан JUDGE_ID сайта acm.timus.ru")
            return redirect(reverse("register_acm"))
        if request.method == "POST":
            form = SubmitProblemForm(request.POST)
            if form.is_valid():
                try:
                    solution = self.submit_solution(problem, form.cleaned_data['language'], form.cleaned_data['body'])
                    solution.contest = get_current_contest()
                    messages.success(self.request, u"Успешно отправлено %d" % solution.acm_id)
                    return redirect(reverse("submits"))
                except Exception as e:
                    messages.error(request, repr(e))
        context = {
            'form': form,
            'problem': problem,
        }
        return render(request, self.template_name, context)

    def submit_solution(self, problem, language, body):
        contestant = Contestant.objects.get(user=self.request.user)
        data = {
            'Action': 'submit',
            'SpaceID': '1',
            'JudgeID': contestant.judge_id,
            'Language': language,
            'ProblemNum': problem.acm_id,
            'Source': body,
        }
        response = requests.post("http://acm.timus.ru/submit.aspx", data)
        if response.status_code == 200:
            solution = ProblemSolution(problem=problem, contestant=contestant)
            solution = SolutionParser(response.text).parse_and_fill(solution)
            solution.save()
            return solution
        else:
            raise Exception(str(response.status_code))


class AddProblemView(TemplateView):
    template_name = "contest/add_problem.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            form = AddProblemForm(request.POST)
            if form.is_valid():
                problem_url = form.cleaned_data['problem_url']
                parser = ProblemParser(problem_url)
                try:
                    problem = parser.parse()
                    problem.contest_id = request.GET.get("contest", None)
                    problem.save()
                    messages.success(request, u"Задача добавлена успешно!")
                    return redirect(reverse("all_problems"))
                except Exception as e:
                    form.add_error("problem_url", e.message)
            context['form'] = form
        return render(request, self.template_name, context)

