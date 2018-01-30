# coding=utf-8

from django.core.management import BaseCommand

from students.management.commands.tests import Type
from students.models import MyUser


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('email', type=str)
        parser.add_argument('pass', type=str)

    def handle(self, *args, **options):
        email = options['email']
        new_pass = options['pass']
        try:
            user = MyUser.objects.get(email=email)
            user.set_password(new_pass)
            user.save()
            print("Password changed successfully")
        except MyUser.DoesNotExist:
            print("User not found")
        except Exception as e:
            print(repr(e))
