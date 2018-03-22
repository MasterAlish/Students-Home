import subprocess
import threading

import os


class JavaRunner:
    process = None
    error = None

    def __init__(self, dir, classname, test, input, expected_output):
        self.dir = dir
        self.classname = classname
        self.test = test
        self.input = input
        self.expected_output = expected_output

    def target(self):
        self.process = subprocess.Popen(
            ['java', '-Djava.security.manager', '-Djava.secutiry.policy=ss.policy', self.classname],
            cwd=self.dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = self.process.communicate(input=self.input)
        if err:
            if 'java.security.AccessControlException:' in err:
                self.error = "Security Error!!! Test: %d" % self.test
            else:
                self.error = "Runtime Error!!! Test: %d" % self.test
            return
        if out.strip() != self.expected_output.strip():
            self.error = "Wrong Answer!!! Test: %d" % self.test

    def run(self, timeout=2):
        thread = threading.Thread(target=self.target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.error = 'Time Out Error!!! Test: %d' % self.test
            self.process.terminate()
            thread.join()
        return self.error


class Compiler:
    def __init__(self, javafile):
        self.javafile = javafile

    def run(self):
        compilation = subprocess.Popen(['javac', self.javafile], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        out, err = compilation.communicate()
        if out or err:
            return "Compile Error!!!"


class TestRunner:

    def __init__(self, dir, classname, test_cases):
        self.dir = dir
        self.classname = classname
        self.test_cases = test_cases

    def run(self):
        error = Compiler(os.path.join(self.dir, self.classname+".java")).run()
        test = 1
        if not error:
            test_cases = self.test_cases
            for test_input, expected_output in test_cases:
                runner = JavaRunner(self.dir, self.classname, test, test_input, expected_output)
                error = runner.run(1)
                if error:
                    print(error)
                    break
                test += 1

        if not error:
            return "Accepted!!!", 0
        return error, 1
