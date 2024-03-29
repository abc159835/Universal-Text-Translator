from module.network import app
from module.env import PATH
from module.debounce import debounce
import module.module
import module.TextParse
import module.OShelper
import module.pywebview
import module.Translate
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

    @debounce(0.2)
    def on_resized(width, height):
        if height >= 720 and width >= 1280: 
            module.OShelper._set_global_config('width',width)
            module.OShelper._set_global_config('height',height)

    height = module.OShelper._global_config('height')
    width = module.OShelper._global_config('width')
    if not(height and width):
        height = 1200
        width = 2160

    if env:
        window = webview.create_window('Universal Text Translator',url='http://localhost:5173/',width=width,height=height)
    else:
        window = webview.create_window('Universal Text Translator',url=app,width=width,height=height)

    window.events.closed += on_closed
    window.events.resized += on_resized

    expose_func.append(_open_folder)

    for func in expose_func:
        window.expose(func)
        print('Expose api '+ func.__name__)
    
    # MainThread blocked
    webview.start(debug = env)



# 0
getfunc_from_module(module.TextParse)

# 1
getfunc_from_module(module.OShelper)

# 2
getfunc_from_module(module.Translate.task_helper)

# 3
module_path = PATH.joinpath('plugins\TextParser\main.py')
_module = module.Translate.import_module(module_path)
getfunc_from_module(_module)

# 4
getfunc_from_module(module.Translate)

try:
    init()
except:
    module.pywebview.Error()

start(env = False)
