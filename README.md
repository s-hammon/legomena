# Legomena

Get certain stats about lengthy bodies of text, such as novels, research papers, and AI-generated constructs with this CLI tool,

## Introduction

Legomena (lego for short) is a CLI tool which can read text files and provide various statistics and metrics on them. Presently, this tool can return:

* the top *n* most frequently occuring words
* the ratio of the set of words occurring once in a body of text (*hapax legomena*) to the unique set of words
* the ratios of the set of words occurring once, twice (*dis legomena*), and trice (*tris legomena*) to the set of words occurring four times (*tetrakis legomena*)

It can also calculate the theoretical proportion of each word's frequency in a body of text to the text's total word count using its ordinal rank in word count, per [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law). This is compared with the actual proportions to return a [chi-squared](https://en.wikipedia.org/wiki/Chi-squared_text) distribution.

The output from this CLI app may be used with other programs to compare bodies of texts, optimize keyword searching, or possibly detect AI-generated texts.

**Note:** Often, the actual word proportions of a text--particularly smaller bodies such as poems or articles--differ greatly from the ideal Zipfian curve, and as a result the chi-squared can be astronomically high. This *may* be abated by removing the words which occur less than 5-10 times in a body of text, which this CLI tool supports, but often this is not the case. Of course, more data is always better, and generally doing this kind of analysis on an author's *entire* repertoire yields better results than just on any one of their works.

## Project Details

This project was designed around two principles: 

1. Limit dependencies as much as is practical, and
2. Provide for very simple integration with other projects

On point #1, this project's (major) dependency is `numpy`, without which calculating the Zipf proportions is practically impossible on any sufficiently large body of work (*Moby Dick* could run all year, for example). Since the chi-squared is the only statistical method used here--and is quite easy to do by hand--I put off the inclusion of a statistical library like `scipy` until use-cases for this tool were further cemented. Everything else, ranging from things like text comprehension, I/O, and CLI commands, were built using Python's standard library.

And on point #2, this project provides two methods in the `stdin` for providing text to analyze, as well as two options to retrieve the data. For each subcommand, the user may use either `--file`/`-f` to extract text from a provided file path, or `--config`/`-c` to use a JSON or YAML file to parse multiple files (see the **Config File** section). The default `stdout` values returned are a series of key-value pairs which may be piped into any other program. The user can also specify `--save`/`-s` to save the output to a file.

## Installation

### Requirements

* Python 3.10+
* git 
* pip 
* Linux or Windows OS

Clone this repository and build to your current Python environment:

```
git clone https://github.com/s-hammon/legomena
cd legomena
pip install .
```

Verify that the build was successful by running `lego -h`

## CLI

### `lego -h`

```
usage: lego [-h] {zipf,wordcount} ...

A CLI for (simple) analysis of text corpora. Incorporates Zipf's Law, Chi-Square tests, and ratio of words used only once, twice, thrice, and so on.

positional arguments:
    zipf            Analyze the text according to Zipf's Law
    wordcount       Get word dictionary of the text, and teh count of each word that appears.

options:
  -h, --help        show this help message and exit
```

### `lego zipf -h`

```
usage: lego zipf [-h] [--proportions] [--exclude-legomena] (--file FILE | --config CONFIG) [--combine] [--from-gutenberg] [--save SAVE]

options:
  -h, --help            show this help message and exit
  --proportions         Include the predicted and actual proportions of each word in the text
  --exclude-legomena    Exclude hapax, dis, tris, and tetrakis legomena from the analysis
  --file FILE, -f FILE  The path to the text file to analyze
  --config CONFIG, -c CONFIG
                        The path to the configuration file (must be YAML or JSON)
  --combine             Combine the text from multiple files into a single corpus. Can only be used with --config
  --from-gutenberg      If the text is from Project Gutenberg. Lego will remove header/footer text. Can only be used with --file
  --save SAVE, -s SAVE  The path to save the results of the analysis. May be TXT or JSON.
```

#### Config File

A JSON or YAML file containing a list of the following key-value pairs:

* fpath (string): path to file containing text to analyze
* name (string, optional): the name given to the analyzed file
* is_gutenberg (boolean, optional): indicates whether the text came from Project Gutenberg

If a file is a UTF-8 encoded text from Project Gutenberg, Legomena will extract the text between `*** START OF THE PROJECT GUTENBERG EBOOK {title} ***` and `*** END OF THE PROJECT GUTENBERG EBOOK {title} ***`. Providing the title is not necessary--simply set `is_gutenberg` to True and Legomena will take care of this under the hood.

### `lego wordcount -h`

```
usage: lego wordcount [-h] (--file FILE | --config CONFIG) [--combine] [--from-gutenberg] [--save SAVE]

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  The path to the text file to analyze
  --config CONFIG, -c CONFIG
                        The path to the configuration file (must be YAML or JSON)
  --combine             Combine the text from multiple files into a single corpus. Can only be used with --config
  --from-gutenberg      If the text is from Project Gutenberg. Lego will remove header/footer text. Can only be used with --file
  --save SAVE, -s SAVE  The path to save the results of the analysis. May be TXT or JSON.
```