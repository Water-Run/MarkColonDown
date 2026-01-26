# `Mark:down`

***[中文](./README-zh.md)***

![Logo](./Assets/Logo.png)

`Mark:down` is a powerful Markdown preprocessor that serves as a strict superset of Markdown, compiling to Markdown. With "line directives" starting with `#:` as its distinctive syntax, it provides the following capabilities for Markdown writing:

* *Syntactic Sugar*: such as `#:4` (level 4 heading), `#:!`/`#:image` (image line), `#:-`/`#:table` (table block, CSV syntax), etc.
* *Preprocessing Capabilities*: such as `#:include` for file imports (implementing header-file-like functionality, or global variables placed in code blocks), `#:define` for macro definitions, etc.
* *Control Flow*: including `#:if`, `#:else`, `#:while`, `#:for`, etc.
* *Embedded Code*: embedding [MiniScript](https://github.com/JoeStrout/miniscript/tree/master/MiniScript-cs), greatly extending possibilities. Includes `#:code` for executing code blocks, `{{}}` for embedding output in text, etc.
* *Template System*: implementing reuse of identical structures through `#:template`

`Mark:down` is developed using `C# AOT` and provides a `Visual Studio Code` extension.

> `Mark:down` is open source on [GitHub](https://github.com/Water-Run/MarkColonDown), where you can read the [complete documentation](https://github.com/Water-Run/MarkColonDown)

## Quick Overview

A typical directory structure for a `Mark:down` project should look like:

```plaintext
│  Compile.mcd # Compilation entry point, the compiler will first enter this file and load the corresponding compilation directives
│  Log.mcd # Log
│  Global.mcd # Stores global variables, templates, etc., automatically imported into every compiled file under default configuration
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

## Capabilities

The extended syntax of `Mark:down` can be overviewed as follows:

- `#::` : Explicitly declare a `Mark:down` file (often used as a comment)
- `#:1`~`#:6` : Level x heading syntactic sugar
- `#:image` / `#:!` : Image line syntactic sugar
- `#:link` / `#:&` : Link line syntactic sugar
- `#:table` / `#:-` : Table block syntactic sugar
- `#:ignore` / `#:*` : Skip the entire file
- `#:skip` / `#:~` : Skip portions of content
- `#:copy` / `#:/` : Copy the entire file
- `#:compile` / `#:;` : Compilation directive
- `#:echo` / `#:>` : Print information during compilation phase
- `#:end` / `#:=` : Universal terminator
- `#:include` / `#:$` : Import and merge another file
- `#:define` / `#:%` : Macro replacement
- `#:raw` / `#:^` : Output as-is
- `#:code` / `#:?` : Execute MiniScript code
- `#:if` : Conditional branch start
- `#:elif` : "else if" for conditional branch
- `#:else` : "else" for conditional branch
- `#:while` : while loop
- `#:for` : for loop
- `#:template` / `#:+` : Declare template
- `#:use` / `#:@` : Call template
- `{{ ... }}` : Embedded expression output
- ` r`` ` and ` r``` ` : Raw code block

*Usage Examples:*

```markdown
#:: `#::` explicitly declares this as a Mark:down file, you can also use it as a comment
#:: Note that `#:` is immediately followed by the corresponding directive, with no space

#:: Level x heading syntactic sugar
#:1
#:2
#:3
#:4
#:5
#:6

#:: Image line, both forms are equivalent
#:image ./MyImage.png
#:! ./MyImage.png(with caption annotation, otherwise no caption)

#:: Link line
#:link http://mylink.com(displayed as content in parentheses, otherwise displays text and link text identically)
#:& http://mylink.com

#:: Link line prefix
#:&- https://github.com/Water-Run/MarkColonDown(Mark:down)
#:&GitHub: https://github.com/Water-Run/MarkColonDown(Mark:down)

#:: A two-column, three-row table, you can also use the full name `#:table`
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
#:: Simplified form of echo with flag, only displayed when compiling with the corresponding flag marked
#:<isflagged>> and the flag is marked

This section of content will be skipped and will not appear in the final compiled result

#:: Universal termination symbol, used by `#:if`, `#:for`, `#:code`, etc. Can also be written in simplified form
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

#:: code executes code. If non-empty after code, it's a single line of code; if empty after code, the middle section is treated as a code block
#:: Code executed in code will not be output to the compiled Markdown
#:code version = "1.0" // MiniScript syntax

#:code
import "global" // Import global.ms (the specific lookup rules for import are determined by the runtime environment)

print "Mark:down does not guarantee the safety of called code, does not run in a sandbox, and while flexible and powerful, you are responsible for the safety of the code yourself"

version = global.version
count = 0
#:=

#:: {{}} represents an embedded block, will embed the result of the corresponding expression. Use r{{}} to avoid embedding
The version of the document is {{ version }}
And this r{{ version }} will have exactly identical text after compilation

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
Loop number {{ count }}
#:code count += 1
#:end

#:- Keyword, Description
#:: for loop, following MiniScript's for-in style
#:: Print the keyword and description list of Mark:down
#:-
Keyword, Description
#:for kv in global.mark_colon_down_keyword
{{ kv.key }}, {{ kv.value }}
#:end
#:end

#:: Template system, used for structural reuse
#:: Declare template name (PascalCase): parameter name (camelCase), equivalent to define replacement
#:template ProgramInfo: name, author, version
Software Name: name
Author: author
Version: version
#:=

#:: Call this template
#:use ProgramInfo: Quick Example, WaterRun, 1.0

#:: We more commonly place the called template in a separate shared .md file, then include it for access
```
