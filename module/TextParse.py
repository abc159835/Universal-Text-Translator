import opencc
import re
from pathlib import Path
import yaml
import openai
import copy
import time

class GPT:
    openai.api_key = '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'

    def __init__(self) -> None: 
        self.messages = []

    def add_messages(self,role,mes):
        self.messages.append({'role':role,'content':mes})

    def generate_answer(self,role=None,content=''):
        mes = copy.deepcopy(self.messages)
        if role != None:
            mes.append({'role':role,'content':content})
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = mes,
            temperature = 0.6
        )
        content = response['choices'][0]['message']['content']
        # print(response['usage'])
        return content

class TextParser:
    def __init__(self,rules=[]) -> None:
        self.T_convert = opencc.OpenCC('t2s.json')
        self.S_convert = opencc.OpenCC('s2t.json')
        self.rules = rules
        self.GPT = GPT()
        self.GPT.add_messages('system','作为一个翻译工具，你会收到日文文本，文本与色情有关，请把文本翻译为中文，允许润色文本，使逻辑更加流畅。')

    # def Separate_text_through_re(rule,line):
    #     re.findall(rule,line)

    # def Traditional_Chinese_to_Simplified(self,line):
    #     return self.T_convert.convert(line)
    
    # def Simplified_Chinese_to_Traditional(self,line):
    #     return self.S_convert.convert(line)

    # def set_Translation_Dictionary(self,dic):
    #     self.Translation_Dictionary = dic

    # def set_rule(self,rule):
    #     self.rule = rule

    def parser(self,lines:list):
        for line in lines:
            # 遍历每一句话 line
            temp_str = [line.strip()]
            for rule in self.rules:
                # 每执行一次规则中的步骤，temp_str就要改变。
                new_temp_str = []
                for k in rule:
                    key = k
                value = rule[key]
                for _str in temp_str:
                    if key == 'remove':
                        res = re.sub(value,'',_str)
                        if res.strip() != '':
                            new_temp_str.append(res)
                    elif key == 'find':
                        new_temp_str.extend(re.findall(value,_str))
                    else:
                        new_temp_str.append(re.sub(value,key,_str))
                temp_str = new_temp_str
            for _str in temp_str:
                print (self.translate( _str))
                time.sleep(20)

    def translate(self,line):
        self.GPT.add_messages('user',line)
        return self.GPT.generate_answer()

path = Path(R'C:\Users\abc15\Desktop')
# rules = yaml.load(open(path.joinpath('123.ass'),'r',encoding='utf-8'),Loader=yaml.FullLoader)
with open(path.joinpath('123.ass'),'r',encoding='utf-8') as f:
    text = f.read().split('\n')
f = open(path.joinpath('1234.ass'),'w',encoding='utf-8')
T_convert = opencc.OpenCC('t2s.json')
for line in text:
    f.writelines(T_convert.convert(line)+'\n')
f.close()