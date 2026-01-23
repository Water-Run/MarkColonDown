# `Mark:down`

***[English](./README.md)***  

![Logo](./Assets/Logo.png)

`Mark:down` is a powerful Markdown template engine that serves as a strict superset of Markdown, compiles to Markdown, and features "line directives" starting with `#:` as its signature syntax, providing the following capabilities for Markdown writing:

- *Syntactic Sugar*: Such as `#:4` (level 4 heading), `#:!`/`#:image` (image line), `#:-`/`#:table` (table block with CSV syntax), etc.
- *Preprocessing Capabilities*: Such as `#:include` for file imports (implementing header file-like functionality, or global variables placed in code blocks), `#:define` for macro definitions, etc.
- *Control Flow*: Including `#:if`, `#:else`, `#:while`, `#:for`, etc.
- *Embedded Code*: Embedded [neolua](https://github.com/neolithos/neolua), greatly expanding possibilities. Including `#:code` for executing code blocks, `{{}}` for embedding output in text, etc.
- *Template System*: Implementing structure reuse through `#:template`

`Mark:down` is developed using `C# AOT` and provides a `Visual Studio Code` extension.

> `Mark:down` is open-sourced on [GitHub](https://github.com/Water-Run/MarkColonDown), where you can read the [complete documentation](https://github.com/Water-Run/MarkColonDown/tree/main/Documents/CompiledDoucuments)

## Quick Overview

A typical directory structure for a `Mark:down` project should look like:

```plaintext
│  Compile.md # Compilation entry point, the compiler will enter this file first to load corresponding compilation directives
│  Log.md # Log
│  Global.md # Stores global variables, templates, etc., automatically imported into every compiled file under default configuration
│
├─Compiled # Compiled results are stored in this directory
└─Source # "Source code"
```

The compilation process is illustrated in the following diagram:

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

| Command   | Optional Parameters                                                                                                          | Description                                                                                                                                                                                                                                                                                                             |
|-----------|------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init`    | `--entry <Path>` `--set <Name[=Value]>` *(repeatable)* `--without <Name>` *(repeatable)*                                     | Initialize (default in running directory, modifiable via `entry`), and write compilation directives specified by `--set` into the `#:compile` configuration area; `--without` removes/excludes directive items from the entry configuration area                                                                        |
| `compile` | `--use <Config>` `--overwrite <Name[=Value]>` *(repeatable)* `--ignore <Name>` *(repeatable)* `--flag <Name>` *(repeatable)* | Execute compilation (default uses `Compile.md` as configuration, modifiable via `--use`); `--overwrite` overwrites/sets directive items in the entry configuration area for this compilation; `--ignore` temporarily disables directive items in the entry configuration area for this compilation; `--flag` adds flags |

*Compilation Directives:*

| Directive Name       | Parameters                                         | Default Value                                | Description                                                                                                                                   |
|----------------------|----------------------------------------------------|----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `Max_Compile_Time`   | Non-negative integer (ms)                          | Not set (timeout not enabled)                | Compilation time limit (milliseconds); timeout not enabled if not set                                                                         |
| `Max_Output_Bytes`   | Non-negative integer                               | Not set (no limit)                           | Maximum total output size (bytes); no limit if not set                                                                                        |
| `Max_Output_Files`   | Non-negative integer                               | Not set (no limit)                           | Maximum total number of output files; no limit if not set                                                                                     |
| `Max_Include_Depth`  | Non-negative integer                               | Not set (no limit)                           | Include recursion depth limit                                                                                                                 |
| `Max_Template_Depth` | Non-negative integer                               | Not set (no limit)                           | Template/use expansion depth limit                                                                                                            |
| `Disable_Code`       | None                                               | Not set (no limit)                           | Disable code embedding, will error when embedding occurs                                                                                      |
| `Ignore_Code`        | None                                               | Not set (no limit)                           | Ignore code embedding, no error when it occurs                                                                                                |
| `Disable_Require`    | None                                               | Not set (no limit)                           | Disable `require(...)` statements in code, will error when it occurs                                                                          |
| `Require_Version`    | Version expression (supports comparison operators) | `Mark:down` version that executed `mcd init` | Require compiler version to meet condition (e.g., `>=1.2.0`)                                                                                  |
| `Include_Base`       | Path                                               | `./Source`                                   | Base path for include relative path resolution                                                                                                |
| `Input_Path`         | Path                                               | `./Source`                                   | Compilation input path                                                                                                                        |
| `Output_Path`        | Path                                               | `./Compiled`                                 | Compilation output path                                                                                                                       |
| `Input_Glob`         | Path wildcard                                      | `**/*.md`                                    | File wildcard for files to be treated as `Mark:down`                                                                                          |
| `Raw_Glob`           | Path wildcard                                      | (empty)                                      | `Mark:down` cares but doesn't process: matching files are copied as-is to output directory (only effective when copy strategy is implemented) |
| `Ignore_Glob`        | Path wildcard                                      | `.mcdignore` `.mcdcopy`                      | `Mark:down` doesn't care and doesn't process: matching files don't enter output                                                               |
| `Log_Path`           | Path                                               | `Log.md`                                     | Log output path                                                                                                                               |
| `Global_Include`     | Path wildcard                                      | `./Global.md`                                | Automatically globally imported files (implicit `#include` at file beginning)                                                                 |

## Syntax

You can get a quick overview of the extended syntax capabilities provided by `Mark:down` from this reference table:

| Syntax Structure     | Simplified Equivalent | Description                                                                                                                                                                               |
|----------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `#::`                | None                  | Explicitly declares this is a Mark:down file (no functionality); also commonly used as a "comment line" (won't enter compiled Markdown).                                                  |
| `#:1`~`#:6`          | None                  | Level x heading syntactic sugar; compiles to corresponding Markdown heading (`#`~`######`).                                                                                               |
| `#:image`            | `#:!`                 | Image line; parameter is image path, optional "(caption)"; compiles to Markdown image syntax.                                                                                             |
| `#:link`             | `#:&`                 | Link line; parameter is URL, optional "(display text)"; compiles to Markdown link syntax.                                                                                                 |
| `#:table`            | `#:-`                 | Table block start; ends at `#:=`; uses CSV syntax within block (comma-separated cells, supports quote escaping).                                                                          |
| `#:ignore`           | `#:*`                 | Skip entire file during compilation (file produces no output). Can be viewed as syntactic sugar for `#:if false`.                                                                         |
| `#:skip`             | `#:~`                 | Skip content between `skip` and `end` (or `=`), doesn't enter final Markdown. Can be viewed as syntactic sugar for `#:if false`.                                                          |
| `#:copy`             | `#:/`                 | Copy entire file during compilation. Can be viewed as syntactic sugar for `#:raw`.                                                                                                        |
| `#:compile`          | `#:;`                 | Compilation directive. Can only be placed in entry file.                                                                                                                                  |
| `#:echo`             | `#:>`                 | Print information during compilation phase (debugging/logging purposes), doesn't affect final output content.                                                                             |
| `#:end`              | `#:=`                 | Universal terminator; ends blocks like `skip/raw/code/if/while/for/template/table`, etc.                                                                                                  |
| `#:include`          | `#:$`                 | Import and directly merge another file (similar to preprocessing include).                                                                                                                |
| `#:define`           | `#:%`                 | Macro replacement: replace matched text with target text during compilation (for simple "global replacement/alias").                                                                      |
| `#:raw`              | `#:^`                 | Raw output mode: doesn't parse Mark:down directives between `raw` and `end` (or `=`), enters output as-is.                                                                                |
| `#:code`             | `#:?`                 | Execute neolua code; supports single-line or code block form; code itself doesn't enter compilation output, but can set variables/environment for subsequent `{{}}` and control flow use. |
| `#:if`               | None                  | Conditional branch start; followed by expression; used with `elif/else/end` (or `=`).                                                                                                     |
| `#:elif`             | None                  | "Else if" in conditional branch.                                                                                                                                                          |
| `#:else`             | None                  | "Else" in conditional branch.                                                                                                                                                             |
| `#:while`            | None                  | While loop; followed by conditional expression; ends with `end` (or `=`).                                                                                                                 |
| `#:for`              | None                  | For loop; follows Lua syntax (e.g., `pairs/ipairs`); ends with `end` (or `=`).                                                                                                            |
| `#:template`         | `#:+`                 | Declare template: `TemplateName: param1, param2...`; reuse structure within block through parameter names.                                                                                |
| `#:use`              | `#:@`                 | Invoke template: `TemplateName: arg1, arg2...`, expand by parameter order to generate output.                                                                                             |
| `{{ ... }}`          | None                  | Embedded output: insert expression result into text; `r{{}}` disables interpolation, preserves literal content.                                                                           |
| ` r`` ` and ` r``` ` | None                  | Raw code block (no replacement).                                                                                                                                                          |

> After the line directive `#:`, you can add a `<>` to indicate that the statement is recognized when the corresponding flag is satisfied (otherwise the statement is treated as non-existent). For example, `#:<flag1>if`
>> Within `<>`, there can be one or more flags: `&` means AND, `|` means OR, `!` means NOT, `()` indicates precedence. For example, `#:<flag1&(flag2|!flag3)>else`

*Example:*

```markdown
#:: `#::` explicitly declares this is a Mark:down file, you can also use it as a comment
#:: Note that `#:` is immediately followed by the corresponding directive, don't include spaces

#:: Level x heading syntactic sugar
#:1
#:2
#:3
#:4
#:5
#:6

#:: Image line, two equivalent ways of writing
#:image ./MyImage.png
#:! ./MyImage.png(With caption description, otherwise no caption)

#:: Link line
#:link http://mylink.com(Display as content in parentheses, otherwise display text matches link text)
#:& http://mylink.com

#:: Link line prefix
#:&- https://github.com/Water-Run/MarkColonDown(Mark:down)
#:&GitHub: https://github.com/Water-Run/MarkColonDown(Mark:down)

#:: A two-column, three-row table, you can also use the full form `#:table`
#:-
row1, row2
1, 2
3, 4
#:=

#:: ignore will skip the entire file during compilation
#:ignore

#:: skip will skip the corresponding section during compilation
#:skip

#:: echo will print the corresponding information during compilation
#:echo Compiled to here
#:: Simplified form of echo with flag, only displays when the corresponding flag is marked during compilation
#:<isflagged>> And flag is marked

This part of the content will be skipped and won't appear in the final compilation result

#:: Universal terminator symbol, including `#:if`, `#:for`, `#:code`, etc. all use this symbol. Can also be written in simplified form
#:end
#:=

#:: Directly merge another file
#:include AnotherDocument.md

#:: Replacement
#:define True False

True will be replaced with False during compilation // After compilation: False will be replaced with True

#:: Preserve native content, skip syntax provided by Mark:down
#:raw

This True will still be True after compilation

#:=

#:: code executes code. If code is followed by non-empty content, it's a single line of code; if code is followed by empty content, the content in between is treated as a code block
#:: Code executed in code won't be output to the compiled Markdown
#:code version = "1.0" -- neolua syntax
#:code
require("../global.lua") -- Can import other lua files

print("Mark:down doesn't guarantee code invocation security, doesn't run in a sandbox, while flexible and powerful you need to be responsible for code security yourself")

version = global.version
count = 0
#:=

#:: {{}} represents an embedded block, will embed the result of the corresponding expression. Use r{{}} to avoid embedding
The version of the document is {{ version }}
While this r{{ version }} will remain exactly the same in the compiled text

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
Loop iteration {{ count }}
#:code count += 1

#:- Keyword, Description
#:: for loop, follows lua syntax, can use pairs or ipairs
#:: Print list of Mark:down keywords and descriptions
#:-
Keyword, Description
#:for keyword, info in pairs(global.mark_colon_down_keyword)
{{ keyword }}, {{ info }}
#:end
#:end

#:: Template system, used for structure reuse
#:: Declare template name (PascalCase): parameter name (camelCase), equivalent to define replacement
#:template ProgramInfo: name, author, version
Software Name: name
Author: author
Version: version
#:=

#:: Invoke the template
#:use ProgramInfo: Quick Example, WaterRun, 1.0

#:: We more commonly place invoked templates in a separate common .md file, then include it for access
```
