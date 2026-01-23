# `Mark:down`

***[中文](./README-zh.md)***

![Logo](./Assets/Logo.png)

`Mark:down` is a powerful Markdown preprocessor. As a strict superset of Markdown, it compiles down to Markdown. Its signature syntax is a set of *line directives* that start with `#:`. These directives provide:

* *Syntactic sugar*: e.g. `#:4` (level-4 heading), `#:!`/`#:image` (image line), `#:-`/`#:table` (table block, CSV syntax), etc.
* *Preprocessing capabilities*: e.g. `#:include` for file inclusion (like header files, or global variables placed in code blocks), `#:define` for macro definitions, etc.
* *Control flow*: including `#:if`, `#:else`, `#:while`, `#:for`, etc.
* *Embedded code*: embeds [MiniScript-cs](https://github.com/JoeStrout/miniscript/tree/master/MiniScript-cs), greatly expanding what you can do. This includes `#:code` for executing code blocks and `{{}}` for inline output in text.
* *Template system*: reuse repeated structures via `#:template`.

`Mark:down` is developed in `C# AOT` and ships with a `Visual Studio Code` extension.

> `Mark:down` is open-sourced on [GitHub](https://github.com/Water-Run/MarkColonDown), where you can also read the [full documentation](https://github.com/Water-Run/MarkColonDown/tree/main/Documents/CompiledDoucuments).

## Quick Look

A typical `Mark:down` project directory looks like this:

```plaintext
│  Compile.md # Compilation entry; the compiler enters this file first and loads compilation directives
│  Log.md # Logs
│  Global.md # Stores global variables, templates, etc.; under the default configuration it is automatically imported into every compiled file
│
├─Compiled # Compilation outputs are stored here
└─Source # "Source"
````

The compilation workflow is illustrated below:

![Compilation Flow](./Assets/CompileFlow.png)

## Compiler

`mcd` is the compiler provided by `Mark:down`.

After installation, run:

```bash
mcd init
```

to initialize. This generates `Compile.md` and the corresponding log file `Log.md` in the current directory.

Run:

```bash
mcd compile
```

to compile, producing outputs in the output directory.

Compiler command reference:

| Command   | Optional Arguments                                                                                                           | Description                                                                                                                                                                                                                                                    |
|-----------|------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init`    | `--entry <Path>` `--set <Name[=Value]>` *(repeatable)* `--without <Name>` *(repeatable)*                                     | Initialize (defaults to the current directory; change via `entry`), and write directives specified by `--set` into the `#:compile` configuration block; `--without` removes/omits a directive item from the entry config block                                 |
| `compile` | `--use <Config>` `--overwrite <Name[=Value]>` *(repeatable)* `--ignore <Name>` *(repeatable)* `--flag <Name>` *(repeatable)* | Compile (uses `Compile.md` by default; override via `--use`); `--overwrite` overrides/sets directive items in the entry config block for this run; `--ignore` temporarily disables directive items in the entry config block for this run; `--flag` adds flags |

*Compilation directives:*

| Directive Name       | Arguments                                          | Default                                    | Description                                                                                                                                        |
|----------------------|----------------------------------------------------|--------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `Max_Compile_Time`   | Non-negative integer (ms)                          | Unset (timeout disabled)                   | Compilation time limit (milliseconds); unset disables timeout                                                                                      |
| `Max_Output_Bytes`   | Non-negative integer                               | Unset (no limit)                           | Maximum total output size (bytes); unset means unlimited                                                                                           |
| `Max_Output_Files`   | Non-negative integer                               | Unset (no limit)                           | Maximum number of output files; unset means unlimited                                                                                              |
| `Max_Include_Depth`  | Non-negative integer                               | Unset (no limit)                           | Maximum recursion depth for `include`                                                                                                              |
| `Max_Template_Depth` | Non-negative integer                               | Unset (no limit)                           | Maximum expansion depth for `template/use`                                                                                                         |
| `Disable_Code`       | None                                               | Unset (not enabled)                        | Disable embedded code; compilation errors if embedded code is encountered                                                                          |
| `Ignore_Code`        | None                                               | Unset (not enabled)                        | Ignore embedded code; no error if encountered                                                                                                      |
| `Disable_Import`     | None                                               | Unset (not enabled)                        | Disable `import` calls inside code; compilation errors if encountered                                                                              |
| `Require_Version`    | Version expression (supports comparison operators) | The `Mark:down` version used by `mcd init` | Require the compiler version to satisfy a constraint (e.g. `>=1.2.0`)                                                                              |
| `Include_Base`       | Path                                               | `./Source`                                 | Base path for resolving relative paths in `include`                                                                                                |
| `Input_Path`         | Path                                               | `./Source`                                 | Compilation input path                                                                                                                             |
| `Output_Path`        | Path                                               | `./Compiled`                               | Compilation output path                                                                                                                            |
| `Input_Glob`         | Glob pattern                                       | `**/*.md`                                  | Glob for files to be treated as `Mark:down`                                                                                                        |
| `Raw_Glob`           | Glob pattern                                       | (empty)                                    | Files that `Mark:down` cares about but does not process: copied as-is to the output directory (only effective when a copy strategy is implemented) |
| `Ignore_Glob`        | Glob pattern                                       | `.mcdignore` `.mcdcopy`                    | Files that `Mark:down` neither cares about nor processes: excluded from compilation                                                                |
| `Log_Path`           | Path                                               | `Log.md`                                   | Log output path                                                                                                                                    |
| `Global_Include`     | Glob pattern                                       | `./Global.md`                              | Automatically globally included file(s) (an implicit `#include` at the start of each file)                                                         |

## Syntax

Use this quick reference table to overview the extended syntax features provided by `Mark:down`:

| Syntax Structure     | Equivalent Short Form | Description                                                                                                                                            |
|----------------------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `#::`                | None                  | Explicitly declares this is a Mark:down file (no functional effect); also commonly used as a “comment line” (not emitted into compiled Markdown).      |
| `#:1`~`#:6`          | None                  | Heading sugar for level x; compiles to Markdown headings (`#`~`######`).                                                                               |
| `#:image`            | `#:!`                 | Image line; parameter is an image path with optional “(caption)”; compiles to Markdown image syntax.                                                   |
| `#:link`             | `#:&`                 | Link line; parameter is a URL with optional “(display text)”; compiles to Markdown link syntax.                                                        |
| `#:table`            | `#:-`                 | Start of a table block; ends at `#:=`; uses CSV syntax inside the block (comma-separated cells, supports quoted escaping).                             |
| `#:ignore`           | `#:*`                 | Skip the entire file during compilation (this file produces no output). Can be viewed as sugar for `#:if false`.                                       |
| `#:skip`             | `#:~`                 | Skip content between `skip` and `end` (or `=`), not emitted into final Markdown. Can be viewed as sugar for `#:if false`.                              |
| `#:copy`             | `#:/`                 | Copy the entire file during compilation. Can be viewed as sugar for `#:raw`.                                                                           |
| `#:compile`          | `#:;`                 | Compilation directives. Only allowed in the entry file.                                                                                                |
| `#:echo`             | `#:>`                 | Print messages during compilation (debug/logging); does not affect final output.                                                                       |
| `#:end`              | `#:=`                 | Generic terminator; ends blocks such as `skip/raw/code/if/while/for/template/table`, etc.                                                              |
| `#:include`          | `#:$`                 | Import and directly merge another file (like a preprocessing include).                                                                                 |
| `#:define`           | `#:%`                 | Macro replacement: replace matched text with target text at compile time (simple “global replace/alias”).                                              |
| `#:raw`              | `#:^`                 | Raw output mode: between `raw` and `end` (or `=`), Mark:down directives are not parsed; content is emitted as-is.                                      |
| `#:code`             | `#:?`                 | Execute MiniScript code; supports single-line or block form; code is not emitted, but can set variables/environment for later `{{}}` and control flow. |
| `#:if`               | None                  | Start conditional branch; followed by an expression; used with `elif/else/end` (or `=`).                                                               |
| `#:elif`             | None                  | “Else if” branch.                                                                                                                                      |
| `#:else`             | None                  | “Else” branch.                                                                                                                                         |
| `#:while`            | None                  | While loop; followed by a condition expression; ends with `end` (or `=`).                                                                              |
| `#:for`              | None                  | For loop; follows MiniScript `for <var> in <sequence>` style (iterates list/string/map, etc.); ends with `end` (or `=`).                               |
| `#:template`         | `#:+`                 | Define a template: `TemplateName: param1, param2...`; reuse structure via parameter names within the block.                                            |
| `#:use`              | `#:@`                 | Use a template: `TemplateName: arg1, arg2...`; expands output by positional argument substitution.                                                     |
| `{{ ... }}`          | None                  | Inline output: inserts the expression result into text; `r{{}}` disables interpolation and preserves literal content.                                  |
| ` r`` ` and ` r``` ` | None                  | Raw code blocks (no replacement).                                                                                                                      |

> After the line directive prefix `#:`, you can add `<>` to indicate the statement is recognized only when the corresponding flag condition is satisfied (otherwise the statement is treated as non-existent). For example: `#:<flag1>if`
>
> > Inside `<>`, you can use one or more flags: `&` for AND, `|` for OR, `!` for NOT, and `()` for precedence. Example: `#:<flag1&(flag2|!flag3)>else`

*Example:*

```markdown
#:: `#::` explicitly declares this is a Mark:down file; you can also use it as comments
#:: Note: `#:` must be immediately followed by the directive; do not insert spaces

#:: Heading sugar for level x
#:1
#:2
#:3
#:4
#:5
#:6

#:: Image line, both forms are equivalent
#:image ./MyImage.png
#:! ./MyImage.png(with caption; otherwise no caption)

#:: Link line
#:link http://mylink.com(display text shown as the content in parentheses; otherwise display text equals link text)
#:& http://mylink.com

#:: Link line prefix
#:&- https://github.com/Water-Run/MarkColonDown(Mark:down)
#:&GitHub: https://github.com/Water-Run/MarkColonDown(Mark:down)

#:: A 2-column 3-row table; you can also use the full form `#:table`
#:-
row1, row2
1, 2
3, 4
#:=

#:: ignore will skip the entire file during compilation
#:ignore

#:: skip will skip the corresponding section during compilation
#:skip

#:: echo will print information during compilation
#:echo compiled up to here
#:: The short form of echo with flags; shown only when the compile flag matches
#:<isflagged>> AND the flag is set

This section will be skipped and will not appear in the final compiled output.

#:: Generic terminator symbol; blocks like `#:if`, `#:for`, `#:code`, etc. all use this. You can also use the short form.
#:end
#:=

#:: Directly merge another file
#:include AnotherDoc.md

#:: Replacement
#:define True False

True will be replaced with False during compilation // After compilation: False will be replaced with True

#:: Preserve original content and skip Mark:down directives
#:raw

This True remains True after compilation

#:=

#:: code executes code. If `code` is followed by non-empty content, it's a single line; otherwise the middle section is treated as a code block.
#:: Code executed in `code` will not be emitted into the compiled Markdown output.
#:code version = "1.0" // MiniScript syntax

#:code
import "global" // Import global.ms (the runtime determines the exact lookup rules for import)

print "Mark:down does not guarantee the safety of executing code. It does not run in a sandbox. While flexible and powerful, you are responsible for the security of the code you execute."

version = global.version
count = 0
#:=

#:: `{{}}` is inline output; it inserts the expression result. Use `r{{}}` to avoid interpolation.
The document version is {{ version }}
And this r{{ version }} will remain exactly the same after compilation

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
Loop iteration {{ count }}
#:code count += 1
#:end

#:- Keyword, Description
#:: for loop, follows MiniScript for-in style
#:: Print the list of Mark:down keywords and descriptions
#:-
Keyword, Description
#:for kv in global.mark_colon_down_keyword
{{ kv.key }}, {{ kv.value }}
#:end
#:end

#:: Template system for reusing structure
#:: Define template name (UpperCamelCase): parameter names (lowerCamelCase), effectively like define replacement
#:template ProgramInfo: name, author, version
Software: name
Author: author
Version: version
#:=

#:: Use the template
#:use ProgramInfo: Quick Example, WaterRun, 1.0

#:: More commonly, we place templates in a separate shared .md file, then include it to access them.
```

```
