from threading import Thread
import uuid
import queue


class Task:
    def __init__(self,*args) -> None:
        self.progress = 0
        self.end_progress = 100
        self.info = ''
        self.cancel = False
        self.message_queue = queue.Queue()
        self.uuid = uuid.uuid1()
        self.result = None
        self.args = args

    def run(self):
        work_thread = Thread(target=self.main,args=self.args)
        work_thread.daemon = True
        work_thread.start()

    def main(self,*args):
        pass

    def wait_to_get_result(self):
        if self.result == None:
            self.result = self.message_queue.get()
        return self.result
        
    
    def set_result(self,res):
        self.message_queue.put(res)

    def close(self):
        self.cancel = True
        self.message_queue.put('Close:'+self.uuid)


class Taskhelper:
    def __init__(self) -> None:
        # 用一个字典来存储所有的任务，键是 uuid，值是 Task 对象
        self.tasks = {}
        self.task_queue = queue.Queue()
        work_thread = Thread(target=self.main)
        work_thread.daemon = True
        work_thread.start()

    def main(self):
        # 按顺序执行 task
        while True:
            task_id = self.task_queue.get()
            task:Task = self.get_task(task_id)
            task.run()
            task.wait_to_get_result()


    def create_task(self, task:Task):
        # 创建一个新的任务，并将其添加到字典中
        self.tasks[task.uuid] = task
        self.task_queue.put(task.uuid)
        # 返回任务的 uuid
        return task.uuid

    def get_task(self, uuid):
        # 根据 uuid 获取任务，如果不存在则返回 None
        task = self.tasks.get(uuid)
        if task:
            return task
        else:
            return None

    def _cancel_task(self, uuid):
        # 根据 uuid 取消任务，如果不存在则返回 False，否则返回 True
        task = self.tasks.get(uuid)
        if task:
            task.close()
            return True
        else:
            return False

    def _get_task_result(self, uuid):
        # 根据 uuid 获取任务的结果，如果不存在则返回 None，否则返回结果或关闭消息
        task = self.tasks.get(uuid)
        if task:
            return task.wait_to_get_result()
        else:
            return None

    def _get_all_tasks_status(self):
        # 获取所有任务的状态，返回一个列表，每个元素是一个元组，包含 uuid，进度，信息
        status_list = []
        for uuid, task in self.tasks.items():
            if task.cancel == False:
                status_list.append((uuid, task.progress, task.info))
        return status_list