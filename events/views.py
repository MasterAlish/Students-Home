import json

from django.http.response import HttpResponse
from django.views import View

from events.models import Event
from students.mail import StudentsMail


class RegisterEventView(View):
    def dispatch(self, request, *args, **kwargs):
        domain = request.POST.get("domain", None)
        name = request.POST.get("event", None)
        details = request.POST.get("details", None)
        StudentsMail().inform_about_new_event(request, name)
        if name:
            Event(name=name, domain=domain, details=details).save()
            return HttpResponse(content=json.dumps({'success': True}), content_type="application/json")
        return HttpResponse(content=json.dumps({'success': False, 'error': 'error'}), content_type="application/json")