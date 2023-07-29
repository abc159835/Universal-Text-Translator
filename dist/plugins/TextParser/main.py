

from module.TextParse import register
import opencc

def init():
    global S_convert
    global T_convert
    T_convert = opencc.OpenCC('t2s.json')
    S_convert = opencc.OpenCC('s2t.json')

@register('convert')
def convert(value,_str):
    global S_convert
    global T_convert

    if value == 's2t':
        new_str = S_convert.convert(_str)
    elif value == 't2s':
        new_str = T_convert.convert(_str)

    if new_str.strip() != '':
        yield new_str, 0, len(_str)

def close():
    print('Finish!')