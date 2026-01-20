# `Mark:down`

***[English](./README.md)***  

![Logo](./Assets/Logo.png)

## Overview

`Mark:down` is a powerful Markdown template engine. As a strict superset of Markdown that compiles to Markdown, it provides the following features for Markdown authoring:

- Syntactic sugar: such as `#:4` (level 4 heading), `#:!`/`#:image` (image line), `#:row` and `#:column` (tables), etc.
- Preprocessing: such as `#:include` for file imports, `#:define` for macro definitions, etc.
- Control flow: including `#:if`, `#:else`, `#:while`, `#:for`, etc.
- Embedded code: embedded [neolua](https://github.com/neolithos/neolua) for greatly extended possibilities. Including `#:code` for executing code blocks, `{{}}` for inline output in text, etc.
- Template system: reusing identical structures through `#:template`

`Mark:down`'s signature syntax consists of "line directives" beginning with `#:` and inline output with `{{}}`.

`Mark:down` is developed using `C# AOT` and provides a `Visual Studio Code` extension.

> `Mark:down` is open source on [GitHub](https://github.com/Water-Run/MarkColonDown), where you can read the [complete documentation](https://github.com/Water-Run/MarkColonDown/tree/main/Documents/CompiledDoucuments)

## Quick Overview

A typical `Mark:down` project directory should look like:

```plaintext
│  Compile.md # Compilation entry point, the compiler will first enter this file and load corresponding compilation directives
│  Log.md # Log
│  Global.md # Stores global variables, templates, etc., automatically imported into every compiled file under default configuration
│
├─Compiled # Compiled results are stored in this directory
└─Source # "Source code"
```

![Compilation Flow Diagram](./Assets/CompileFlow.png)

## Compiler

`mcd` is the compiler provided by `Mark:down`.

After installation, use:

```bash
mcd init
```

to initialize. This will generate `Compile.md` and the corresponding log `Log.md` in the directory.

Use:

```bash
mcd compile
```

to compile and output to the output directory.

Compiler command reference:

| Command   | Optional Parameters                                                                                                          | Description                                                                                                                                                                                                                                                                                                                                                            |
|-----------|------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init`    | `--entry <Path>` `--set <Name[=Value]>` *(repeatable)* `--without <Name>` *(repeatable)*                                     | Initialize (default in the working directory, can be modified via `entry`), and write compilation directives specified by `--set` into the `#:compile` configuration area; `--without` is used to remove/not write a directive item from the entry configuration area                                                                                                  |
| `compile` | `--use <Config>` `--overwrite <Name[=Value]>` *(repeatable)* `--ignore <Name>` *(repeatable)* `--flag <Name>` *(repeatable)* | Execute compilation (default uses `Compile.md` as configuration, can be modified using `--use`); `--overwrite` overwrites/sets directive items in the entry configuration area for this compilation; `--ignore` temporarily disables directive items in the entry configuration area for this compilation; `--flag` adds flags (corresponding to compilation behavior) |

*Compilation directives:*

| Directive Name       | Parameter                                          | Default Value                                    | Description                                                                                                                                   |
|----------------------|----------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `Max_Compile_Time`   | Non-negative integer (ms)                          | Not set (timeout not enabled)                    | Compilation time limit (milliseconds); if not set, timeout is not enabled                                                                     |
| `Max_Output_Bytes`   | Non-negative integer                               | Not set (no limit)                               | Maximum total output size (bytes); if not set, no limit                                                                                       |
| `Max_Output_Files`   | Non-negative integer                               | Not set (no limit)                               | Maximum total output file count; if not set, no limit                                                                                         |
| `Max_Include_Depth`  | Non-negative integer                               | Not set (no limit)                               | include recursion depth limit                                                                                                                 |
| `Max_Template_Depth` | Non-negative integer                               | Not set (no limit)                               | template/use expansion depth limit                                                                                                            |
| `Disable_Code`       | None                                               | Not set (no limit)                               | Disable code embedding, will report error when embedding occurs                                                                               |
| `Ignore_Code`        | None                                               | Not set (no limit)                               | Ignore code embedding, no error when it occurs                                                                                                |
| `Disable_Require`    | None                                               | Not set (no limit)                               | Disable `require(...)` statements in code, will report error when it occurs                                                                   |
| `Require_Version`    | Version expression (supports comparison operators) | The `Mark:down` version that executed `mcd init` | Require compiler version to meet conditions (e.g., `>=1.2.0`)                                                                                 |
| `Include_Base`       | Path                                               | `./Source`                                       | Base path for include relative path resolution                                                                                                |
| `Input_Path`         | Path                                               | `./Source`                                       | Compilation input path                                                                                                                        |
| `Output_Path`        | Path                                               | `./Compiled`                                     | Compilation output path                                                                                                                       |
| `Input_Glob`         | Path wildcard                                      | `**/*.md`                                        | File wildcard for files to be treated as `Mark:down`                                                                                          |
| `Raw_Glob`           | Path wildcard                                      | (Empty)                                          | `Mark:down` cares but doesn't process: matching files are copied as-is to output directory (only effective when copy strategy is implemented) |
| `Ignore_Glob`        | Path wildcard                                      | `.mcdignore` `.mcdcopy`                          | `Mark:down` doesn't care and doesn't process: matching files don't enter output                                                               |
| `Log_Path`           | Path                                               | `Log.md`                                         | Log output path                                                                                                                               |
| `Overwrite_Output`   | `On/Off`                                           | `On`                                             | Whether to overwrite when output file already exists                                                                                          |
| `GlobalInclude`      | Path wildcard                                      | `./Global.md`                                    | Automatically globally imported files (implicit `#include` at file beginning)                                                                 |

## Syntax

You can get a quick overview of `Mark:down`'s extended syntax capabilities from this reference table:

| Syntax Structure     | Simplified Equivalent | Description                                                                                                                                                                                 |
|----------------------|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `#::`                | None                  | Explicitly declares this is a Mark:down file (no functionality); also commonly used as a "comment line" (won't enter compiled Markdown).                                                    |
| `#:1`~`#:6`          | None                  | x-level heading syntactic sugar; compiles to corresponding Markdown heading (`#`~`######`).                                                                                                 |
| `#:image`            | `#:!`                 | Image line; parameter is image path, optional "(caption)"; compiles to Markdown image syntax.                                                                                               |
| `#:link`             | `#:&`                 | Link line; parameter is URL, optional "(display text)"; compiles to Markdown link syntax.                                                                                                   |
| `#:row`              | `#:-`                 | Table row (commonly used as first row/header row); comma-separated cells.                                                                                                                   |
| `#:column`           | `#:\|`                | Table row (commonly used as subsequent rows); comma-separated cells.                                                                                                                        |
| `#:ignore`           | `#:*`                 | Skip entire file during compilation (the file produces no output). Can be viewed as syntactic sugar for `#:if false`.                                                                       |
| `#:skip`             | `#:~`                 | Skip content between `skip` and `end` (or `=`), doesn't enter final Markdown. Can be viewed as syntactic sugar for `#:if false`.                                                            |
| `#:copy`             | `#:/`                 | Copy entire file during compilation. Can be viewed as syntactic sugar for `#:raw`.                                                                                                          |
| `#:compile`          | `#:;`                 | Compilation directive. Can only be placed in entry file.                                                                                                                                    |
| `#:echo`             | `#:>`                 | Print information during compilation phase (for debugging/logging purposes), doesn't affect final output content.                                                                           |
| `#:end`              | `#:=`                 | Universal terminator; ends `skip/raw/code/if/while/for/template` etc. blocks.                                                                                                               |
| `#:include`          | `#:$`                 | Import and directly merge another file (similar to preprocessor include).                                                                                                                   |
| `#:define`           | `#:%`                 | Macro replacement: replaces matched text with target text during compilation (for simple "global replacement/aliasing").                                                                    |
| `#:raw`              | `#:^`                 | Raw output mode: content between `raw` and `end` (or `=`) doesn't parse Mark:down directives, enters output as-is.                                                                          |
| `#:code`             | `#:?`                 | Execute neolua code; supports single-line or code block form; code itself doesn't enter compilation output, but can set variables/environment for subsequent `{{}}` and control flow usage. |
| `#:if`               | None                  | Conditional branch start; followed by expression; used with `elif/else/end` (or `=`).                                                                                                       |
| `#:elif`             | None                  | "Else if" for conditional branch.                                                                                                                                                           |
| `#:else`             | None                  | "Else" for conditional branch.                                                                                                                                                              |
| `#:while`            | None                  | while loop; followed by conditional expression; ends with `end` (or `=`).                                                                                                                   |
| `#:for`              | None                  | for loop; follows Lua syntax (e.g., `pairs/ipairs`); ends with `end` (or `=`).                                                                                                              |
| `#:template`         | `#:+`                 | Declare template: `TemplateName: param1, param2...`; reuse structure within block through parameter names.                                                                                  |
| `#:use`              | `#:@`                 | Call template: `TemplateName: arg1, arg2...`, expands and generates output by replacing in parameter order.                                                                                 |
| `{{ ... }}`          | None                  | Inline output: inserts expression result into text; `r{{}}` disables interpolation, preserves literal content.                                                                              |
| ` r`` ` and ` r``` ` | None                  | Raw code blocks (no substitution).                                                                                                                                                          |

*Example:*

```markdown
#:: `#::` explicitly declares this is a Mark:down file, you can also use it as a comment
#:: Note that `#:` is immediately followed by the corresponding directive, with no spaces

#:: x-level heading syntactic sugar
#:1
#:2
#:3
#:4
#:5
#:6

#:: Image line, two equivalent ways to write
#:image ./MyImage.png
#:! ./MyImage.png (with caption description, otherwise no caption)

#:: Link line
#:link http://mylink.com (displays as content in parentheses, otherwise display text and link text are identical)
#:& http://mylink.com

#:: A two-column three-row table, you can also use the full names `#:row` and `#:column`
#:- row1, row2
#:| 1, 2
#:| 3, 4

#:: ignore will skip the entire file during compilation
#:ignore

#:: skip will skip the corresponding part during compilation
#:skip

#:: echo will print the corresponding information during compilation
#:echo Compiled to here

This part of the content will be skipped and won't appear in the final compilation result

#:: Universal terminator symbol, including `#:if`, `#:for`, `#:code` etc. all use this symbol. Can also be written in simplified form
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

#:: Code blocks can use r``` and r``, won't be escaped
Below is a piece of Vue code, including r`{{ }}`, won't be translated:

r```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Vue {{}} Simplest Example</title>
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

#:: code executes code. If code is followed by non-empty content, it's a single line of code; if code is followed by empty, then the middle part is viewed as a code block
#:: Code executed in code won't be output to the compiled Markdown
#:code version = "1.0" -- neolua syntax
#:code
require("../global.lua") -- can import other lua files

print("Mark:down does not guarantee the security of called code, doesn't run in a sandbox, while being flexible and powerful you need to be responsible for the security of the code yourself")

version = global.version
count = 0
#:=

#:: {{}} indicates an inline block, will embed the result of the corresponding expression. Use r{{}} to avoid embedding
The version of the document is {{ version }}
And this r{{ version }} compiled text will remain completely identical

#:: Selection control flow, followed by an expression
#:if version == "1.0"
Version is 1.0
#:elif version == "2.0"
Version is 2.0
#:else
Version is another version
#:=

#:: while loop, also followed by an expression
#:while count < 10
The {{ count }}th loop
#:code count += 1

#:- Keyword, Description
#:: for loop, follows lua syntax, can use pairs or ipairs
#:: Print the list of Mark:down keywords and descriptions
#:for keyword, info in pairs(global.mark_colon_down_keyword)
#:| keyword, info
#:=

#:: Template system, for reusing structures
#:: Declare template name (PascalCase): parameter name (camelCase), equivalent to define replacement
#:template ProgramInfo: name, author, version
Software name: name
Author: author
Version: version
#:=

#:: Call the template
#:use ProgramInfo: Quick Example, WaterRun, 1.0

#:: We more commonly place the called template in a separate shared .md file, then include it to access
```