# dictrule

[![PyPI version](https://badge.fury.io/py/dictrule.svg)](https://badge.fury.io/py/dictrule)
[![Python package](https://github.com/elhoangvu/dictrule/actions/workflows/python-package.yml/badge.svg)](https://github.com/elhoangvu/dictrule/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/elhoangvu/dictrule/graph/badge.svg?token=CPE82M9GVB)](https://codecov.io/gh/elhoangvu/dictrule)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/elhoangvu/dictrule/blob/main/LICENSE)

`dictrule` is a simple Python module that helps generate text from defined rules in dictionary form. This module provides popular built-in rules and supports extended external rules for different usages.

With the input is `dictrule.yml` in YAML format (or `dictrule.json` in JSON format with a similar config) ...

```yaml
- '"""'
- format_uppercase: {eval: gen.header}
- '"""'
- 
- comment:
  - inline:
    - eval: gen.id
    - '. '
    - eval: gen.title
  - inline: ["Creation date: ", eval: gen.date]
  - inline: ["Author: ", eval: gen.author]
-
- indent_0: "class Sample:"
- indent_1: "def contents(self) -> List[str]:"
- indent_2: return [
- indent_3:
    for: content
    in: gen.contents
    block:
      - inline: [stringify: {eval: content.index}, ","]
      - inline: [stringify: {eval: content}, ","]
- indent_2: "]"
```

And generate with example code ...

```python
# loading dict from config file
config_file = 'dictrule.yml'
dict_config: Dict[str, Any] = load_config(config_file)

# generating string by loaded config
generator = dictrule.Generator(dict_config)
context: dictrule.Context = build_context()
generated_str = generator.generate(context)

# printing the output
print(generated_str)
```

Then output is ...

```python
"""
THIS IS THE GENERATED EXAMPLE CODE
"""

# 3101. Sampler for getting sample contents
# Creation date: 01-01-2024
# Author: Zooxy Le

class Sample:
  def contents(self) -> List[str]:
    return [
      "0",
      "Train",
      "1",
      "Flight",
      "2",
      "Ship",
    ]
```

**Explanation**

> for the methods
> 
> - `load_config`: load config from config file in `dict` format
> - `build_context`: build context for `dictrule.Generator` in `dictrule.Context`

> for the variables
> 
> - `gen.header`: "THIS IS THE GENERATED EXAMPLE CODE"
> - `gen.id`: 3101
> - `gen.title`: "Sampler for getting sample contents"
> - `gen.date`: "01-01-2024"
> - `gen.author`: "Zooxy Le"
> - `gen.contents`: ["Train", "Flight", "Ship"]

__Note:__ The value of the variables is depended to current context by `build_context` method.

Refer to my projects using `dictrule` to generate text resources:

- [leetcodegen](https://github.com/elhoangvu/leetcodegen)

## Installing dictrule

`dictrule` is available on PyPI:

```console
$ python -m pip install dictrule
```

`dictrule` officially supports Python 3.7+.

## Built-in rules

### BlockRule

This rule joins a list of rules separated by a new line.

| Key   | Required | Value type | Value description     |
| ----- |:--------:| ---------- | --------------------- |
| block | Yes      | list       | A list of other rules |

**Example**

```python
>>> dictrule.Generator({
...   "block": [
...         "rule_1",
...         "rule_2",
...         "rule_3",
...     ]
... }).generate()
rule_1
rule_2
rule_3
```

### CommentRule

This rule allows generating comment text based on single-line and multi-line rules.

| Key     | Required | Value type       | Value description                                       |
| ------- |:--------:| ---------------- | ------------------------------------------------------- |
| comment | Yes      | string/list/dict | A text or a list of other rules are commented.          |
| style   | No       | string           | Styles of comment:<br/>- `singleline`<br/>- `multiline` |

Building `Context` with `CommentRule.ContextCase` to define the comment style.

**Example**

```python
>>> context = build_singleline_context("#")
>>> dictrule.Generator({
...     "comment": "This is a single-line comment"
... }).generate(context)
# This is a single-line comment

>>> context = build_multiline_context('"""')
>>> dictrule.Generator({
...     "style": "multiline",
...     "comment": [
...         "line1": "Line 1 of multi-line comment",
...         "line2": "Line 2 of multi-line comment",
...     ]
... }).generate(context)
"""
Line 1 of multi-line comment
Line 2 of multi-line comment
"""
```

### EvalRule

This rule evaluates the value of provied variable or command.

| Key  | Required | Value type | Value description                                                     |
| ---- |:--------:| ---------- | --------------------------------------------------------------------- |
| eval | Yes      | string     | Variable name or keypath or command are provided from your generator. |

**Example**

```python
>>> git_author = "Zooxy Le"
>>> dictrule.Generator({
...     "eval": "git_author"
... }).generate()
Zooxy Le

>>> project_id = "123456789"
>>> dictrule.Generator({
...     "eval": "project_id"
... }).generate()
123456789
```

### ForInRule

This rule executes generatable rules in a `for-in-block` loop with a provided iterable variable.

| Key   | Required | Value type | Value description                                                  |
| ----- |:--------:| ---------- | ------------------------------------------------------------------ |
| in    | Yes      | string     | An iterable variable that can be evaluated.                        |
| for   | Yes      | string     | Name of iterating variable.                                        |
| block | Yes      | list       | A list of other rules is generated for each item in the iteration. |

Requires providing a `Context` that includes the necessary information for the rules in the `block`. The `in` keyword must be represented by a `EvalRule` variable, and the value of this variable must be a `Interable` type.

**Example**

```python
>>> context = build_saved_lines_context([
...     Line(content="This is the line_1 content"),
...     Line(content="This is the line_2 content"),
... ])
>>> dictrule.Generator({
...     "for": "line"
...     "in": "saved_lines"
...     "block: [
...         "line.index",
...         "line.content"
...     ]
... }).generate()
1
This is the line_1 content
2
This is the line_2 content
```

### FormatRule

This rule formats text according to specified rules. This rule now supports the following types:

| Key               | Value type       | Value description                                                     |
| ----------------- | ---------------- | --------------------------------------------------------------------- |
| format_lowercase  | string/list/dict | A text or rules generated to format text in lowercase.                |
| format_uppercase  | string/list/dict | A text or rules generated to format text in uppercase.                |
| format_upper_head | string/list/dict | A text or rules generated to format the first character to uppercase. |

**Example**

```python
>>> dictrule.Generator({
...     "format_lowercase": "UPPERCASE TITLE"
...     "format_uppercase": "lowercase content"
...     "format_upper_head": "camelVariable"
... }).generated()
uppercase title
LOWERCASE CONTENT
CamelVariable
```

### IndentRule

This rule indents generated text from provided rules by a specified number of indent spaces.

| Key prefix | Required | Value type       | Value description                                                                                                                                        |
| ---------- |:--------:| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| indent     | Yes      | string/list/dict | Indents multiple lines of parsed text from rules by specified indent (splits after `indent_` prefix)<br/>Example: `indent_1`, `indent_2`, `indent_3`,... |

Defines the number of spaces for text indentation by providing `IndentRule.ContextCase` within the `Context`.

**Example**

```python
>>> context = build_number_spaces_context(4)
>>> dictrule.Generator({
...     "class Menu:"
...     "indent_1": "def content(self):"
...     "indent_2": "return 'Empty'"
... }).generate(context)
class Menu:
    def content(self):
        return 'Empty'
```

### InlineRule

This rule builds generated text of a list of rules that are in a line.

| Key    | Required | Value type | Value description                          |
| ------ |:--------:| ---------- | ------------------------------------------ |
| inline | Yes      | list       | A list of other rules that join in a line. |

**Example**

```python
>>> dictrule.Generator({
...    "inline": ["This", " is", " the", " text", " in", " a", " line"]
... }).generate()
This is the text in a line
```

### JoinBlockRule

This rule joins generated texts for a block of rules by a specified separator.

| Key   | Required | Value type | Value description                                                 |
| ----- |:--------:| ---------- | ----------------------------------------------------------------- |
| join  | Yes      | string     | Separator for joining.                                            |
| block | Yes      | list       | A list of other rules that generates a list of texts for joining. |

**Example**

```python
>>> dictrule.Generator({
...     "join": "-"
...     "block": ["This", "is", "the", "snake", "line"]
... }).generate()
This-is-the-snake-line
```

### JoinEvalRule

This rule joins generated texts from the value of `EvalRule` by a specified separator.

| Key  | Required | Value type | Value description                             |
| ---- |:--------:| ---------- | --------------------------------------------- |
| join | Yes      | string     | Separator for joining.                        |
| eval | Yes      | string     | `EvalRule` value for joining generated texts. |

**Example**

```python
>>> context = build_football_teams_context([
...     "Real Madrid",
...     "Barcelona",
...     "Bayern Munchen",
...     "PSG",
...     "MC",
...     "MU",
...     "AC Milan",
... ])
>>> dictrule.Generator({
...     "join": ", "
...     "eval": "football_teams"
... }).generate(context)
Real Madrid, Barcelona, Bayern Munchen, PSG, MC, MU, AC Milan
```

### StringifyRule

This rule wraps content by quotes.

| Key       | Required | Value type       | Value description                                  |
| --------- |:--------:| ---------------- | -------------------------------------------------- |
| stringify | Yes      | string/list/dict | A text or other rules quoted after generated text. |

**Examples:**

```python
>>> dictrule.Generator({
...    "stringify": "This is the 1st text"
...    "stringify": "This is the 2nd text"
... }).generate()
"This is the 1st text"
"This is the 2nd text"
```

## Testing

`dictrule` includes a comprehensive test suite. To run the tests, run:

```shell
pytest
```

## Contributing

Read the [Contributing Guide](https://github.com/elhoangvu/dictrule/blob/trunk/CONTRIBUTING.md) to learn about reporting issues, contributing code, and more ways to contribute.

Submit bug reports and feature requests to the [dictrule bug tracker](https://github.com/elhoangvu/dictrule/issues).

## License

The `dictrule` module is written by Zooxy Le [elhoangvu@gmail.com](mailto:elhoangvu@gmail.com).

`dictrule` is released under the [MIT License](https://github.com/elhoangvu/dictrule/blob/main/LICENSE).
