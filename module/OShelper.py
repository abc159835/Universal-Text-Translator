import os
import chardet

def recursive_read_folder(folder_path):
    folder_data = []
    
    # 权限判断
    try:
        items:list = os.listdir(folder_path)
    except PermissionError:
        return []
    
    # 对文件夹和文件进行排序
    items.sort()  

    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            d = recursive_read_folder(item_path)
            if d != []:
                folder_data.append({'label':item,'path':item_path,'children':d})
            
    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            folder_data.append({'label':item,'path':item_path})
    return folder_data


def get_folder_all_file(folder_path):
    folder_data = recursive_read_folder(folder_path)
    return folder_data


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