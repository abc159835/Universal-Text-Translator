from module.pywebview import Error
from module.env import PATH
from module.Task import Task
from module.TextParse import TextParser
from module.Translate import translator_change, translator_close, translate_dict_init, translate_dict_save
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileModifiedEvent
from module.debounce import debounce
from pathlib import Path
import pyperclip
import queue
import win32api, win32con
import yaml
import chardet
import os

class FileHandler (FileSystemEventHandler):
    @debounce(0.2)
    def on_modified (self, event:FileModifiedEvent):
        try:
            if event.is_directory == False:
                if event.src_path.endswith('plugins\TextParser\{}'.format(_global_config('rule'))):
                    Parser_init()
                    put_message('success','Detect change Reload '+ _global_config('rule'))
                elif event.src_path.find('plugins\Translator\{}'.format(_global_config('translator'))) != -1:
                    translator_change()
                    put_message('success','Detect change Reload '+ _global_config('translator'))
            else:
                if event.src_path.endswith('plugins\TextParser'):
                    rule_list_init()
                elif event.src_path.endswith('plugins\Translator'):
                    translator_list_init()
        except:
            Error()


def init():
    global global_configs
    global config_observer
    global message_queue
    global save_lock

    global_configs = read_config(None,PATH.joinpath('global_config.yaml'))
    translator_list_init()
    rule_list_init()
    translate_dict_init(_global_config('path'))
    
    config_observer = Observer()
    config_observer.schedule(FileHandler(),PATH.joinpath('plugins'),recursive=True)
    config_observer.start()

    # auto_save_thread = Thread(target=auto_save)
    # auto_save_thread.daemon = True
    # auto_save_thread.start()

    message_queue = queue.Queue()

    Parser_init()
    translator_change()

def translator_list_init():
    global translator_list
    translator_list = get_all_folder(PATH.joinpath('plugins\Translator'))

def rule_list_init():
    global rule_list
    rule_list = get_all_file(PATH.joinpath('plugins\TextParser'),extension='.yaml')

def Parser_init():
    # 初始化提取器
    global textParser
    textParser = TextParser(read_config(None,PATH.joinpath('plugins\TextParser\{}'.format(_global_config('rule'))),error_return={}))
   

def _get_translator_config(translator_name):
    return read_config(None, PATH.joinpath(f'plugins\Translator\{translator_name}\config.yaml'))


def save():
    translate_dict_save(_global_config('path'))


# def auto_save():
#     while True:
#         save()
#         time.sleep(40)


def _get_message():
    level,mes,box = message_queue.get()
    return {"level":level,"message":mes,"box":box}


def _set_translator_config(translator_name, config):
    dump_config(config,PATH.joinpath(f'plugins\Translator\{translator_name}\config.yaml'))


def _copy(_str):
    pyperclip.copy(_str)


def get_all_folder(path) -> list:
    folder_data = []
    for item in os.listdir(path):
        if os.path.isdir(path.joinpath(item)):
            folder_data.append(item)
    return folder_data


def get_all_file(path,extension = None) -> list:
    file_data = []
    for item in os.listdir(path):
        if os.path.isfile(path.joinpath(item)):
            if extension == None or item.endswith(extension):   
                file_data.append(item)
    return file_data


def _recursive_read_folder(folder_path):
    """获取文件夹下的所有文件 输出树状格式"""
    folder_data = []
    file_data = []

    items: list = os.listdir(folder_path)
        
    # 对文件夹和文件进行排序
    items.sort()

    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            if not item_path.endswith('UTT'):
                res = _recursive_read_folder(item_path)
                if res != []:
                    folder_data.append(
                        {'label': item, 'path': item_path, 'children': res})
        else:
            file_data.append({'label': item, 'path': item_path})

    return folder_data + file_data


def creata_file_path(file_path):
    if type(file_path) == str:
        file_path = Path(file_path)
    if not file_path.parent.exists():
        os.makedirs(file_path.parent)
        win32api.SetFileAttributes(str(file_path.parent), win32con.FILE_ATTRIBUTE_HIDDEN)


def _get_file_content(path, useTrans = False, mytextParser = None):
    if mytextParser is None:
        global textParser
        mytextParser = textParser
    root_path = _global_config('path')
    relative_path = os.path.relpath(path,root_path)
    data = {'content': '', 'info': {'Encoding': 'UTF-8'}}
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data['content'] = f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'rb') as f:
                bytes = f.read()
            result = chardet.detect(bytes)
            encoding = result['encoding']

            data['content'] = bytes.decode(encoding)
            data['info']['Encoding'] = encoding
            
        except:
            return None

    data['selection'],data['content'],data['lines'] = mytextParser.parser(data['content'].split('\n'))

    if useTrans:
        data['selection'],data['content'],data['bools'] = TextParser.translate(data['selection'], data['content'])
    else:
        data['bools'] = [False] * len(data['selection'])

    find = len(data['selection'])

    data['info']['Path'] = relative_path
    data['info']['Find'] = find
    data['info']['Line'] = len(data['content'].split('\n'))

    from module.Translate import export_list
    if relative_path not in export_list and find > 0:
        export_list.append(relative_path)

    return data


def _global_config(name):
    global global_configs
    if name == None:
        return global_configs
    res = global_configs.get(name)
    if res == None:
        return None
    return res


def _get_variable(name):
    return eval(name)


def _set_global_config(key, value):
    global global_configs
    old_value = global_configs.get(key)
    global_configs[key] = value
    dump_config(global_configs,PATH.joinpath('global_config.yaml'))

    if key == 'rule':
        Parser_init()
    elif key == 'translator':
        translator_change()
    elif key == 'path':
        if old_value:
            translate_dict_save(old_value)
        translate_dict_init(value)
    
    
def put_message(level,message,box=False):
    global message_queue
    message_queue.put((level,message,box))


def dump_config(config,path):
    yaml.dump(config, open(path,'w', encoding='utf-8'), allow_unicode=True)


def _save_file(path,content,encoding):
    with open(path,'w',encoding=encoding) as f:
        f.write(content)


def read_config(name, path, error_return = {},onlyfirst = False):
    config = yaml.load(open(path, 'r', encoding='utf-8'),Loader=yaml.FullLoader)
    if name == None:
        return config
    res = config.get(name)
    if res == None:
        return error_return
    if onlyfirst and type(res) == list:
        return res[0]
    else:
        return res


def close():
    translator_close()


def _create_export_task(path):
    from module.Translate import task_helper
    ef = export_folder(path)
    ef.name = path
    if task_helper.create_task(task = ef, start_now = True):
        put_message('success',f'导出任务: {path} 创建成功！')
    else:
        put_message('error',f'导出任务: {path} 已经存在！')


class export_folder(Task):
    def main(self, path):
        from module.Translate import export_list
        self.end_progress = len(export_list)
        rootpath = _global_config('path')
        for file in export_list:
            if self.cancel:
                return
            self.info = file
            data = _get_file_content(Path(rootpath).joinpath(file), useTrans=True)
            if data['info']['Find'] > 0:
                with open(Path(path).joinpath(data['info']['Path']),mode='w',encoding=data['info']['Encoding']) as f:
                    f.write(data['content'])
            self.progress += 1