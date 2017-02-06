from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from students.model.base import Todo


class TodoActView(View):
    def dispatch(self, request, *args, **kwargs):
        action = request.POST.get("action")
        id = request.POST.get("id")
        text = request.POST.get("text")
        type = request.POST.get("type")
        if action == 'add' and text and type in ['achievement', 'todo']:
            todo = Todo(user=request.user, text=text, done=(type == 'achievement'))
            todo.save()
        elif action == 'delete' and id:
            Todo.objects.filter(pk=id).delete()
        elif action == 'toggle' and id:
            for todo in Todo.objects.filter(pk=id):
                todo.done = not todo.done
                todo.save()

        return redirect(reverse("profile"))

