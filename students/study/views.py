# coding=utf-8
import random

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from students.model.base import Quiz, QuizQuestion, QuizAnswer, QuizResult, Task, Resolution
from students.study.forms import QuizScoreForm
from students.view.common import StudentsAndTeachersView, user_authorized_to_course, TeachersView


def get_random_questions(questions, count):
    result = []
    selected = set([])
    while len(selected) < count:
        i = random.randint(0, len(questions) - 1)
        if i not in selected:
            selected.add(i)
            result.append(questions[i])
    return result


class TestResultView(StudentsAndTeachersView):
    template_name = "test/test_result.html"

    def handle(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['task_id'])
        if user_authorized_to_course(request.user, task.course):
            context = {
                'task': task
            }
            if request.GET.get("id"):
                result = QuizResult.objects.get(pk=request.GET.get("id"))
                form = QuizScoreForm(request.POST or None, initial={'score': result.result})
                context['form'] = form
                if result.student == request.user or request.user.is_admin:
                    context['result'] = result

                if request.method == 'POST' and form.is_valid():
                    result.result = form.cleaned_data['score']
                    result.comment = form.cleaned_data['comment']
                    result.checked = True
                    result.save()
                    Resolution.objects.filter(student=result.student.student, task=task).delete()
                    Resolution(student=result.student.student, task=task, mark=result.result).save()

            elif request.user.is_admin:
                context['results'] = QuizResult.objects.filter(task=task)

            return render(request, self.template_name, context)
        return redirect("/")


class TestView(TemplateView):
    template_name = "test/test_form.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        task = Task.objects.get(pk=kwargs['task_id'])
        if QuizResult.objects.filter(task=task, student=request.user).exists():
            result = QuizResult.objects.get(task=task, student=request.user)
            return redirect(reverse("quiz_results", kwargs={'task_id': task.id})+"?id="+str(result.id))
        if request.method == 'POST':
            result = QuizResult(task=task, student=request.user)
            result.result, result.answer = self.count_result(request.POST, task)
            result.attempts += 1
            result.save()
            Resolution.objects.filter(student=result.student.student, task=task).delete()
            Resolution(student=result.student.student, task=task, mark=result.result).save()
            messages.success(request, u"Тест сдан успешно! Предварительная оценка: %s" % unicode(result.result))
            return redirect(reverse("quiz_results", kwargs={'task_id': task.id}) + "?id=" + str(result.id))
        else:
            questions = self.get_or_create_tests(task)
            context = {'questions': questions}

        return render(request, self.template_name, context)

    def get_or_create_tests(self, task):
        if "QUESTIONS%d" % task.id in self.request.session:
            question_ids = self.request.session["QUESTIONS%d" % task.id]
        else:
            questions = get_random_questions(
                reduce(lambda questions, quiz: questions + list(quiz.questions.all()), task.quiz.all(), []),
                task.quiz_count
            )
            question_ids = map(lambda q:q.id, questions)
            self.request.session["QUESTIONS%d" % task.id] = question_ids
        return QuizQuestion.objects.filter(pk__in=question_ids)

    def count_result(self, POST, task):
        score = 0
        html = u""
        counter = 1
        for key in POST.keys():
            if key.startswith("question"):
                quest_id = int(key[8:])
                question = QuizQuestion.objects.get(pk=quest_id)
                html += u"<b>%d. %s</b><br>" % (counter, question.text)
                counter += 1
                right = True
                if question.type == "multiple":
                    answers = map(lambda s: int(s), POST.getlist(key))
                    right = question.check_answer(answers)

                    for answer in question.answers.all():
                        html += u"<div class='answer'>"
                        html += u"[*] " if answer.id in answers else u"[ ] "
                        html += u"%s</div><br>" % unicode(answer.text).replace(u"<", u"&lt;").replace(u">", u"&gt;")
                elif question.type == "single":
                    answer_id = int(POST.get(key))
                    for answer in question.answers.all():
                        html += u"<div class='answer'>"
                        html += u"[*] " if answer.id == answer_id else u"[ ] "
                        html += u"%s</div><br>" % unicode(answer.text).replace(u"<", u"&lt;").replace(u">", u"&gt;")
                    right = question.check_answer([answer_id])
                else:
                    answer = POST.get(key)
                    html += u"<u>Ваш ответ:</u> <i class='answer'>%s</i>" % unicode(answer).replace(u"<", u"&lt;").replace(u">", u"&gt;")
                    right = question.check_text_answer(answer)
                html += u"<br><br>%s<br><br>" % (u"<span class='label label-success'>Правильно</span>" if right
                                             else u"<span class='label label-danger'>Неправильно</span>")

                if right:
                    score += task.max_score/float(task.quiz_count)
        return score, html


class DeleteTestResultView(TeachersView):
    def handle(self, request, *args, **kwargs):
        result = QuizResult.objects.get(pk=kwargs['id'])
        result.delete()
        return redirect(reverse("quiz_results", kwargs={'task_id': result.task_id}))


