import os

class Runner:
    def __init__(self):
        self.process_ids = []
        
    def exec(self, args):
        self.process_ids.append(os.fork())

        if self.process_ids[-1] == 0:
            os.execv('/usr/bin/' + args[0], args)
    
    def wait_for_all_processes(self):
        for id in self.process_ids:
            os.waitpid(id, 0)

def main():
    runner = Runner()
    runner.exec(['cat', '/proc/cpuinfo'])
    runner.exec(['echo', 'Hello World'])
    runner.exec(['python3', 'spinner.py', '1000000']) 
    runner.exec(['uname', '-a'])
    
    runner.wait_for_all_processes()
    runner.exec(['python3', 'spinner.py', '2000000'])

main()
