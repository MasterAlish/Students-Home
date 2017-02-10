import os

from django.conf import settings
from django.core.management import BaseCommand

from students.mail import StudentsMail
from students.model.base import FileResolution
from students.model.checks import ZipContainsFileConstraint


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_resolutions = FileResolution.objects.all()
        for file_resolution in file_resolutions:
            if self.has_html_index_file(file_resolution.task):
                labname = "lab%d" % file_resolution.task.number
                username = file_resolution.student.get_short_name()
                lab_url = os.path.join(settings.MEDIA_URL, "sites", labname, username, "index.html")
                file_resolution.index_file = lab_url
                file_resolution.save()

    def has_html_index_file(self, labtask):
        for constraint in labtask.constraints.instance_of(ZipContainsFileConstraint):
            if u'index.html' in constraint.file_names:
                return True
        return False