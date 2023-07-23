import opencc
import re

class TextParser:
    def __init__(self,rules=[]) -> None:
        self.T_convert = opencc.OpenCC('t2s.json')
        self.S_convert = opencc.OpenCC('s2t.json')
        self.rules = rules

    def parser(self,lines:list[str]):
        line_conut = 0
        selection = []
        for line in lines:
            # 遍历每一句话 line
            line_conut += 1
            temp_str = [line.strip()]
            for rule in self.rules:
                # 每执行一次规则中的步骤，temp_str就要改变。
                new_temp_str = []
                for k in rule:
                    key = k
                value = rule[key]
                for (_str) in temp_str:
                    if key == 'remove':
                        res = re.sub(value,'',_str)
                        if res.strip() != '':
                            new_temp_str.append(res)
                    elif key == 'find':
                        new_temp_str.extend(re.findall(value,_str))
                    elif key == 'replace':
                        args = value.split('-->')
                        new_temp_str.append(_str.replace(args[0],args[1]))
                    elif key == 'other':
                        if value == 's2t':
                            new_temp_str.append(self.S_convert.convert(_str))
                        elif value == 't2s':
                            new_temp_str.append(self.T_convert.convert(_str))
                temp_str = new_temp_str
            for _str in temp_str:
                position = line.find(_str)
                selection.append((line_conut,position + 1,line_conut,position + len(_str) + 1))
        return selection
