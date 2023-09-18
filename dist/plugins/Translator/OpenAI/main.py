from pathlib import Path
from module.OShelper import read_config
import openai
import time
import json

def init():
    global model, temperature, prompt, top_p

    config_path = Path(__file__).parent.joinpath('config.yaml')

    # openai.api_base = ' https://openkey.cloud/v1'
    openai.api_key = read_config('API-KEY',config_path)

    model = read_config('model',config_path,onlyfirst=True)
    temperature = read_config('temperature',config_path,onlyfirst=True)
    top_p = read_config('top_p',config_path,onlyfirst=True)
    prompt = read_config('prompt',config_path)
    

def generate_answer(messages):
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = temperature,
        top_p = top_p
    )
    content = response['choices'][0]['message']['content']
    return content

def retry(mes):
    from module.pywebview import Error
    try:
        _line = generate_answer(mes)
    except:
        Error()
        time.sleep(1)
        _line = retry(mes)
    return _line

def split_list(lst, n):
    return (lst[i:i+n] for i in range(0,len(lst),n))

# """
# 多行文本翻译尝试
# """
# def translate(lines: list[str]):
#     for _lines in split_list(lines,12):
#         count = len(_lines)

#         messages = [
#             {'role':'system','content':prompt},
#             {'role':'user','content':json.dumps(_lines,ensure_ascii=False)}
#         ]
        
#         _lines = []
#         while len(_lines) != count:
#             res = retry(messages)
#             print(res)
#             try:
#                 _lines = json.loads(res)
#             except:
#                 pass

#         for _line in _lines:
#             yield _line

"""
逐行文本翻译
"""
def translate(lines: list[str]):
    for _line in lines:
        messages = [
            {'role':'system','content':prompt},
            {'role':'user','content':_line}
        ]
        res = retry(messages)
        yield res