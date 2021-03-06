import sys 
import trace 
import threading 
import time 

class Thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        print("killed")
        self.killed = True

def threaded(fn):
    #Custom threading annotation 
    def wrapper(*args, **kwargs):
        thread = Thread_with_trace(
            target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def kill_thread(thread):
    #Kills the thread and returns None type
    if thread and thread.is_alive():
        thread.kill()
        thread.join() 
    return None

def clean_thread(thread):
    #Returns none if the thread is not alive
    if thread and not thread.is_alive():
        return None
    else:
        return t

@threaded
def timeout_thread(timeout, thread):
    #Sleeps for timeout parameter seconds and kills thread
    time.sleep(timeout)
    return kill_thread(thread)