import sys
sys.path.append(R'C:\Users\abc15\Desktop\Universal Translator')

from pathlib import Path
from module.OShelper import read_config
import openai

config_path = Path(__file__).parent.joinpath('config.yaml')

openai.api_key = read_config('API-KEY',config_path)
model = read_config('model',config_path)
temperature = read_config('temperature',config_path)
prompt = read_config('prompt',config_path)

# messages = []
# def add_messages(role,mes):
#     messages.append({'role':role,'content':mes})

def Translate(line):
    messages = [
        {'role':'system','content':prompt},
        {'role':'user','content':line}
    ]
    def generate_answer():
        response = openai.ChatCompletion.create(
            model = model,
            messages = messages,
            temperature = temperature
        )
        content = response['choices'][0]['message']['content']
        # print(response['usage'])
        return content
    return generate_answer()


# print(Translate('人気の無い駐車場の隅に日向を連れ込み、有無を言わせずにしゃがませる。'))