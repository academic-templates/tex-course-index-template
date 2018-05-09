# LaTeX Course Index Template

The goal of this template is to provide a way to write very condensed indexes typically for courses with multiple books. It leverages [LaTeX indexing](https://en.wikibooks.org/wiki/LaTeX/Indexing) by using a `.idx` file for organizing the index entries. The way this template can be used is by directly editing the `.idx` file.

## Structure

The template is structured in the following way:

- `main.tex`: This is the main TeX file to be compiled. No need to edit this file unless you require to adapt the layout of the course index.
- `main.idx`: This holds the index entries of the books of the course to be indexed.
- `data.tex`: This defines a few course-related variables (title, code and date) to be used in `main.tex`.
- `lib`: This folder contains the images called in `main.tex` and for use in `main.idx` (useful e.g. for mentioning that a tool is only for linux ; then use the `\linux` command in the `\indexentry`).

## Compilation

The compilation can easilly be configured in [Texmaker](https://en.wikipedia.org/wiki/Texmaker) by defining a *Quick Build Command*:

1. Go to the menu *Options*
2. Select *Configure Texmaker*
3. Go to tab *Quick Build*
4. In the field *User : (...)*, replace the command with:

       makeindex %.idx -s lib/std.ist|pdflatex -synctex=1 -interaction=nonstopmode %.tex|evince %.pdf|rm %.ilg %.ind %.aux %.synctex.gz

5. Then click *OK*

When editing the index with [Texmaker](https://en.wikipedia.org/wiki/Texmaker):

1. Open `main.tex`
2. Go to the menu *Options*
3. Select *Define Current Document as "Master Document"*
4. Open `main.idx` for edition
5. Click on *Quick Build* to compile

This will produce `main.pdf` with all the index entries organized in a two-columns document.

NB: Do not forget to edit `data.tex`.

## Making your index

### `idx` File Structure

`main.idx` file comes organized with a few example sections. Basically, one section represents a symbol, a digit or a letter for sorting the references. In this template:
- Symbols are reserved for the *Topics* section (e.g. for providing the course structure)
- Digits are reserved for the *Categories* section (e.g. for sorting interesting resources such as tools, commands, standards, ...)
- Letters are used normally

This behavior is defined in `lib/std.ist`.

### LaTeX Indexing Basics

The raw material of an `idx` file is the `indexentry`. The signature of this command is the following:

    \indexentry{some_text}{page_number_or_range}

> Example of valid index entry: `\indexentry{\textbf{Course Philosophy}}{1-10}`

It is possible to provide a reference and to alias it with a desired text thanks to the "`@`" symbol:

    \indexentry{reference@some_text}{page_number_or_range}

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

  > \indexentry{1b@\blankline|comment}{0}

- Insert a page break: `\newpage` (standard in LaTeX)

      \indexentry{...@\blankline|newpage \comment}{0}

  > \indexentry{999@\blankline|newpage \comment}{0}

- Fill in the page number with the book code: `\book{x}`

      \indexentry{...|book{x}}{...}

  > \indexentry{A reference in the third book|book{3}}{123}

- Insert a rating with stars: `\rate{x}`

      \indexentry{... \rate{x}|...}{...}

  > \indexentry{A very useful reference \rate{5}|book{1}}{45}

- Insert graphics: `\linux`, `\mac`, `\win`, `\all`, ...

      \indexentry{... \[graphic]|...}{...}

  > \indexentry{A Windows-related reference \win|book{2}}{67}
