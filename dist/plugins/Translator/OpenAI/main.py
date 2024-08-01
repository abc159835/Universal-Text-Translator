from pathlib import Path
from module.OShelper import read_config
import openai
import time
import json

def init():
    global model, temperature, prompt, top_p

    config_path = Path(__file__).parent.joinpath('config.yaml')

    openai.api_base = 'http://127.0.0.1:6006/v1/'
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
        top_p = top_p,

    )
    content = response['choices'][0]['message']['content']
    return content

def retry(mes) -> str:
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


"""
多行文本翻译尝试
"""
def translate(lines: list[str]):
    for lineslice in split_list(lines, 10):
        line = '\n\n'.join(lineslice)

        messages = [
            {'role':'system','content':prompt},
            {'role':'user','content':line}
        ]
        
        _line = retry(messages)
        # _line = line
        if len(_line.split('\n\n')) != len(lineslice):
            for line in translateSigle(lineslice):
                yield line
        else:
            for l in _line.split('\n\n'):
                yield l
         

"""
逐行文本翻译
"""
def translateSigle(lines: list[str]):
    for _line in lines:
        messages = [
            {'role':'system','content':prompt},
            {'role':'user','content':_line}
        ]
        res = retry(messages)
        yield res