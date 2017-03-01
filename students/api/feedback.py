import json

from students.api.articles import JsonView
from students.model.extra import Feedback


class FeedbackApi(JsonView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and request.POST.get("text", None):
            text = request.POST.get("text", None)
            feedback = Feedback(text=text, mobile=True)
            data = {}
            if request.user.is_authenticated():
                data['user'] = unicode(request.user)
            feedback.data = json.dumps(data)
            feedback.save()
            return self.json_success({"message": "Feedback received"})
        return self.json_error("Feedback text not provided", 125)