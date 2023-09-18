from module.env import PATH
import re

register_func = {}

def finditer(pattern: str, line: str):
    for m in re.finditer(pattern=pattern, string=line):
        g = m.groups()
        if len(g) > 0:
            for c in range(len(g)):
                p = m.span(c + 1)
                if m.group(c + 1).strip() != '':
                    yield m.group(c + 1), p[0], p[1]
        else:
            new_str = m.group()
            if new_str.strip() != '':
                yield new_str, m.start(), m.end()

def relist_to_str(var):
    if type(var) == list:
        return '|'.join(var)
    else:
        return var


def init():
    global language_range

    # 避免循环引用
    from module.OShelper import read_config
    language_range = read_config('language',PATH.joinpath('global_config.yaml'),{})



def register(name :str):
    global register_func
    def decorator(func):
        register_func[name] = func
        return func
    return decorator


def get_language(value):
    global language_range
    range_ = language_range.get(value)
    if range_ != None: 
        value = range_
    return value


@register('remove')
def findexcludeiter(pattern: str, line: str):
    start = 0
    for x in re.finditer(pattern=relist_to_str(pattern),string=line):
        g = x.groups()
        if len(g) > 0:
            for c in range(len(g)):
                p = x.span(c + 1)
                end = p[0]
                if start < end:
                    yield line[start:end], start, end
                start = p[1]
        else:
            end = x.start()
            if start < end:
                yield line[start:end], start, end
            start = x.end()
    end = len(line)
    if start < end:
        yield line[start:end], start, end


@register('find')
def find(value, _str):
    for new_str,start,end in finditer(relist_to_str(value), _str):
        yield new_str,start,end

@register('try-find')
def find(value, _str):
    find = False
    for new_str,start,end in finditer(relist_to_str(value), _str):
        find = True
        yield new_str,start,end
    if not find:
        yield _str, 0, len(_str)


@register('include')
def include(value, _str):
    value = relist_to_str(value)
    res = re.findall(value,_str)
    if len(res) > 0:
        yield _str, 0, len(_str)


@register('exclude')
def exclude(value, _str):
    value = relist_to_str(value)
    res = re.findall(value,_str)
    if len(res) == 0:
        yield _str, 0, len(_str)


@register('replace')
def replace(value, _str):
    for values, new_str in value:
        values = get_language(values)
        for _, start, end in finditer(values, _str):
            yield new_str, start, end



class TextParser:
    def __init__(self, rule={}) -> None:    
        rules =  rule.get('step')
        fixs = rule.get('fix')
        fixs_after = rule.get('fix_after')
        fixs_before = rule.get('fix_before')
        self.rules = []
        self.fixs = {}
        self.fixs_after = {}
        self.fixs_before = {}

        if rules != None:
            # 尝试使用预设的正则替换关键字
            for c in range(len(rules)):
                rule = rules[c]

                # 得到 key 与 value
                for k in rule:
                    key = k
                    break
                value = rule[key]

                if type(value) == str:
                    rules[c][key] = get_language(value)
                elif type(value) == list:
                    for v in range(len(value)):
                        rules[c][key][v] = get_language(value[v])

            self.rules = rules

        if fixs != None:
            self.fixs = fixs

        if fixs_before != None:
            self.fixs_before = fixs_before

        if fixs_after != None:
            self.fixs_after = fixs_after



    def parser(self, lines: list[str]):
        """
        remove: 正则移除选区
        find: 正则筛选选区

        include: 根据字符组成筛选选区
        exclude: 根据字符组成筛选选区

        convert: 简体与繁体中文互转
        replace: 改变文本
        fix: 固定文本中的内容，使其翻译前后不变。
        """
        global register_func
        global offset
        
        row = 1
        selections = []
        str_list = []

        for line in lines:
            # 遍历每一句话 line
            # temp_str 与 selection 的长度应始终相等。

            strip_line = line.strip()
            temp_str:list = [strip_line]
        
            p = line.find(strip_line)
            selection = [(p,p + len(strip_line))]

            for rule in self.rules:
                # 每执行一次规则中的步骤，temp_str就要改变。
                # 谨慎使用 replace，因为其可越界替换。

                if len(temp_str) == 0:
                    break

                # 得到 key 与 value
                for k in rule:
                    key = k
                    break
                value = rule[key]

                # new_temp_str 中不要提交 ''
                new_temp_str = []
                new_selection = []

                # 替换所引起的位移修正
                offset = 0

                for c in range(len(temp_str)):
                    _str = temp_str[c]
                    parent_start, _ = selection[c]
                    parent_start += offset

                    func = register_func.get(key)

                    def main(new_str, start, end):
                        global offset
                        _start = parent_start + start + offset
                        original_str = _str[start:end]
                        if new_str != original_str:
                            lines[row - 1] = lines[row - 1][:_start] + new_str + lines[row - 1][parent_start + end:]
                            if len(new_str) != len(original_str):
                                offset += len(new_str) - len(original_str)

                        new_temp_str.append(new_str)
                        new_selection.append((_start, parent_start + end + offset))
                    main_func = main

                    if func != None:
                        generator = func(value, _str)
                        
                        try:
                            temp = next(generator)
                        except:
                            temp = None

                        for _temp in generator:
                                
                            new_str, start, end = temp
                            temp = _temp

                            if temp[1] == end:
                                temp = list(temp)
                                temp[0] = new_str + temp[0] 
                                temp[1] = start
                                temp = tuple(temp)
                            else:
                                main_func(new_str, start, end)
                            
                        
                        if temp != None:
                            main_func(*temp)

                # 每走一步，重新计算
                selection = new_selection
                temp_str = new_temp_str

            for start, end in selection:
                selections.append([row, start + 1, row, end + 1])
                str_list.append(lines[row - 1][start: end])

            row += 1

        return selections, '\n'.join(lines), str_list
    

    def translate(selections,content):
        from module.Translate import translate_dict
        lines = content.split('\n')
        new_selections = []
        translate_bool = []
        offset = 0
        old_row = 1
        for row, start, _, end in selections:
            if old_row != row:
                offset = 0
                old_row = row
            origin = lines[row - 1][offset + start - 1:offset + end - 1]
            text = translate_dict.get(origin)
            _start = offset + start
            if text:
                lines[row - 1] = lines[row - 1][:offset + start - 1] + text.replace('\n','\t') + lines[row - 1][offset + end - 1:]
                offset += len(text) - len(origin)
                translate_bool.append(True)
            else:
                translate_bool.append(False)
            new_selections.append([row, _start, row, offset + end])
        return new_selections, '\n'.join(lines), translate_bool
    
    def fix_before(self, strs: list[str]):
        self.fix_list = []
        for c in range(len(strs)):
            Str = strs[c]
            _str_list = []
            offset = 0
            for key,value in self.fixs.items():
                for _str, start, end in finditer(pattern=key, line=Str):
                    _str_list.append(_str)
                    strs[c] = strs[c][:offset + start] + value + strs[c][offset + end:]
                    offset += len(value) - len(_str)
                Str = strs[c]
                offset = 0
            
            self.fix_list.append(_str_list)

            for key,value in self.fixs_before.items():
                for _str, start, end in finditer(pattern=key, line=Str):
                    strs[c] = strs[c][:offset + start] + value + strs[c][offset + end:]
                    offset += len(value) - len(_str)
                Str = strs[c]
                offset = 0

        return strs

    def fix_after(self, strs: list[str]):
        for c in range(len(strs)):
            Str = strs[c]
            _str_list = self.fix_list[c]
            count = 0
            for _, value in self.fixs.items():
                count += Str.count(value)
            if count == len(_str_list):
                count = 0
                offset = 0
                for _, value in self.fixs.items():
                    for _, start, end in finditer(pattern=value, line=Str):
                        strs[c] = strs[c][:offset + start] + _str_list[count] + strs[c][offset + end:]
                        offset += len(_str_list[count]) - len(value)
                        count += 1
                    Str = strs[c]
                    offset = 0
            
            for key,value in self.fixs_after.items():
                for _str, start, end in finditer(pattern=key, line=Str):
                    strs[c] = strs[c][:offset + start] + value + strs[c][offset + end:]
                    offset += len(value) - len(_str)
                Str = strs[c]
                offset = 0
        return strs