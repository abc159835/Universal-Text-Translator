import sys
sys.path.append(R'C:\Users\abc15\Desktop\Universal Translator')


from module.env import PATH
from module.TextParse import TextParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileModifiedEvent
import yaml
import chardet
import os

class FileHandler (FileSystemEventHandler):
    def on_modified (self, event:FileModifiedEvent):
        if event.is_directory == False:
            if event.src_path.endswith('plugins\TextParse\{}'.format(_global_config('rule'))):
                Parser_init()
                print('Detect change Reload '+ _global_config('rule'))
            elif event.src_path.endswith(_global_config('translator')):
                pass
        else:
            if event.src_path.endswith('plugins\TextParse'):
                rule_list_init()
            elif event.src_path.endswith('plugins\Translator'):
                translator_list_init()


def init():
    global global_configs
    global config_observer

    global_configs = read_config(None,PATH.joinpath('global_config.yaml'))
    translator_list_init()
    rule_list_init()

    config_observer = Observer()
    config_observer.schedule(FileHandler(),PATH.joinpath('plugins'),recursive=True)
    config_observer.start()

    Parser_init()

def translator_list_init():
    global translator_list
    translator_list = get_all_folder(PATH.joinpath('plugins\Translator'))

def rule_list_init():
    global rule_list
    rule_list = get_all_file(PATH.joinpath('plugins\TextParse'))

def Parser_init():
    # 初始化提取器
    global textParser
    textParser = TextParser(read_config(None,PATH.joinpath('plugins\TextParse\{}'.format(_global_config('rule')))))


def _get_translator_config(translator_name):
    return read_config(None, PATH.joinpath(f'plugins\Translator\{translator_name}\config.yaml'))


def _set_translator_config(translator_name, config):
    dump_config(config,PATH.joinpath(f'plugins\Translator\{translator_name}\config.yaml'))


def get_all_folder(path) -> list:
    folder_data = []
    for item in os.listdir(path):
        if os.path.isdir(path.joinpath(item)):
            folder_data.append(item)
    return folder_data


def get_all_file(path) -> list:
    file_data = []
    for item in os.listdir(path):
        if os.path.isfile(path.joinpath(item)):
            file_data.append(item)
    return file_data


def _recursive_read_folder(folder_path):
    """获取文件夹下的所有文件 输出树状格式"""
    folder_data = []
    file_data = []

    # 权限判断
    try:
        items: list = os.listdir(folder_path)
    except PermissionError:
        return {'Error': 'PermissionError'}

    # 对文件夹和文件进行排序
    items.sort()

    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            res = _recursive_read_folder(item_path)
            if res != []:
                folder_data.append(
                    {'label': item, 'path': item_path, 'children': res})
        else:
            file_data.append({'label': item, 'path': item_path})

    return folder_data + file_data


def _get_file_content(path):
    global textParser
    data = {'content': '', 'info': {'Encoding': 'UTF-8'}}
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
    data['selection'] = textParser.parser(data['content'].split('\n'))
    return data


def _global_config(name):
    global global_configs
    if name == None:
        return global_configs
    return global_configs[name]


def _get_variable(name):
    return eval(name)


def _set_global_config(key, value):
    global global_configs
    global_configs[key] = value
    dump_config(global_configs,PATH.joinpath('global_config.yaml'))
    if key == 'rule':
        Parser_init()


def dump_config(config,path):
    yaml.dump(config, open(path,'w', encoding='utf-8'), allow_unicode=True)


def read_config(name, path):
    try:
        config = yaml.load(open(path, 'r', encoding='utf-8'),Loader=yaml.FullLoader)
        if name == None:
            return config
        res = config[name]
        if type(res) == list:
            return res[0]
        else:
            return res
    except:
        return None


def close():
    print('Byee!')

