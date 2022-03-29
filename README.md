## :information_source: Introduction

The goal of this template is to provide a way to write very condensed indexes typically for courses with multiple books. It leverages [LaTeX indexing](https://en.wikibooks.org/wiki/LaTeX/Indexing) by using a `.idx` file for organizing the index entries. The way this template can be used is by directly editing the `.idx` file.

> See folder [`examples`](examples/) for some real-life indexes which have already desmontrated their effectiveness.

Here is an example preview:

<p align="center"><img src="https://raw.githubusercontent.com/dhondta/tex-course-index-template/master/doc/preview.png">
<sub><sup>Preview image generated with <a href="https://gist.github.com/dhondta/f57dfde304905644ca5c43e48c249125">this tool</a></sup></sub></p>

## :card_file_box: Structure

The template is structured in the following way:

- [`main.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.tex): This is the main TeX file to be compiled. No need to edit this file unless you require to adapt the layout of the course index.
- [`main.idx`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.idx): This holds the index entries of the books of the course to be indexed.
- [`data.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/data.tex): This defines a few course-related variables (title, code, date and version) to be used in [`main.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.tex).
- [`lib`](https://github.com/dhondta/tex-course-index-template/blob/master/src/lib): This folder contains the images called in [`main.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.tex) and for use in [`main.idx`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.idx) (useful e.g. for mentioning that a tool is only for linux ; then use the `\linux` command in the `\indexentry`).

## :gear: Compilation

The compilation can easilly be configured in [Texmaker](https://en.wikipedia.org/wiki/Texmaker) by defining a *Quick Build Command*:

1. Go to the menu *Options*
2. Select *Configure Texmaker*
3. Go to tab *Quick Build*
4. In the field *User : (...)*, replace the command with:

       makeindex %.idx -s lib/std.ist|pdflatex -synctex=1 -interaction=nonstopmode %.tex|evince %.pdf|cp %.idx %.idx.bak|rm %.ilg %.ind %.aux %.synctex.gz

5. Then click *OK*

When editing the index with [Texmaker](https://en.wikipedia.org/wiki/Texmaker):

1. Open [`main.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.tex)
2. Go to the menu *Options*
3. Select *Define Current Document as "Master Document"*
4. Open [`main.idx`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.idx) for edition
5. Click on *Quick Build* to compile

This will produce [`main.pdf`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.pdf) with all the index entries organized in a two-columns document.

NB: Do not forget to edit [`data.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/data.tex).

> **Important**: It could happen that Texmaker is configured to remove temporary files while exiting, including `main.idx`. That's why the *Quick Build* herebefore includes `cp %.idx %.idx.bak` to backup this file and not to loose hours of work adding index entries. If removal still occurred, simply restore `main.idx.bak` to `main.idx`. Note that, consequently, the **backup is not made if you do not build the document**. So, **mind clicking regularly on the *Quick Build* button** !

## :bookmark_tabs: Making your index

The only files to be edited when making a new index are:

1. [`data.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/data.tex): Define the course attributes there (title, code, date, version).
2. [`main.idx`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.idx): Define the index entries there.

### `idx` File Structure

[`main.idx`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.idx) file comes organized with a few example sections. Basically, one section represents a symbol, a digit or a letter for sorting the references. In this template:
- Symbols are reserved for the *Topics* section (e.g. for providing the course structure)
- Digits are reserved for the *Categories* section (e.g. for sorting interesting resources such as tools, commands, standards, ...)
- Letters are used normally

The *Topics* and *Categories* titles are defined in [`lib/std.ist`](https://github.com/dhondta/tex-course-index-template/blob/master/src/lib/std.ist).

### LaTeX Indexing Basics

The raw material of an `idx` file is the `indexentry`. The signature of this command is the following:

    \indexentry{some_text}{page_number_or_range}

> Example of valid index entry: `\indexentry{\textbf{Course Philosophy}}{1-10}`

It is possible to provide a reference and to alias it with a desired text thanks to the "`@`" symbol:

    \indexentry{reference@some_text}{page_number_or_range}

> **Important note**: The format of `reference` affects the index reference location. That is, an alias consisting of:
> 
> - 1+ digits and 1+ letters: will be sorted as a symbol, thus in the *Topics* section.
> - only digits: will be sorted as a number, thus in the *Categories* section.
> - 1+ letters then anything else: will be sorted as text, thus in the letter sections.

It is also possible to indent a reference under another one thanks to the "`!`" symbol:

    \indexentry{some_text!some_indented_text}{page_number_or_range}

> Example of valid index entry: `\indexentry{\textbf{Course Philosophy}!Principle 1}{10}`

One can format the page number by using the "`|`" symbol:

    \indexentry{some_text!some_indented_text|command}{page_number_or_range}

> Example of valid index entry: `\indexentry{\textbf{Course Philosophy}|textbf}{10}`


### Commands Available in the Template

`main.tex` defines a few useful commands that can be mixed with `indexentry` in `main.idx`. Note that, in the following descriptions, `...` must each time be set so that the entry is sorted at the right location in the document.

- Adding a blank line: `\blankline`

      \indexentry{...@\blankline|comment}{0}

  > Example: `\indexentry{1b@\blankline|comment}{0}`

- Insert a page break: `\newpage` (standard in LaTeX)

      \indexentry{...@\blankline|newpage \comment}{0}

  > Example: `\indexentry{999@\blankline|newpage \comment}{0}`

- Fill in the page number with the book code: `\book{x}`

      \indexentry{...|book{x}}{...}

  > Example: `\indexentry{A reference in the third book|book{3}}{123}`

- Insert a rating with stars: `\rate{x}`

      \indexentry{... \rate{x}|...}{...}

  > Example: `\indexentry{A very useful reference \rate{5}|book{1}}{45}`

- Insert graphics: `\linux`, `\mac`, `\win`, `\all`, ...

      \indexentry{... \[graphic]|...}{...}

  > Example: `\indexentry{A Windows-related reference \win|book{2}}{67}`


### Predefined Icons

For convenience, multiple shorcuts are predefined in [`main.tex`](https://github.com/dhondta/tex-course-index-template/blob/master/src/main.tex) and the [`lib`](https://github.com/dhondta/tex-course-index-template/blob/master/src/lib) folder for displaying icons:

- `\all`: cross-platform ; Linux, Windows and Mac
- `\android`: Android
- `\cloud`: cloud icon with a server
- `\coin`: dollar (for paid asset)
- `\ios`: iOS
- `\linux`: Linux
- `\mac`: Mac OS
- `\note`: paper note with a pen
- `\portable`: USB key
- `\python`: Python script
- `\script`: general-purpose script
- `\question`: red question mark (e.g. for pointing an entry related to an exam question)
- `\solaris`: Soralis
- `\web`: Web-related asset
- `\win`: Windows


## :star: Related Projects

You may also like these:

- [TeX Book Template](https://github.com/dhondta/tex-book-template): A template for writing a nice book with LaTeX.
- [TeX Master Thesis Template](https://github.com/dhondta/tex-master-thesis-template): A template for writing a nice master thesis dissertation with LaTeX.


## :clap:  Supporters

[![Stargazers repo roster for @dhondta/tex-course-index-template](https://reporoster.com/stars/dark/dhondta/tex-course-index-template)](https://github.com/dhondta/tex-course-index-template/stargazers)

[![Forkers repo roster for @dhondta/tex-course-index-template](https://reporoster.com/forks/dark/dhondta/tex-course-index-template)](https://github.com/dhondta/tex-course-index-template/network/members)

<p align="center"><a href="#"><img src="https://img.shields.io/badge/Back%20to%20top--lightgrey?style=social" alt="Back to top" height="20"/></a></p>

