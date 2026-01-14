# `Mark:down`

***[中文](./README-zh.md)***

![Logo](./Assets/Logo.png)

## Overview

`Mark:down` is a Markdown template engine. As a strict superset of Markdown that compiles to Markdown, it provides the following features for Markdown authoring:

- Syntactic sugar: such as `#:4` (level 4 heading), `#:!`/`#:image` (image line), `#:row` and `#:column` (tables), etc.
- Preprocessing: such as `#:include` for file imports, `#:define` for macro definitions, etc.
- Control flow: including `#:if`, `#:else`, `#:while`, `#:for`, etc.
- Embedded code: embeds [neolua](https://github.com/neolithos/neolua), greatly expanding possibilities. Includes `#:code` for executing code blocks, `{{}}` for inline output in text, etc.
- Template system: implements structure reuse through `#:template`

`Mark:down`'s signature syntax consists of "line directives" starting with `#:` and `{{}}` for inline output.

`Mark:down` is developed using `C# AOT` and provides a `Visual Studio Code` extension.

> `Mark:down` is open source on [GitHub](https://github.com/Water-Run/MarkColonDown), where you can read the [complete documentation](https://github.com/Water-Run/MarkColonDown/tree/main/Documents/CompiledDoucuments)

## Quick Start

`mcd` is the compiler provided by `Mark:down`.

After installation, use:

```bash
mcd init
```

to initialize. This will generate `__mcd__.md` (the entry file) and its corresponding log `__mcd__.log` in the directory.

Use:

```bash
mcd compile
```

to compile.

Compiler command reference:

| Command   | Optional Parameters                                                                   | Description                                                                                                                                                                    |
| --------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `init`    | `--entry <path>` `--set <Name[=Value]>` *(repeatable)* `--without <Name>` *(repeatable)* | Generate/update entry file (default `./__mcd__.md`), and write `--set` specified compile directives into the `#:compile` config section; `--without` removes/doesn't write specified directive items from entry config |
| `compile` | `--entry <path>` `--overwrite <Name[=Value]>` *(repeatable)* `--ignore <Name>` *(repeatable)* | Compile entry file (default `./__mcd__.md`); `--overwrite` overrides/sets directive items in entry config for this compilation; `--ignore` temporarily disables directive items in entry config for this compilation |
| `clean`   | `--entry <path>`                                                                      | Clean build artifacts: removes output files and logs derived from entry file configuration (plus implementation-defined temporary files)                                       |

Quick syntax reference:

| Syntax Structure | Simplified Equivalent | Description                                                                                                                      |
| ---------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `#::`            | None                  | Explicitly declares this is a Mark:down file (no functionality); also commonly used as a "comment line" (not included in compiled Markdown) |
| `#:1`~`#:6`      | None                  | Level x heading syntactic sugar; compiles to corresponding Markdown headings (`#`~`######`)                                      |
| `#:image`        | `#:!`                 | Image line; parameter is image path, optional "(caption)"; compiles to Markdown image syntax                                     |
| `#:link`         | `#:&`                 | Link line; parameter is URL, optional "(display text)"; compiles to Markdown link syntax                                         |
| `#:row`          | `#:-`                 | Table row (commonly used as first/header row); comma-separated cells                                                             |
| `#:column`       | `#:\|`                | Table row (commonly used for subsequent rows); comma-separated cells                                                             |
| `#:ignore`       | `#:*`                 | Skip entire file during compilation (file produces no output)                                                                    |
| `#:skip`         | `#:~`                 | Skip content between `skip` and `end` (or `=`), not included in final Markdown                                                   |
| `#:compile`      | `#:;`                 | Compile directive. Can only be placed in entry file                                                                              |
| `#:echo`         | `#:>`                 | Print information during compilation (for debugging/logging), doesn't affect final output                                        |
| `#:end`          | `#:=`                 | Universal terminator; ends blocks like `skip/raw/code/if/while/for/template`                                                     |
| `#:include`      | `#:$`                 | Import and directly merge another file (similar to preprocessor include)                                                         |
| `#:define`       | `#:%`                 | Macro replacement: replaces matched text with target text during compilation (for simple "global replacement/alias")             |
| `#:raw`          | `#:^`                 | Raw output mode: content between `raw` and `end` (or `=`) doesn't parse Mark:down directives, enters output as-is              |
| `#:code`         | `#:?`                 | Execute neolua code; supports single line or code block form; code itself not included in compilation output, but can set variables/environment for subsequent `{{}}` and control flow |
| `#:if`           | None                  | Conditional branch start; followed by expression; used with `elif/else/end` (or `=`)                                             |
| `#:elif`         | None                  | "Else if" for conditional branch                                                                                                 |
| `#:else`         | None                  | "Else" for conditional branch                                                                                                    |
| `#:while`        | None                  | while loop; followed by conditional expression; ends with `end` (or `=`)                                                         |
| `#:for`          | None                  | for loop; follows Lua syntax (e.g., `pairs/ipairs`); ends with `end` (or `=`)                                                    |
| `#:template`     | `#:+`                 | Declare template: `TemplateName: param1, param2...`; reuse structure through parameter names within block                        |
| `#:use`          | `#:@`                 | Call template: `TemplateName: arg1, arg2...`, expands and generates output by replacing parameters in order                      |
| `{{ ... }}`      | None                  | Inline output: inserts expression result into text; `r{{}}` disables interpolation, preserving literal content                   |

See example:

```markdown
#:: `#::` explicitly declares this is a Mark:down file, you can also use it as a comment
#:: Note `#:` is immediately followed by the corresponding directive, with no space

#:: Level x heading syntactic sugar
#:1
#:2
#:3
#:4
#:5
#:6

#:: Image line, two equivalent ways to write
#:image ./MyImage.png
#:! ./MyImage.png (with caption note, otherwise no caption)

#:: Link line
#:link http://mylink.com (displays as content in parentheses, otherwise display text matches link text)
#:& http://mylink.com

#:: A table with 2 columns and 3 rows, you can also use full names `#:row` and `#:column`
#:- row1, row2
#:| 1, 2
#:| 3, 4

#:: ignore will skip the entire file during compilation
#:ignore

#:: skip will skip the corresponding part during compilation
#:skip

#:: echo will print corresponding information during compilation
#:echo Compiling to here

This content will be skipped, not appearing in final compilation result

#:: Universal terminator symbol, used by `#:if`, `#:for`, `#:code` etc. Can also be written in simplified form
#:end
#:=

#:: Directly merge another file
#:include AnotherDocument.md

#:: Replacement
#:define True False

True will be replaced with False during compilation // After compilation: False will be replaced with True

#:: Preserve raw content, skip syntax provided by Mark:down
#:raw

This True will still be True after compilation

#:=

#:: code executes code. If non-empty after code, it's a single line; if empty after code, content in between is treated as code block
#:: Code executed in code won't output to compiled Markdown
#:code version = "1.0" -- neolua syntax
#:code
require("../global.lua") -- can import other lua files

print("Mark:down doesn't guarantee code safety, doesn't run in sandbox, flexible and powerful but you're responsible for code security")

version = global.version
count = 0
#:=

#:: {{}} represents inline block, will embed the result of corresponding expression. Use r{{}} to avoid embedding
The document version is {{ version }}
And this r{{ version }} will preserve exactly the same text after compilation

#:: Selection control flow, followed by an expression
#:if version == "1.0"
Version is 1.0
#:elif version == "2.0"
Version is 2.0
#:else
Version is other version
#:=

#:: while loop, also followed by expression
#:while count < 10
Loop number {{ count }}
#:code count += 1

#:- Keyword, Description
#:: for loop, follows lua syntax, can use pairs or ipairs
#:: Print Mark:down's keyword and description list
#:for keyword, info in pairs(global.mark_colon_down_keyword)
#:| keyword, info
#:=

#:: Template system for structure reuse
#:: Declare template name (PascalCase): parameter names (camelCase), equivalent to define replacement
#:template ProgramInfo: name, author, version
Software name: name
Author: author
Version: version
#:=

#:: Call this template
#:use ProgramInfo: Quick Example, WaterRun, 1.0

#:: We more commonly place called templates in a separate common .md file, then include it for access
```

Compile directives:

| Directive Name               | Parameter                      | Description                                                                   |
| ---------------------------- | ------------------------------ | ----------------------------------------------------------------------------- |
| `Max_Compile_Time`           | Non-negative integer (ms)      | Compilation timeout (milliseconds); timeout not enabled if not set            |
| `Max_Output_Bytes`           | Non-negative integer           | Maximum total output size (bytes); unlimited if not set                       |
| `Max_Include_Depth`          | Non-negative integer           | include recursion depth limit                                                 |
| `Max_Template_Depth`         | Non-negative integer           | template/use expansion depth limit                                            |
| `Max_Loop_Iterations`        | Non-negative integer           | `for/while` total iteration count limit (prevent infinite loops)              |
| `Disable_Code`               | None                           | Disable code embedding                                                        |
| `Ignore_Code`                | None                           | Ignore code embedding (don't execute `#:code`)                                |
| `Disable_Require`            | None                           | Disable `require(...)` in code                                                |
| `Require_Version`            | Version expression (supports comparison operators) | Require compiler version to meet condition (e.g., `>=1.2.0`)    |
| `Include_Base`               | Path                           | Base path for resolving include relative paths                                |
| `Allow_Include_Outside_Base` | `On/Off`                       | Whether to allow include to jump out of `Include_Base`                        |
| `Output_Path`                | Path                           | Compilation result output path                                                |
| `Input_Glob`                 | Path wildcard                  | File wildcard to be treated as Mark:down (usually no need to set when entry-driven) |
| `Copy_Glob`                  | Path wildcard                  | Mark:down cares but doesn't process: matched files copied as-is to output directory (only effective when implementing copy strategy) |
| `Ignore_Glob`                | Path wildcard                  | Mark:down doesn't care and doesn't process: matched files not included in output |
| `Log_Path`                   | Path                           | Log output path                                                               |
| `Overwrite_Output`           | `On/Off`                       | Whether to overwrite when output file already exists                          |

Default entry `__MCD__.md` contains the following parameters:

```markdown
#:compile Max_Compile_Time 100000
#:compile Max_Output_Bytes 10485760
#:compile Max_Include_Depth 32
#:compile Max_Template_Depth 64
#:compile Max_Loop_Iterations 200000

#:compile Require_Version >=(initialized Mark:down version)

#:: include base (relative paths are resolved from this base)
#:compile Include_Base .
#:compile Allow_Include_Outside_Base Off

#:: output & log
#:compile Output_Path ../__MCD__.compiled.md
#:compile Log_Path ./__mcd__.log
#:compile Overwrite_Output On

#:: ignore common IDE/build artifacts (glob)
#:: separator recommendation: use ';' between patterns (implementation-defined)
#:compile Ignore_Glob ".git/**;.idea/**;.vscode/**;.vs/**;target/**;node_modules/**;dist/**;build/**;out/**;bin/**;obj/**;__pycache__/**;*.tmp;*.log"
```