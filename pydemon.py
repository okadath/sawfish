# # correrlo desde un pípenv 
# python pydemon.py asd.asd 

from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os ,sys
import subprocess
from termcolor import colored

a=0
def imprime_watch():
    print(colored("========= loading... ========","yellow"))
    print(colored("=============================","yellow"))
    print("\n")
    if 0==os.system('python '+sys.argv[1]):
        # print(a)
        # subprocess.run(['python',sys.argv[1]], check = True)
        print(colored("=============================","green"))
        print(colored("=======task executed=========","green"))
        print("\n\n")
    else:
        print(colored("=============================","red"))
        print(colored("=======task failed===========","red"))
        print("\n\n")

class Handler(FileSystemEventHandler):

    def on_modified(self, event):
        global a
        if a==0:
        # if event.src_path == "./"+sys.argv[1]: # in this example, we only care about this one file
            # print ("changed")
            imprime_watch()
            a=1                        

separador="="*(28+ len(sys.argv[1]))
print(colored(separador,"green"))
print(colored("====","green"),colored(" listening file ","yellow"),sys.argv[1],colored(" ====","green"))
imprime_watch()

observer = Observer()
observer.schedule(Handler(), "./"+sys.argv[1]) # watch the local directory
observer.start()

try:
    while True:
        sleep(0.5)

        a=0
except KeyboardInterrupt:
    observer.stop()

observer.join()
