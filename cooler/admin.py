from django.contrib.admin import site
from django.contrib.admin.options import ModelAdmin

from cooler.models import CoolSnippet, Puzzle, ExerciseTestCase, ExerciseSubmit, Exercise


class CoolSnippetAdmin(ModelAdmin):
    list_display = ['datetime', 'task', 'user', 'username', ]


class PuzzleAdmin(ModelAdmin):
    list_display = ['title', 'datetime', 'added']


site.register(CoolSnippet, CoolSnippetAdmin)
site.register(Puzzle, PuzzleAdmin)
site.register(Exercise)
site.register(ExerciseTestCase)
site.register(ExerciseSubmit)
