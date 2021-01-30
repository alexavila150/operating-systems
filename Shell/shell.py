import os
import sys

class ConsoleReader:
    def __init__(self):
        pass

    def get_next_line(self):
        return input()

class FileReader:
    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        self.file_lines = [x.strip() for x in content]

    def get_next_line(self):
        return self.file_lines.pop(0)

class Runner:
    def __init__(self):
        self.process_ids = []

    def exec(self, args):
        self.process_ids.append(os.fork())

        if self.process_ids[-1] == 0:
            os.execve('/usr/bin/' + args[0], args, os.environ)

    def wait_for_all_processes(self):
        for id in self.process_ids:
            os.waitpid(id, 0)

class Shell:
    def __init__(self):
        self.is_running = False
        self.args = []
        self.reader = ConsoleReader()
        self.runner = Runner()
        self.valid_commands = {'ls', 'cat', 'grep', 'cd', 'mkdir', 'touch',
         'rm', 'git'}

    def run(self):
        self.is_running = True
        while self.is_running:
            self.args = self.reader.get_next_line().split(" ")
            self.process_args()

    def exit(self):
        self.is_running = False

    def process_args(self):
        if self.input_is_exit():
            self.exit();
            return
        if self.args[0] in self.valid_commands:
            self.runner.exec(self.args)


    def input_is_exit(self):
        return self.args[0] == 'exit' and len(self.args) == 1



def main():
    print("Hello world")
    shell = Shell()
    shell.run()


main()
