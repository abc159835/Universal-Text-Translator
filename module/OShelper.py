from module.env import PATH
import os
import chardet
import yaml

def init():
    global global_configs
    global_configs = yaml.load(open(PATH.joinpath('global_config.yaml'),'r',encoding='utf-8'),Loader=yaml.FullLoader)

def recursive_read_folder(folder_path):
    """获取文件夹下的所有文件 输出树状格式"""
    folder_data = []
    file_data = []
    
    # 权限判断
    try:
        items:list = os.listdir(folder_path)
    except PermissionError:
        return {'Error':'PermissionError'}
    
    # 对文件夹和文件进行排序
    items.sort()  

    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            res = recursive_read_folder(item_path)
            if res != []:
                folder_data.append({'label':item,'path':item_path,'children':res})
        else:
            file_data.append({'label':item,'path':item_path})

    return folder_data + file_data


def get_file_content(path):
    data = {'content':[],'info':'UTF-8'}
    try:
        with open(path,'r',encoding='utf-8') as f:
            data['content'] = f.read()
    except UnicodeDecodeError:
        try:
            with open(path,'rb') as f:
                bytes = f.read()
            result = chardet.detect(bytes)
            encoding = result['encoding']
            data['content'] = bytes.decode(encoding)
            data['info'] = encoding
        except:
            data = None
    return data

def global_config(name):
    global global_configs
    return global_configs[name]

def set_global_config(key,value):
    global global_configs
    global_configs[key] = value
    yaml.dump(global_configs,open(PATH.joinpath('global_config.yaml'),'w',encoding='utf-8'))