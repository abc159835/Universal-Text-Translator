from threading import Thread
import uuid
import queue


class Task:
    def __init__(self,*args) -> None:
        self.progress = 0
        self.end_progress = 100
        self.info = ''
        self.name = ''
        self.uuid = str(uuid.uuid1())
        self.cancel = False
        self.message_queue = queue.Queue()
        self.result = None
        self.args = args
        self.callback = Task._call_back
        self.strat_callback = Task._call_back

    def _call_back(self):
        pass

    def run(self):
        work_thread = Thread(target=self._main,args=self.args)
        work_thread.daemon = True
        work_thread.start()

    def _main(self,*args):
        from module.pywebview import Error
        try:
            self.set_result(self.main(*args))
        except:
            Error()
            self.close()

    def main(self,*args):
        pass

    def wait_to_get_result(self):
        if self.result == None:
            self.result = self.message_queue.get()
        if self.result == self.uuid:
            return None
        else:
            return self.result        
    
    def set_result(self,res):
        self.message_queue.put(res)

    def close(self):
        self.cancel = True
        self.message_queue.put(self.uuid)


class Taskhelper:
    def __init__(self) -> None:
        # 用一个字典来存储所有的任务，键是 name，值是 Task 对象
        self.tasks = {}
        self.task_queue = queue.Queue()
        work_thread = Thread(target=self.main)
        work_thread.daemon = True
        work_thread.start()

    def main(self):
        # 按顺序执行 task
        while True:
            task_id = self.task_queue.get()
            task:Task = self.tasks.get(task_id)
            Taskhelper.run_task(task)

    def run_task(task: Task):
        if task.cancel == False:
            task.strat_callback(task)
            task.run()
            task.wait_to_get_result()
            task.callback(task)


    def create_task(self, task:Task, start_now = False):
        # 创建一个新的任务，并将其添加到字典中
        if self.tasks.get(task.name):
            return False
        else:
            self.tasks[task.name] = task
            if start_now:
                Taskhelper.run_task(task)
            else:
                self.task_queue.put(task.name)
            return True

    def _cancel_task(self, name):
        # 根据 name 取消任务，如果不存在则返回 False，否则返回 True
        task = self.tasks.get(name)
        if task:
            task.close()
            self.tasks.pop(name)
            return True
        else:
            return False

    def _get_task_result(self, name):
        # 根据 name 获取任务的结果，如果不存在则返回 None，否则返回结果或关闭消息
        task = self.tasks.get(name)
        if task:
            return task.wait_to_get_result()
        else:
            return None

    def _get_all_tasks_status(self):
        # 获取所有任务的状态，返回一个列表，每个元素是一个元组，包含 name，进度，信息
        active_list = []
        disactive_list = []
        for name, task in self.tasks.items():
            if task.progress > 0:
                active_list.append({
                    'name':name, 
                    'progress':task.progress,
                    'info':task.info,
                    'end_progress': task.end_progress
                })
            else:
                disactive_list.append({
                    'name':name, 
                    'progress':task.progress,
                    'info':task.info,
                    'end_progress': task.end_progress
                })
        active_list.extend(disactive_list)
        return active_list
    