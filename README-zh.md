# `Mark:down`

***[English](./README.md)***

![Logo](./Assets/Logo.png)

`Mark:down`是一个强大的 Markdown 预处理器, 作为 Markdown 的严格超集, 编译为 Markdown, 以`#:`开头的"行指令"为标志性的语法为 Markdown 的编写提供了:

* *语法糖*: 如`#:4`(四级标题), `#:!`/`#:image`(图片行), `#:-`/`#:table`(表格块, CSV语法)等
* *预处理能力*: 如`#:include`进行文件导入(实现类似头文件, 或置于代码块中的全局变量), `#:define`宏定义等
* *控制流*: 包括`#:if`, `#:else`, `#:while`, `#:for`等
* *内嵌代码*: 内嵌 [MiniScript](https://github.com/JoeStrout/miniscript/tree/master/MiniScript-cs), 极大扩展可能. 包括`#:code`执行代码块, `{{}}`在文本中内嵌输出等
* *模板系统*: 通过`#:template`实现相同结构复用

`Mark:down`使用`C# AOT`开发, 提供`Visual Studio Code`插件.

> `Mark:down`开源于[GitHub](https://github.com/Water-Run/MarkColonDown), 你可以在上面阅读[完整文档](https://github.com/Water-Run/MarkColonDown)

## 速览

一个`Mark:down`项目的典型目录应当如:

```plaintext
│  Compile.mcd # 编译入口, 编译器将首先进入此文件, 加载对应的编译指令
│  Log.mcd # 日志
│  Global.mcd # 存储全局的变量, 模板等内容, 默认配置下自动导入每一个编译的文件中
│
├─Compiled # 编译后的结果存储在此目录
└─Source # "源码"
```

编译流程如下图所示:

![编译流程图](./Assets/CompileFlow.png)

## 编译器

`mcd`是`Mark:down`提供的编译器.

安装后, 使用:

```bash
mcd init
```

进行初始化, 这将在目录下生成`Compile.md`以及对应的日志`Log.md`.

使用:

```bash
mcd compile
```

进行编译, 输出至输出目录.

## 能力

`Mark:down`的扩展语法可由以下速览:  

- `#::` : 显式声明`Mark:down`文件(常做注释)  
- `#:1`~`#:6` : x 级标题语法糖
- `#:image` / `#:!` : 图片行语法糖
- `#:link` / `#:&` : 链接行语法糖
- `#:table` / `#:-` : 表格块语法糖。
- `#:ignore` / `#:*` : 跳过整个文件。
- `#:skip` / `#:~` : 跳过部分内容
- `#:copy` / `#:/` : 复制整个文件
- `#:compile` / `#:;` : 编译指令
- `#:echo` / `#:>` : 编译阶段打印信息
- `#:end` / `#:=` : 通用终止符
- `#:include` / `#:$` : 导入并合并另一个文件
- `#:define` / `#:%` : 宏替换。
- `#:raw` / `#:^` : 原样输出
- `#:code` / `#:?` : 执行 MiniScript 代码
- `#:if` : 条件分支开始
- `#:elif` : 条件分支的"否则如果"
- `#:else` : 条件分支的"否则"
- `#:while` : while 循环
- `#:for` : for 循环
- `#:template` / `#:+` : 声明模板
- `#:use` / `#:@` : 调用模板
- `{{ ... }}` : 内嵌表达式输出
- ` r`` ` 和 ` r``` ` : 原始代码块

*使用示例:*

```markdown
#:: `#::`显式的声明这是一个 Mark:down 文件, 你也可以作为注释使用  
#:: 注意`#:`后紧跟对应指令, 不要有空格

#:: x 级标题语法糖
#:1
#:2
#:3
#:4
#:5
#:6

#:: 图片行, 两种写法等效
#:image ./我的图片.png
#:! ./我的图片.png(带注解说明,否则无注解)

#:: 链接行
#:link http://mylink.com(显示为括号内的内容, 否则显示文本和链接文本一致)
#:& http://mylink.com

#:: 链接行前缀
#:&- https://github.com/Water-Run/MarkColonDown(Mark:down)
#:&GitHub: https://github.com/Water-Run/MarkColonDown(Mark:down)

#:: 一个两列三行的表格, 你也可以用`#:table`全称  
#:-
row1, row2
1, 2
3, 4
#:=

#:: ignore 将在编译时跳过整个文件
#:ignore

#:: skip 将在编译时跳过对应的部分
#:skip

#:: echo 将在编译时打印对应的信息
#:echo 编译到这里了
#:: echo的简化形式与flag, 仅在编译标记对应flag的时候显示  
#:<isflagged>> 且标记了flag  

此部分内容将被跳过, 不在最终编译结果中出现

#:: 通用中止符号, 包括`#:if`, `#:for`, `#:code`等均使用此符号. 也可以写为简化形式
#:end
#:=
 
#:: 直接合并另一个文件  
#:include 另一个文档.md

#:: 替换
#:define True False

True 将在编译时替换为 False // 编译后: False 将在编译时替换为 True

#:: 保留原生内容, 跳过 Mark:down 提供的语法
#:raw

这个 True 在编译后仍然是 True

#:=

#:: code 执行代码. 如果 code 后非空, 为一行代码; 如果 code 后为空, 则中间的视为代码块
#:: 在 code 中执行的代码不会输出到编译后的 Markdown 中
#:code version = "1.0" // MiniScript 语法

#:code
import "global" // 导入 global.ms（由运行环境决定 import 的具体查找规则）

print "Mark:down 不保证调用代码的安全性, 不在沙箱中运行, 灵活强大的同时你需要自己为代码的安全性负责"

version = global.version
count = 0
#:=

#:: {{}}表示内嵌块, 会嵌入对应表达式的结果. 使用 r{{}}避免嵌入
文档的版本是 {{ version }}
而这个 r{{ version }}编译后的文本会保留完全一致

#:: 选择控制流, 跟随一个表达式
#:if version == "1.0"
版本是 1.0
#:elif version == "2.0"
版本是 2.0
#:else
版本是其它版本
#:=

#:: while 循环, 同样跟随表达式
#:while count < 10
第 {{ count }} 次循环
#:code count += 1
#:end

#:- 关键字, 说明
#:: for 循环, 遵循 MiniScript 的 for-in 风格
#:: 打印 Mark:down 的关键字和说明列表
#:-
关键字, 说明
#:for kv in global.mark_colon_down_keyword
{{ kv.key }}, {{ kv.value }}
#:end
#:end

#:: 模板系统, 用于复用结构
#:: 声明模板名(大驼峰): 参数名(小驼峰), 相当于 define 替换
#:template ProgramInfo: name, author, version
软件名: name
作者: author
版本: version
#:=

#:: 调用该模板
#:use ProgramInfo: 快速示例, WaterRun, 1.0

#:: 我们更常将调用的模板放置在一个独立的公用.md 文件中, 然后 include 进来进行访问
```
