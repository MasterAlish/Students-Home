from django.core.management import BaseCommand

from students.mail import StudentsMail


class Command(BaseCommand):
    def handle(self, *args, **options):
        StudentsMail().send_saved_mails(self.stdout)