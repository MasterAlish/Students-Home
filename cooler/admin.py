from django.contrib.admin import site
from django.contrib.admin.options import ModelAdmin

from cooler.models import CoolSnippet


class CoolSnippetAdmin(ModelAdmin):
    list_display = ['datetime', 'task', 'user', 'username', ]


site.register(CoolSnippet, CoolSnippetAdmin)