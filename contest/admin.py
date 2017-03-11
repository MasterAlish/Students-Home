from django.contrib import admin

from contest.models import Problem, Contestant, ProblemSolution

admin.site.register(Problem)
admin.site.register(Contestant)
admin.site.register(ProblemSolution)
