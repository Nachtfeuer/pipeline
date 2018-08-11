# The spline-loc tool

## Purpose

Helping to verify that the ratio between code and comments
is at a level you can accept.


## The usage

You can be sure that the list will be empty when you read this :)
However you can specify a path with `--path` (you can repeat that parameter).

The threshold (ratio) is at 0.5 by default but you can specify `--threshold` (or `-t`)
to take another one you prefer. The threshold is for all files. At the moment
Bash, Python, Java, Javascript, Typescript, Groovy and C++ are supported.

If one file has been found that is below given threshold the tool ends with exit code 1.

```bash
$ spline-loc --path=spline
2018-08-11 11:04:34,790 - spline.tools.loc.application - Running with Python 2.7.13 (default, Nov 24 2017, 17:33:09) [GCC 6.3.0 20170516]
2018-08-11 11:04:34,798 - spline.tools.loc.application - Running on platform Linux-4.9.0-6-amd64-x86_64-with-debian-9.4
2018-08-11 11:04:34,799 - spline.tools.loc.application - Current cpu count is 4
|-----|---|---|--------------------|------|
|Ratio|Loc|Com|File                |Type  |
|-----|---|---|--------------------|------|
|0.36 |73 |26 |pipeline.py         |Python|
|0.35 |162|57 |application.py      |Python|
|0.34 |77 |26 |tools/event.py      |Python|
|0.38 |89 |34 |tools/version.py    |Python|
|0.26 |213|56 |components/tasks.py |Python|
|0.36 |80 |29 |components/config.py|Python|
|-----|---|---|--------------------|------|
```

You can use the option `--show-all` (or `-s`) to show all files.


## About loc, com and ratio

- **LOC** - lines of code without comments; empty lines included.
- **COM** - lines of comments; empty comment lines includes.
- **RATIO** - **COM** / **LOC** if **COM** < **LOC** otherwise 1.0.

**Some notes**:

- if you have as many comments as you have code the ratio is 1.0
- if you have one line comment for four lines code the ration is 0.25
- if you have comments only the ratio is 1.0
- if you have more comments than code the ratio is also 1.0

Basially I was interested in code that has not enough comments which
focuses on ratios below 1.0. That's the idea.

## About comments

 - I do not check about empty lines.
 - I do not check for sense ... if somebody writes 'bla bla bla' a code review should reject.
 - I do not check tags against parameters because a) there are to many different styles and b)
   it would required to parse each language to know which parameters a function or method has.
