from module.env import PATH
from module.Task import Task, Taskhelper
from pathlib import Path
from threading import Thread, Lock
from module.debounce import debounce
import json
import os
import copy
import importlib.util

_module = None
translator:Task = None
task_helper = Taskhelper()
translate_dict = {}
export_list = []
save_lock = Lock()

def init():
    global debounce_save
    from module.OShelper import save
    debounce_save = debounce(2)(save)


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
            save_lock.acquire()
            json.dump(json_object, f, ensure_ascii = False,indent=4)
            save_lock.release()


def translate_dict_init(path):
    global translate_dict
    global export_list
    translate_dict = json_init(path,'UTT/data.json',{})
    export_list = json_init(path,'UTT/export.json',[])


def translate_dict_save(path: str):
    global translate_dict
    global export_list

    back_up = Path(path).joinpath('UTT/backup_data.json')
    data = Path(path).joinpath('UTT/data.json')
    if back_up.exists():
        os.remove(back_up)
    if data.exists():
        os.rename(data,back_up)
    
    json_save(path,'UTT/data.json',translate_dict)
    json_save(path,'UTT/export.json',export_list)


def close():
    from module.OShelper import save
    save()


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
        try:
            translator = getattr(_module,'Translator')
        except:
            translate_func = getattr(_module,'translate')
            translator = get_translator(translate_func)

        translator_init()

def _updata_translation(origin, text):
    global translate_dict
    global debounce_save
    translate_dict[origin] = text
    debounce_save()


def _get_translation(origin):
    global translate_dict
    return translate_dict.get(origin)


def finish_callback(t: Task):
    from module.pywebview import Error
    if t.result == t.uuid:
        return
    try:
        if t.result:
            values = list(t.result.values())
            values = t.textparser.fix_after(values)
            for c in range(len(values)):
                translate_dict[t.res_backup[c]] = values[c]
    except:
        Error()


def _translate(line: str):
    from module.OShelper import textParser
    t = translator()
    line = textParser.fix_before([line])[0]
    t_line = t.main([line])[line]
    line = textParser.fix_after([t_line])[0]
    return line.replace('\n','\t')


def _create_translate_all_task(file_data, useTrans = True):
    from module.OShelper import put_message
    name = '查找所有可预翻译文本'

    t: Task = TranslateALL(file_data, useTrans)
    t.name = name
    t.info = '等待中...'

    if task_helper.create_task(task = t, start_now=True):
        put_message('success',f'任务: {name} 创建成功！')
    else:
        put_message('error',f'任务: {name} 已经存在！')


def preTranslate(strs: list[str]):
    new_strs = []
    for _str in strs:
        if not translate_dict.get(_str):
            new_strs.append(_str)
    return new_strs


def start_callback(self: Task):
    from module.OShelper import textParser
    if self.args[1]:
        strs = preTranslate(self.args[0])
    else:
        strs = self.args[0]
    
    mytextParser = copy.deepcopy(textParser)
    strs = mytextParser.fix_before(strs)
    self.textparser = mytextParser
    # 元组中只包含一个元素时，需要在元素后面添加逗号
    self.args = (strs,)


def _create_translate_task(name, strs: list[str], useTrans = True):
    from module.OShelper import put_message

    # 使用dict.fromkeys()保持顺序地去重
    strs = list(dict.fromkeys(strs))
    
    if useTrans:
        strs = preTranslate(strs)

    if len(strs) == 0:
        put_message('warning',f'{name} 没有需要翻译的文本！')
        return

    t: Task = translator(strs, useTrans)
    t.name = name
    t.info = '等待中...'
    # 用于保存fix_before 之前的数据
    t.res_backup = copy.deepcopy(strs)
    t.callback = finish_callback
    t.strat_callback = start_callback

    if task_helper.create_task(task = t):
        put_message('success',f'翻译任务: {name} 创建成功！')
    else:
        put_message('error',f'翻译任务: {name} 已经存在！')


class TranslateALL(Task):
    def find_file(self,Trees):
        self.end_progress += len(Trees)
        for tree in Trees:
            if 'children' in tree:
                self.end_progress -= 1
                for file in self.find_file(tree['children']):
                    yield file
            else:
                yield tree['path']


    def main(self, file_data, useTrans = True):
        from module.OShelper import _get_file_content, textParser
        self.end_progress = 0
        mytextParser = copy.deepcopy(textParser)
        for file_path in self.find_file(file_data):
            datas = _get_file_content(file_path, False, mytextParser)
            if datas and datas['info']['Find'] > 0:
                if self.cancel:
                    return
                rel_path = datas['info']['Path']
                self.info = rel_path
                if useTrans:
                    datas['lines'] = preTranslate(datas['lines'])
                if len(datas['lines']) > 0:
                    _create_translate_task(rel_path, datas['lines'], False)
            self.progress += 1


def get_translator(translate_func):
    class Translator(Task):
        def main(self, lines: list[str]):
            # 设置任务终点
            self.end_progress = len(lines)

            res = {}
            Generator = translate_func(lines)
            for line in lines:
                # 检查任务是否被用户取消，销毁线程
                if self.cancel:
                    return

                # 传递当前翻译目标信息
                self.info = line

                _line = next(Generator)

                print(line + ' --> ' + _line)
                
                res[line] = _line

                # 前进度加 1
                self.progress += 1

            return res
        
    return Translator