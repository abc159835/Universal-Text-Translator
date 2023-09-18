# Univerasl Text Translator

——一个插件化的游戏脚本翻译编辑器

（正则文本提取 + 预翻译 + 文本编辑器）

![](./assets/UTT.png)

## Features

 - 软件本身定义了一套文本提取方法，兼具简洁与自由度
 - 翻译方法以插件形式裸露，完全自定义，可自己扩展
 - 提取方法以插件形式裸露，完全自定义，可自己扩展
 - 具备完善的文本编辑器，方便修改预翻译文本
 - 运行时动态检测 配置文件、 脚本文件变化，无需重启
 - 文本高亮显示：三种高亮文本类型
 - 任务列表实时显示预翻译进度
 - 实验中：fix语句锁定关键字在翻译前后不变

## 提取方法介绍

配置文件实例：
```yaml
step:
  - try-find: 
    - text=\"(.*?)\"
  - remove: 
    - ^[*;@#].*$
    - //.*$
    - \[.*?\]
    - 「
    - 」
  - include: 
    - jp
  - exclude: 
    - \".*?\"
    - \'.*\'

fix:
  失敗: 失败

fix-after:
  Alice: 爱丽丝  
```

### step 项定义查找游戏内文本步骤

将多行（行数为n）的文本文件视作n个区块，每个区块占有一行。
程序将逐行执行给定指令，使得区块缩小。

+ remvoe 指令 通过正则表达式匹配文本，丢弃匹配文本，缩小区块。
+ try-find 指令 通过正则表达式匹配文本，丢弃未匹配文本，缩小区块。
+ find 指令 通过正则表达式匹配文本，丢弃未匹配文本，缩小区块。
  + 区别于 try-find的是：find若在区块中未匹配任意文本，则丢弃整个区块，而 try-find不会。
+ include 指令 通过正则表达式匹配文本，丢弃没有文本匹配的区块。
+ exclude 指令 通过正则表达式匹配文本，丢弃有文本匹配的区块。

### fix 语句锁定关键字在翻译前后不变

原理比较简陋（以示例说明）：

+ 在翻译前将文本的中的 失敗 替换为 失败
+ 翻译中 失败 大概率不会被翻译，即发生更改的可能性低
+ 翻译后将文本的中的 失败 替换回 失敗
+ fix 语句的键可以是 正则表达式，但不推荐这样做。

等价写法：
```yaml
fix-before:
  失敗: 失败

fix-after:
  失败: 失敗  
```

## 插件自定义介绍

### TextParser

通过改写 插件文件夹 中 `main.py`文件，可自定义添加功能。

以下拿 `.\plugins\TextParser\main.py`举例：

```py
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
```

脚本文件中的特定名称函数，这即是程序入口

通用的入口有：
+ `init()`
  + 程序初始化时执行
+ `close()`
  + 程序被关闭时执行

以上代码为 step项添加了一个语句 `convert`
+ value是 convert的键，而 _str是区块文本。

于是可以这样使用，使得区块文本简繁转换。
```yaml
step:
  - convert: t2s
```
### Translator

大同小异，懒得写了，反正也没人用（笑），自己去看文件夹里是示例代码吧。

提醒几点：
+ `translate(lines: list[str])` 是翻译接口。
+ 没有 `return`型的函数，只有 `yield`型 和 `void`型的函数。

## Credits

 - [Ns Emu Tools](https://github.com/triwinds/ns-emu-tools) - Ns Emu Tools
