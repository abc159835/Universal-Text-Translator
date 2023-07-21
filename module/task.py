import queue
from threading import Thread
import uuid

class Task:
    def __init__(self,end_progress = 0) -> None:
        self.progress = 0
        self.end_progress = end_progress
        self.info = ''
        self.cancel = False
        self.message_queue = queue.Queue()
        self.uuid = uuid.uuid1()

    def run(self,*args):
        work_thread = Thread(target=self.main,args=args)
        work_thread.daemon = True
        work_thread.start()

    def main(self,*args):
        pass

    def wait_to_get_result(self):
        res = self.message_queue.get()
        return res
        
    
    def set_result(self,res):
        self.message_queue.put(res)

    def close(self):
        self.cancel = True
        self.message_queue.put('Close:'+self.uuid)