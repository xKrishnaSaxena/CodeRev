# PEP 8 – Style Guide for Python Code (Clean Markdown Version)

## Introduction

This document gives coding conventions for the Python code comprising the standard library in the main Python distribution. This document and PEP 257 (Docstring Conventions) were adapted from Guido’s original Python Style Guide essay, with additions from Barry’s style guide.

This style guide evolves over time as additional conventions are identified and past conventions are rendered obsolete by changes in the language itself.

Many projects have their own coding style guidelines. In the event of conflicts, such project-specific guides take precedence for that project.

## A Foolish Consistency is the Hobgoblin of Little Minds

One of Guido’s key insights is that code is read much more often than it is written. The guidelines here are intended to improve readability and make code consistent across the wide spectrum of Python code. As PEP 20 says, “Readability counts”.

A style guide is about consistency. Consistency with this guide is important. Consistency within a project is more important. Consistency within one module or function is the most important.

However, know when to be inconsistent—sometimes recommendations just aren’t applicable. When in doubt, use your best judgment. Look at other examples and decide what looks best. And don’t hesitate to ask!

**Do not break backward compatibility just to comply with this PEP.**

Good reasons to ignore a guideline:

- Applying it would make the code less readable—even to someone used to PEP 8.
- To be consistent with surrounding code that also breaks it (perhaps for historical reasons). This can also be an opportunity to clean things up.
- The code predates the guideline and there’s no other reason to modify it.
- The code must remain compatible with older Python versions that lack the recommended feature.

## Code Layout

### Indentation

- Use **4 spaces** per indentation level.
- Continuation lines should align wrapped elements either:

  - **Vertically**, using Python’s implicit line joining inside parentheses, brackets, and braces, or
  - With a **hanging indent**. When using a hanging indent:

    - Put **no arguments** on the first line.
    - Add an extra indentation level to clearly distinguish continuation lines.

```python
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Hanging indent: no args on the first line; indent continuation lines.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)

# Optional: hanging indents may use other widths for readability.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```

#### Tabs or Spaces?

- **Spaces** are the preferred indentation method.
- Tabs should be used **only** to remain consistent with code already indented with tabs.
- **Never mix** tabs and spaces.

### Maximum Line Length

- Limit all lines to a maximum of **79 characters**.
- For flowing long blocks of text (docstrings or comments), limit to **72 characters**.

### Blank Lines

- Surround **top-level** function and class definitions with **two** blank lines.
- Method definitions inside a class are surrounded by **a single** blank line.
- Extra blank lines may be used (sparingly) to separate related groups of functions.
- Use blank lines inside functions (sparingly) to indicate logical sections.

### Source File Encoding

- Code in the core Python distribution should use **UTF-8** and **should not** include an encoding declaration.
- For other projects, if a different encoding is required, use a PEP 263 encoding declaration at the top of the file.

### Imports

- Imports should usually be on **separate lines**:

```python
# Correct:
import os
import sys

# Not recommended:
import os, sys
```

- Place imports at the **top of the file**, after any module comments and docstrings, and before module globals and constants.
- Group imports in this order, with a **blank line** between each group:

  1. Standard library imports
  2. Related third-party imports
  3. Local application/library-specific imports

- Use **absolute imports** when possible; they are usually more readable and provide better error messages if the import system is misconfigured. Explicit **relative imports** are acceptable within packages.

```python
# Absolute imports:
import mypkg.sibling
from mypkg import sibling
from mypkg.sibling import example
```

### String Quotes

- Single-quoted and double-quoted strings are the same in Python. Pick one and **be consistent**.
- When a string contains a single or double quote character, prefer the **other** quote to avoid backslashes.
- For **triple-quoted** strings, use triple **double** quotes to be consistent with PEP 257 docstring conventions.

### Whitespace in Expressions and Statements

#### Pet Peeves (avoid extraneous whitespace):

- Immediately **inside** parentheses, brackets, or braces:

  - `spam(ham[1], {eggs: 2})` ✅ not `spam( ham[1], { eggs: 2 } )` ❌

- Between a trailing comma and a closing parenthesis:

  - `func(a, )` ❌

- Immediately **before** a comma, semicolon, or colon:

  - `if x == 4: print(x, y)` ✅ not `if x == 4 : print(x , y)` ❌

- Immediately **before** the opening parenthesis of a function call:

  - `func(x)` ✅ not `func (x)` ❌

- Immediately **before** the opening bracket of an index:

  - `spam[1]` ✅ not `spam [1]` ❌

#### Around operators and commas

- Use **one space** around binary operators and after commas.

- **Never** add spaces at the beginning or end of a line to align visually with other lines.

- Always surround these binary operators with a **single space** on either side:

  - Assignment (`=`, `+=`, `-=` …)
  - Comparisons (`==`, `<`, `>`, `!=`, `<=`, `>=`, `in`, `not in`, `is`, `is not`)
  - Booleans (`and`, `or`, `not`)

## Naming Conventions

> The most important rule: **be consistent** within a project or module.

### Names to Avoid

- Never use the characters **`l`** (lowercase el), **`O`** (uppercase oh), or **`I`** (uppercase eye) as single-letter variable names.

### Package and Module Names

- Use **short, all-lowercase** names.
- Underscores may be used for modules if it improves readability.
- Packages should be short, all-lowercase; underscores are **discouraged**.

### Class Names

- Use the **CapWords** (PascalCase) convention: `MyClass`.

### Type Variable Names

- Use **CapWords** (e.g., `AnyStr`, `PathLike`), or the prevailing convention in your codebase.
- Single-letter type variables (e.g., `T`) are common and acceptable.

### Function and Variable Names

- Use **lowercase**, with words separated by **underscores** as needed: `get_user_id`.

### Function and Method Arguments

- Always use **`self`** for the first argument to instance methods.
- Always use **`cls`** for the first argument to class methods.

### Constants

- Define constants at **module level**, written in **ALL_CAPS** with underscores: `MAX_OVERFLOW`, `TOTAL`.

## Programming Recommendations

### Avoid `global` When Possible

- Do not use the `global` statement unless absolutely necessary. It obscures data flow and can make code harder to reason about.

### Function Annotations

- Use precise types when helpful:

```python
def sum_two_ints(a: int, b: int) -> int:
    return a + b
```

### Default Argument Values

- **Do not** use mutable objects (e.g., lists, dicts) as default values. Use `None` and set inside the function.

```python
def append_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

### Properties vs. Getters/Setters

- Prefer `@property` and setters over explicit `get_*/set_*` methods when appropriate.

```python
class Person:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
```

### Comparisons to Singletons

- Compare to **`None`** (and other singletons) with `is` or `is not`, **never** with `==` or `!=`.

```python
if foo is None:
    ...
```

- Don’t compare boolean values to `True` or `False` using `==`.

```python
if is_valid:         # ✅
    ...
if is_valid is True: # ❌
    ...
```

### `isinstance()` vs. `type()`

- Use `isinstance(obj, Class)` rather than `type(obj) is Class` for type checks (supports inheritance).

### Exception Handling

- Use `try/except` sparingly and **catch specific exceptions**.
- Avoid bare `except:`; use `except Exception:` only if you must catch all non-system-exit exceptions.
- Re-raise exceptions when appropriate and keep error handling narrow.

## References

- **Guido van Rossum**, _Original Python Style Guide_.
- **PEP 257**: Docstring Conventions.

---

_End of cleaned, chat-friendly Markdown version of your document._
