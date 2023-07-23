from module.network import app
from module.Task import Taskhelper
import module.OShelper
import webview

init_func = []
expose_func = []
close_func = []

def getfunc_from_module(module:module):
    """将函数分类"""
    for method in dir(module):
        if callable(getattr(module,method)):
            if method == 'init':
                init_func.append(getattr(module,method))
            elif method == 'close':
                close_func.append(getattr(module,method))
            elif method[0] == '_' and method[1] != '_':
                expose_func.append(getattr(module,method))

def init():
    for init in init_func:
        init()

    
def start(env = False):
    if env:
        window = webview.create_window('Universal Translator',url='http://localhost:5173/',width=2160,height=1200)
    else:
        window = webview.create_window('Universal Translator',url=app,width=2160,height=1200)
        
    def _open_folder():
        """文件夹选择"""
        result = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
        if result is not None:
            return result[0]
        else:
            return None
    
    def on_closed():
        for close in close_func:
            close()
    
    expose_func.append(_open_folder)
    window.events.closed += on_closed

    for func in expose_func:
        window.expose(func)
        print('Expose api '+ func.__name__)
    
    # MainThread blocked
    webview.start(debug = True)

task_helper = Taskhelper()
getfunc_from_module(module.OShelper)
getfunc_from_module(task_helper)

init()
start(env = True)