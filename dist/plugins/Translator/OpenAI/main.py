from pathlib import Path
from module.OShelper import read_config
from module.Task import Task
import openai
import time

def init():
    global model, temperature, prompt

    config_path = Path(__file__).parent.joinpath('config.yaml')

    openai.api_base = ' https://openkey.cloud/v1'
    openai.api_key = read_config('API-KEY',config_path)

    model = read_config('model',config_path,onlyfirst=True)
    temperature = read_config('temperature',config_path,onlyfirst=True)
    prompt = read_config('prompt',config_path)
    

def generate_answer(messages):
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = temperature
    )
    content = response['choices'][0]['message']['content']
    return content

class Translator(Task):
    def main(self, lines: list[str]):
        # 设置任务终点
        self.end_progress = len(lines)

        res = {}
        for c in range(len(lines)):
            # 检查任务是否被用户取消，销毁线程
            if self.cancel:
                return
            
            line = lines[c]

            # 传递当前翻译目标信息
            self.info = line

            # messages = [
            #     {'role':'system','content':prompt},
            #     {'role':'user','content':line}
            # ]
            # lines[c] = generate_answer(messages)

            # 模拟翻译请求API
            time.sleep(0.1)

            res[line] = line

            # 前进度加 1
            self.progress += 1

        return res
