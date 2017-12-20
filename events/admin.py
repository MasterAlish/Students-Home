from django.contrib.admin import site, ModelAdmin

from events.models import Event


class EventAdmin(ModelAdmin):
    list_display = ["datetime", "domain", "name", "details"]

site.register(Event, EventAdmin)