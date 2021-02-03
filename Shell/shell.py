import os
import sys

class ConsoleReader:
    def __init__(self):
        pass

    def get_next_line(self):
        return input(">>> ")

class FileReader:
    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        self.file_lines = [x.strip() for x in content]

    def get_next_line(self):
        line = self.file_lines.pop(0)
        if not line.startswith('#'):
            print('line', line)
            return line

        return ''


class Runner:
    def __init__(self):
        self.child_process_id = 0

    def exec(self, args):
        self.exec_async(args)
        os.waitpid(self.child_process_id, 0)

    def exec_async(self, args):
        self.child_process_id = os.fork()
        if self.child_process_id == 0:
            try:
                os.execv('/usr/bin/' + args[0], args)
            except:
                print('That is not a valid command')
                os._exit(0)

class Shell:
    def __init__(self, reader):
        self.is_running = False
        self.args = []
        self.reader = reader
        self.runner = Runner()

    def run(self):
        self.is_running = True
        while self.is_running:
            self.on_running()

    def exit(self):
        self.is_running = False

    def on_running(self):
        try:
            self.args = self.reader.get_next_line().split(" ")
        except IndexError:
            self.exit()
            return

        if self.input_is_empty():
            return

        if self.input_is_exit():
            self.exit();
            return

        if self.input_ends_with('$'):
            self.args = self.args[:1]
            self.runner.exec_async(self.args)
            return

        self.runner.exec(self.args)


    def input_is_empty(self):
        return len(self.args) == 0 or len(self.args) == 1 and self.args[0] == ''

    def input_is_exit(self):
        return len(self.args) == 1 and self.args[0] == 'exit'

    def input_ends_with(self, word):
        return len(self.args) > 0 and self.args[-1] == word

def get_reader():
    if len(sys.argv) == 1:
        return ConsoleReader()

    if len(sys.argv) == 2:
        return FileReader(sys.argv[1])

    raise ValueError

def main():
    print("Hello world")
    try:
        reader = get_reader()
        shell = Shell(reader)
        shell.run()
    except ValueError:
        print("Invalid arguments")


main()
