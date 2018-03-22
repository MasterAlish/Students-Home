from random import randint

import os

import shutil
from django.conf import settings

from cooler.exercises.javarunner import TestRunner


class JavaExerciseChecker:
    def __init__(self, code):
        self.code = code
        self.temp_number = randint(0, 999999)
        self.prepare_file()
        self.working_dir = None
        self.prepare_file()

    def prepare_file(self):
        self.working_dir = os.path.join(settings.MEDIA_ROOT, "tests", "java_%d" % self.temp_number)
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
        java_file = open(os.path.join(self.working_dir, "Solution.java"), mode="w")
        java_file.write(self.code.encode("utf8"))
        java_file.close()

    def check(self, test_cases):
        runner = TestRunner(self.working_dir, "Solution", test_cases)
        return runner.run()

    def clear_all(self):
        shutil.rmtree(self.working_dir)
