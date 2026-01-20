# `Mark:down`

***[English](./README.md)***  

![Logo](./Assets/Logo.png)

## 概述

`Mark:down`是一个强大的 Markdown 模板引擎, 作为 Markdown 的严格超集, 编译为 Markdown, 为 Markdown 的编写提供了:

- 语法糖: 如`#:4`(四级标题), `#:!`/`#:image`(图片行), `#:row`和`#:column`(表格)等
- 预处理: 如`#:include`进行文件导入, `#:define`宏定义等
- 控制流: 包括`#:if`, `#:else`, `#:while`, `#:for`等
- 内嵌代码: 内嵌[neolua](https://github.com/neolithos/neolua), 极大扩展可能. 包括`#:code`执行代码块, `{{}}`在文本中内嵌输出等
- 模板系统: 通过`#:template`实现相同结构复用

`Mark:down`标志性的语法是`#:`开头的"行指令", 以及`{{}}`的内嵌输出.

`Mark:down`使用`C# AOT`开发, 提供`Visual Studio Code`插件.

> `Mark:down`开源于[GitHub](https://github.com/Water-Run/MarkColonDown), 你可以在上面阅读[完整文档](https://github.com/Water-Run/MarkColonDown/tree/main/Documents/CompiledDoucuments)

## 速览

一个`Mark:down`项目的典型目录应当如:  

```plaintext
│  Compile.md # 编译入口, 编译器将首先进入此文件, 加载对应的编译指令
│  Log.md # 日志
│  Global.md # 存储全局的变量, 模板等内容, 默认配置下自动导入每一个编译的文件中
│
├─Compiled # 编译后的结果存储在此目录
└─Source # "源码"
```

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

编译器指令参考:  

| 指令      | 可选参数                                                                                                         | 说明                                                                                                                                                                                                        |
|-----------|------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init`    | `--entry <Path>` `--set <Name[=Value]>` *(可重复)* `--without <Name>` *(可重复)*                                 | 初始化(默认在运行目录, 可通过`entry`修改)，并将 `--set` 指定的编译指令写入 `#:compile` 配置区；`--without` 用于从入口配置区移除/不写入某个指令项                                                            |
| `compile` | `--use <Config>` `--overwrite <Name[=Value]>` *(可重复)* `--ignore <Name>` *(可重复)* `--flag <Name>` *(可重复)* | 执行编译(默认使用`Compile.md`作为配置, 可使用`--use`进行修改)；`--overwrite` 在本次编译中覆写/设置入口配置区中的指令项；`--ignore` 在本次编译中临时禁用入口配置区中的指令项；`--flag`添加标记(对应编译行为) |

*编译指令:*

| 指令名               | 参数                     | 默认值                          | 说明                                                                           |
|----------------------|--------------------------|---------------------------------|--------------------------------------------------------------------------------|
| `Max_Compile_Time`   | 非负整数(ms)             | 未设置（不启用超时）            | 编译限时（毫秒）；未设置则不启用超时                                           |
| `Max_Output_Bytes`   | 非负整数                 | 未设置（不限制）                | 最大总输出大小（字节）；未设置则不限制                                         |
| `Max_Output_Files`   | 非负整数                 | 未设置（不限制）                | 最大总输出文件数；未设置则不限制                                               |
| `Max_Include_Depth`  | 非负整数                 | 未设置（不限制）                | include 递归深度上限                                                           |
| `Max_Template_Depth` | 非负整数                 | 未设置（不限制）                | template/use 展开深度上限                                                      |
| `Disable_Code`       | 无                       | 未设置（不限制）                | 禁用代码内嵌, 出现内嵌时将会报错                                               |
| `Ignore_Code`        | 无                       | 未设置（不限制）                | 忽略代码内嵌, 出现时不报错                                                     |
| `Disable_Require`    | 无                       | 未设置（不限制）                | 禁用代码中的 `require(...)` 语句, 出现时将会报错                               |
| `Require_Version`    | 版本表达式（支持比较符） | 执行`mcd init`的`Mark:down`版本 | 要求编译器版本满足条件（如 `>=1.2.0`）                                         |
| `Include_Base`       | 路径                     | `./Source`                      | include 相对路径解析的基路径                                                   |
| `Input_Path`         | 路径                     | `./Source`                      | 编译输入路径                                                                   |
| `Output_Path`        | 路径                     | `./Compiled`                    | 编译输出路径                                                                   |
| `Input_Glob`         | 路径通配符               | `**/*.md`                       | 需要被当作 `Mark:down` 处理的文件通配符                                        |
| `Raw_Glob`           | 路径通配符               | （空）                          | `Mark:down` 关心但不处理：匹配文件原样复制到输出目录（仅在实现复制策略时生效） |
| `Ignore_Glob`        | 路径通配符               | `.mcdignore` `.mcdcopy`         | `Mark:down` 不关心也不处理：匹配文件不进入输出                                 |
| `Log_Path`           | 路径                     | `Log.md`                        | 日志输出路径                                                                   |
| `Overwrite_Output`   | `On/Off`                 | `On`                            | 输出文件已存在时是否覆写                                                       |
| `GlobalInclude`      | 路径通配符               | `./Global.md`                   | 自动全局导入的文件(文件开头隐含`#include`)                                     |

## 语法  

可从此参考表速览`Mark:down`提供的扩展语法能力:  

| 语法结构            | 等效简化 | 说明                                                                                                          |
|---------------------|----------|---------------------------------------------------------------------------------------------------------------|
| `#::`               | 无       | 显式声明这是一个 Mark:down 文件(无功能)；也常作为作为“注释行”使用（不会进入编译后的 Markdown）。              |
| `#:1`~`#:6`         | 无       | x 级标题语法糖；编译为对应 Markdown 标题（`#`~`######`）。                                                    |
| `#:image`           | `#:!`    | 图片行；参数为图片路径，可选“(注解)”；编译为 Markdown 图片语法。                                              |
| `#:link`            | `#:&`    | 链接行；参数为 URL，可选“(显示文本)”；编译为 Markdown 链接语法。                                              |
| `#:row`             | `#:-`    | 表格行（常用作第一行/表头行）；逗号分隔单元格。                                                               |
| `#:column`          | `#:\|`   | 表格行（常用作后续行）；逗号分隔单元格。                                                                      |
| `#:ignore`          | `#:*`    | 编译时跳过整个文件（该文件不产生任何输出）。可以视为`#:if false`的语法糖。                                    |
| `#:skip`            | `#:~`    | 跳过 `skip` 与 `end`（或 `=`）之间的内容，不进入最终 Markdown。可以视为`#:if false`的语法糖。                 |
| `#:copy`            | `#:/`    | 编译时复制整个文件。可以视为`#:raw`的语法糖。                                                                 |
| `#:compile`         | `#:;`    | 编译指令。只能放在入口文件。                                                                                  |
| `#:echo`            | `#:>`    | 编译阶段打印信息（调试/日志用途），不影响最终输出内容。                                                       |
| `#:end`             | `#:=`    | 通用终止符；结束 `skip/raw/code/if/while/for/template` 等块。                                                 |
| `#:include`         | `#:$`    | 导入并直接合并另一个文件（类似预处理 include）。                                                              |
| `#:define`          | `#:%`    | 宏替换：编译期将匹配到的文本替换为目标文本（用于简易“全局替换/别名”）。                                       |
| `#:raw`             | `#:^`    | 原样输出模式：`raw` 与 `end`（或 `=`）之间不解析 Mark:down 指令，按原文进入输出。                             |
| `#:code`            | `#:?`    | 执行 neolua 代码；支持单行或代码块形式；代码本身不进入编译输出，但可设置变量/环境供后续 `{{}}` 与控制流使用。 |
| `#:if`              | 无       | 条件分支开始；后跟表达式；与 `elif/else/end`（或 `=`）配合使用。                                              |
| `#:elif`            | 无       | 条件分支的“否则如果”。                                                                                        |
| `#:else`            | 无       | 条件分支的“否则”。                                                                                            |
| `#:while`           | 无       | while 循环；后跟条件表达式；以 `end`（或 `=`）结束。                                                          |
| `#:for`             | 无       | for 循环；遵循 Lua 语法（如 `pairs/ipairs`）；以 `end`（或 `=`）结束。                                        |
| `#:template`        | `#:+`    | 声明模板：`TemplateName: param1, param2...`；块内通过参数名复用结构。                                         |
| `#:use`             | `#:@`    | 调用模板：`TemplateName: arg1, arg2...`，按参数顺序替换展开生成输出。                                         |
| `{{ ... }}`         | 无       | 内嵌输出：将表达式结果插入文本；`r{{}}` 禁用插值，保留字面量内容。                                            |
| ` r`` ` 和 ` r``` ` | 无       | 原始代码块(不替换)。                                                                                          |

*示例:*

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
#:! ./我的图片.png (带注解说明,否则无注解)

#:: 链接行
#:link http://mylink.com (显示为括号内的内容, 否则显示文本和链接文本一致)
#:& http://mylink.com

#:: 一个两列三行的表格, 你也可以用`#:row`和`#:column`全称  
#:- row1, row2
#:| 1, 2
#:| 3, 4

#:: ignore 将在编译时跳过整个文件
#:ignore

#:: skip 将在编译时跳过对应的部分
#:skip

#:: echo 将在编译时打印对应的信息
#:echo 编译到这里了

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

#:: 代码块可以使用r```和r``, 不会被转义  
下面是一段Vue代码, 包括r`{{ }}`, 不会被转译:  

r```
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <title>Vue {{}} 最简单示例</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  </head>

  <body>
    <div id="app">
      <h1>{{ message }}</h1>
    </div>

    <script>
      const { createApp } = Vue;

      createApp({
        data() {
          return {
            message: "Hello, Vue!"
          };
        }
      }).mount("#app");
    </script>
  </body>
</html>
```

#:: code 执行代码. 如果 code 后非空, 为一行代码; 如果 code 后为空, 则中间的视为代码块
#:: 在 code 中执行的代码不会输出到编译后的 Markdown 中
#:code version = "1.0" -- neolua 语法
#:code
require("../global.lua") -- 可以导入其它的 lua 文件

print("Mark:down 不保证调用代码的安全性, 不在沙箱中运行, 灵活强大的同时你需要自己为代码的安全性负责")

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

#:- 关键字, 说明
#:: for 循环, 遵循 lua 语法, 可以用 pairs 或者 ipairs
#:: 打印 Mark:down 的关键字和说明列表
#:for keyword, info in pairs(global.mark_colon_down_keyword)
#:| keyword, info
#:=

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
