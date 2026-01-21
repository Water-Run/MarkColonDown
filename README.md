# `Mark:down`

***[English](./README.md)***  

![Logo](./Assets/Logo.png)

`Mark:down` is a powerful Markdown template engine. As a strict superset of Markdown, it compiles to Markdown. With "line directives" starting with `#:` as its distinctive syntax, it provides the following capabilities for Markdown writing:

- *Syntactic sugar*: such as `#:4` (level 4 heading), `#:!`/`#:image` (image line), `#:row` and `#:column` (tables), etc.
- *Preprocessing capabilities*: such as `#:include` for file imports (implementing header-file-like functionality, or global variables placed in code blocks), `#:define` for macro definitions, etc.
- *Control flow*: including `#:if`, `#:else`, `#:while`, `#:for`, etc.
- *Embedded code*: embedding [neolua](https://github.com/neolithos/neolua), greatly expanding possibilities. Including `#:code` for executing code blocks, `{{}}` for embedding output in text, etc.
- *Template system*: implementing reuse of identical structures through `#:template`

`Mark:down` is developed using `C# AOT` and provides a `Visual Studio Code` extension.  

> `Mark:down` is open source on [GitHub](https://github.com/Water-Run/MarkColonDown), where you can read the [complete documentation](https://github.com/Water-Run/MarkColonDown/tree/main/Documents/CompiledDoucuments)

## Quick Overview

A typical `Mark:down` project directory should look like:  

```plaintext
│  Compile.md # Compilation entry point, the compiler will first enter this file and load corresponding compilation directives
│  Log.md # Log
│  Global.md # Stores global variables, templates, etc., automatically imported into every compiled file under default configuration
│
├─Compiled # Compilation results are stored in this directory
└─Source # "Source code"
```

The compilation process is shown in the following diagram:  

![Compilation Flow Diagram](./Assets/CompileFlow.png)  

## Compiler  

`mcd` is the compiler provided by `Mark:down`.  

After installation, use:  

```bash
mcd init
```

to initialize, which will generate `Compile.md` and the corresponding log `Log.md` in the directory.  

Use:  

```bash
mcd compile
```

to compile and output to the output directory.  

Compiler command reference:  

| Command   | Optional Parameters                                                                                                          | Description                                                                                                                                                                                                                                                                                                                          |
|-----------|------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init`    | `--entry <Path>` `--set <Name[=Value]>` *(repeatable)* `--without <Name>` *(repeatable)*                                     | Initialize (defaults to run directory, modifiable via `entry`), and write compilation directives specified by `--set` into the `#:compile` configuration section; `--without` is used to remove/not write certain directive items from the entry configuration section                                                               |
| `compile` | `--use <Config>` `--overwrite <Name[=Value]>` *(repeatable)* `--ignore <Name>` *(repeatable)* `--flag <Name>` *(repeatable)* | Execute compilation (defaults to using `Compile.md` as configuration, modifiable with `--use`); `--overwrite` overwrites/sets directive items in the entry configuration section for this compilation; `--ignore` temporarily disables directive items in the entry configuration section for this compilation; `--flag` adds a flag |

*Compilation Directives:*

| Directive Name       | Parameters                                         | Default Value                            | Description                                                                                                                                  |
|----------------------|----------------------------------------------------|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `Max_Compile_Time`   | Non-negative integer (ms)                          | Not set (timeout not enabled)            | Compilation time limit (milliseconds); timeout not enabled if not set                                                                        |
| `Max_Output_Bytes`   | Non-negative integer                               | Not set (no limit)                       | Maximum total output size (bytes); no limit if not set                                                                                       |
| `Max_Output_Files`   | Non-negative integer                               | Not set (no limit)                       | Maximum total output file count; no limit if not set                                                                                         |
| `Max_Include_Depth`  | Non-negative integer                               | Not set (no limit)                       | Upper limit for include recursion depth                                                                                                      |
| `Max_Template_Depth` | Non-negative integer                               | Not set (no limit)                       | Upper limit for template/use expansion depth                                                                                                 |
| `Disable_Code`       | None                                               | Not set (no limit)                       | Disable code embedding, will report error when encountered                                                                                   |
| `Ignore_Code`        | None                                               | Not set (no limit)                       | Ignore code embedding, no error when encountered                                                                                             |
| `Disable_Require`    | None                                               | Not set (no limit)                       | Disable `require(...)` statements in code, will report error when encountered                                                                |
| `Require_Version`    | Version expression (supports comparison operators) | `Mark:down` version executing `mcd init` | Require compiler version to meet condition (e.g., `>=1.2.0`)                                                                                 |
| `Include_Base`       | Path                                               | `./Source`                               | Base path for include relative path resolution                                                                                               |
| `Input_Path`         | Path                                               | `./Source`                               | Compilation input path                                                                                                                       |
| `Output_Path`        | Path                                               | `./Compiled`                             | Compilation output path                                                                                                                      |
| `Input_Glob`         | Path wildcard                                      | `**/*.md`                                | File wildcard for files to be treated as `Mark:down`                                                                                         |
| `Raw_Glob`           | Path wildcard                                      | (Empty)                                  | `Mark:down` cares but doesn't process: matched files are copied as-is to output directory (only effective when copy strategy is implemented) |
| `Ignore_Glob`        | Path wildcard                                      | `.mcdignore` `.mcdcopy`                  | `Mark:down` doesn't care and doesn't process: matched files don't enter output                                                               |
| `Log_Path`           | Path                                               | `Log.md`                                 | Log output path                                                                                                                              |
| `Global_Include`     | Path wildcard                                      | `./Global.md`                            | Automatically globally imported files (implicit `#include` at file beginning)                                                                |

## Syntax  

You can quickly overview the extended syntax capabilities provided by `Mark:down` from this reference table:  

| Syntax Structure     | Simplified Form | Description                                                                                                                                                                               |
|----------------------|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `#::`                | None            | Explicitly declares this is a Mark:down file (no functionality); also commonly used as a "comment line" (won't enter compiled Markdown).                                                  |
| `#:1`~`#:6`          | None            | x-level heading syntactic sugar; compiles to corresponding Markdown headings (`#`~`######`).                                                                                              |
| `#:image`            | `#:!`           | Image line; parameter is image path, optional "(annotation)"; compiles to Markdown image syntax.                                                                                          |
| `#:link`             | `#:&`           | Link line; parameter is URL, optional "(display text)"; compiles to Markdown link syntax.                                                                                                 |
| `#:row`              | `#:-`           | Table row (commonly used as first row/header row); comma-separated cells.                                                                                                                 |
| `#:column`           | `#:\|`          | Table row (commonly used for subsequent rows); comma-separated cells.                                                                                                                     |
| `#:ignore`           | `#:*`           | Skip entire file during compilation (the file produces no output). Can be viewed as syntactic sugar for `#:if false`.                                                                     |
| `#:skip`             | `#:~`           | Skip content between `skip` and `end` (or `=`), doesn't enter final Markdown. Can be viewed as syntactic sugar for `#:if false`.                                                          |
| `#:copy`             | `#:/`           | Copy entire file during compilation. Can be viewed as syntactic sugar for `#:raw`.                                                                                                        |
| `#:compile`          | `#:;`           | Compilation directive. Can only be placed in entry file.                                                                                                                                  |
| `#:echo`             | `#:>`           | Print information during compilation phase (for debugging/logging purposes), doesn't affect final output content.                                                                         |
| `#:end`              | `#:=`           | Universal terminator; ends blocks like `skip/raw/code/if/while/for/template`, etc.                                                                                                        |
| `#:include`          | `#:$`           | Import and directly merge another file (similar to preprocessing include).                                                                                                                |
| `#:define`           | `#:%`           | Macro substitution: replaces matched text with target text during compilation (for simple "global replacement/alias").                                                                    |
| `#:raw`              | `#:^`           | Raw output mode: between `raw` and `end` (or `=`), Mark:down directives are not parsed, original text enters output.                                                                      |
| `#:code`             | `#:?`           | Execute neolua code; supports single-line or code block form; code itself doesn't enter compilation output, but can set variables/environment for subsequent `{{}}` and control flow use. |
| `#:if`               | None            | Conditional branch start; followed by expression; used with `elif/else/end` (or `=`).                                                                                                     |
| `#:elif`             | None            | "Else if" in conditional branch.                                                                                                                                                          |
| `#:else`             | None            | "Else" in conditional branch.                                                                                                                                                             |
| `#:while`            | None            | while loop; followed by condition expression; ends with `end` (or `=`).                                                                                                                   |
| `#:for`              | None            | for loop; follows Lua syntax (e.g., `pairs/ipairs`); ends with `end` (or `=`).                                                                                                            |
| `#:template`         | `#:+`           | Declare template: `TemplateName: param1, param2...`; reuse structure within block through parameter names.                                                                                |
| `#:use`              | `#:@`           | Call template: `TemplateName: arg1, arg2...`, expand and generate output by replacing parameters in order.                                                                                |
| `{{ ... }}`          | None            | Embedded output: inserts expression result into text; `r{{}}` disables interpolation, preserves literal content.                                                                          |
| ` r`` ` and ` r``` ` | None            | Raw code blocks (no substitution).                                                                                                                                                        |

> After the line directive `#:`, you can add a `<>` to indicate the statement is recognized when the corresponding flag is met (otherwise the statement is considered non-existent). For example, `#:<flag1>if`  
>> Within `<>` there can be one or more flags: `&` means AND, `|` means OR, `!` means NOT, `()` means priority. For example, `#:<flag1&(flag2|!flag3)>else`  

*Example:*

```markdown
#:: `#::` explicitly declares this is a Mark:down file, you can also use it as a comment  
#:: Note that `#:` is immediately followed by the corresponding directive, don't include spaces

#:: x-level heading syntactic sugar
#:1
#:2
#:3
#:4
#:5
#:6

#:: Image line, two equivalent ways of writing
#:image ./MyImage.png
#:! ./MyImage.png (with annotation description, otherwise no annotation)

#:: Link line
#:link http://mylink.com (displays as content in parentheses, otherwise display text and link text are identical)
#:& http://mylink.com

#:: A two-column, three-row table, you can also use the full names `#:row` and `#:column`  
#:- row1, row2
#:| 1, 2
#:| 3, 4

#:: ignore will skip the entire file during compilation
#:ignore

#:: skip will skip the corresponding part during compilation
#:skip

#:: echo will print corresponding information during compilation
#:echo Compilation reached here
#:: Simplified form of echo with flag, only displays when the flag is marked during compilation  
#:<isflagged>> and flag is marked  

This part of the content will be skipped and won't appear in the final compilation result

#:: Universal terminator symbol, including `#:if`, `#:for`, `#:code`, etc. all use this symbol. Can also be written in simplified form
#:end
#:=

#:: Directly merge another file  
#:include AnotherDocument.md

#:: Substitution
#:define True False

True will be replaced with False during compilation // After compilation: False will be replaced with True

#:: Preserve native content, skip syntax provided by Mark:down
#:raw

This True will still be True after compilation

#:=

#:: code executes code. If code is followed by non-empty content, it's a single line of code; if code is followed by empty content, the middle part is treated as a code block
#:: Code executed in code won't output to the compiled Markdown
#:code version = "1.0" -- neolua syntax
#:code
require("../global.lua") -- Can import other lua files

print("Mark:down does not guarantee the safety of called code, does not run in a sandbox, while flexible and powerful you need to be responsible for the safety of the code yourself")

version = global.version
count = 0
#:=

#:: {{}} represents embedded block, will embed the result of the corresponding expression. Use r{{}} to avoid embedding
The version of the document is {{ version }}
And this r{{ version }} will retain exactly the same text after compilation

#:: Selection control flow, followed by an expression
#:if version == "1.0"
Version is 1.0
#:elif version == "2.0"
Version is 2.0
#:else
Version is another version
#:=

#:: while loop, also followed by expression
#:while count < 10
Loop number {{ count }}
#:code count += 1

#:- Keyword, Description
#:: for loop, follows lua syntax, can use pairs or ipairs
#:: Print the keyword and description list of Mark:down
#:for keyword, info in pairs(global.mark_colon_down_keyword)
#:| keyword, info
#:=

#:: Template system, used for structure reuse
#:: Declare template name (PascalCase): parameter name (camelCase), equivalent to define substitution
#:template ProgramInfo: name, author, version
Software name: name
Author: author
Version: version
#:=

#:: Call this template
#:use ProgramInfo: Quick Example, WaterRun, 1.0

#:: We more commonly place called templates in a separate shared .md file, then include it for access
```
