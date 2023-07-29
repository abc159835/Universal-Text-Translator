from module.env import PATH
from module.Task import Task, Taskhelper
from pathlib import Path
import json
import copy
import importlib.util

_module = None
translator:Task = None
task_helper = Taskhelper()
translate_dict = {}
export_list = []

def json_init(rootpath, path, json_object):
    if rootpath and Path(rootpath).joinpath(path).exists():
        with open(Path(rootpath).joinpath(path),'r',encoding='utf-8') as f:
            json_object = json.load(f)
    return json_object

def json_save(rootpath, path, json_object):
    from module.OShelper import creata_file_path
    if rootpath and len(json_object) > 0:
        creata_file_path(Path(rootpath).joinpath(path))
        with open(Path(rootpath).joinpath(path),'w',encoding='utf-8') as f:
            json.dump(json_object, f, ensure_ascii = False,indent=4)


def translate_dict_init(path):
    global translate_dict
    global export_list
    translate_dict = json_init(path,'UTT/data.json',{})
    export_list = json_init(path,'UTT/export.json',[])


def translate_dict_save(path):
    global translate_dict
    global export_list
    json_save(path,'UTT/data.json',translate_dict)
    json_save(path,'UTT/export.json',export_list)

def close():
    from module.OShelper import _global_config
    translate_dict_save(_global_config('path'))


def import_module(module_path):
    if module_path.exists():
        spec = importlib.util.spec_from_file_location('module',module_path)
        _module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_module)
        return _module
    
def translator_init():
    if hasattr(_module,'init'):
        init = getattr(_module,'init')
        init()

def translator_close():
    if hasattr(_module,'close'):
        close = getattr(_module,'close')
        close()

def translator_change():
    global translator
    global _module

    from module.OShelper import _global_config
    translator_name = _global_config('translator')
    if translator_name != None:
        _module = import_module(PATH.joinpath(f'plugins\Translator\{translator_name}\main.py'))
        translator = getattr(_module,'Translator')
        translator_init()

def _updata_translation(origin, text):
    global translate_dict
    translate_dict[origin] = text

def _get_translation(origin):
    global translate_dict
    return translate_dict.get(origin)


def finish_callback(t: Task):
    if t.result:
        for key in t.result:
            translate_dict[key] = t.textparser.fix_after([t.result[key]])[0]


def _translate(line: str):
    from module.OShelper import textParser
    t = translator()
    line = textParser.fix_before([line])[0]
    t_line = t.main([line])[line]
    line = textParser.fix_after([t_line])[0]
    return line


def _create_translate_task(name, strs):
    from module.OShelper import textParser,put_message

    mytextParser = copy.deepcopy(textParser)
    strs = mytextParser.fix_before(strs)

    t: Task = translator(strs)
    t.name = name
    t.info = '等待中...'
    t.textparser = mytextParser
    t.callback = finish_callback

    if task_helper.create_task(task = t):
        put_message('success',f'翻译任务: {name} 创建成功！')
    else:
        put_message('error',f'翻译任务: {name} 已经存在！')