from django.contrib.auth import authenticate, login, SESSION_KEY

from students.api.articles import JsonView
from hashlib import md5

from students.view.common import is_student, is_teacher


class AuthView(JsonView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.handle(request, *args, **kwargs)
        else:
            return self.json_error("User is not authenticated", 101)

    def handle(self, request, *args, **kwargs):
        return self.json_response({'result': "nothing"})


class LoginApi(JsonView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return self.json_response({
                    'result': "success",
                    'user': {
                        'id': user.id,
                        'name': user.get_full_name(),
                        'email': email,
                        'avatar': self.get_avatar(user)
                    }
                })
            else:
                return self.json_error("Email or password is incorrect", 102)
        else:
            return self.json_error("only POST is allowed", 99)

    def get_avatar(self, user):
        if is_student(user) and user.student.avatar.name:
            return "http://"+self.request.META['HTTP_HOST']+user.student.avatar.url
        if is_teacher(user) and user.teacher.avatar.name:
            return "http://"+self.request.META['HTTP_HOST']+user.teacher.avatar.url
        return "https://www.gravatar.com/avatar/%s?d=monsterid&s=256" % md5(user.email).hexdigest()