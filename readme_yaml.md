Itt tartok: https://www.tutorialspoint.com/yaml/yaml_character_streams.htm

# Notes on YAML

Used information
* general documentation
  * YAML Specification Index: https://yaml.org/spec/
  * https://www.tutorialspoint.com/yaml/index.htm
    * (for me, the explanations there were often not clear enough :( )
  * YAML parser (usable as format validator): http://www.yamllint.com/
* information to some details
  * https://stackoverflow.com/questions/50788277/why-3-dashes-hyphen-in-yaml-file
  * https://yaml-multiline.info/


# General features

* YAML = "YAML Ain’t markup language"
* Current version: 1.2 (2009)  - https://yaml.org/spec/1.2/
  * Revision 1.2.2 (Oct. 2021)
* data serialization language
* human-readable structured format
* unicode-based
* case-sensitive
* file extension: .yaml
* the content builds a **representation node graph**
  * root node: the current document
  * during serialization, a serialization event tree will be built
* no tabulator use allowed! use spaces instead
* structure through
  * indentation (block-style) 
  * separation (flow-style)
* keys and values
  * basic values:
    * "scalar": literal value, it can have different types: string, integer, float  
    * "block scalar", "flow scalar"
  * complex types: arrays and objects
    * "sequence": a list structure
    * "mapping": an associative array (dict) structure
    * "collection": unnamed mappings 
      * TODO ???

## Indicator characters

| Character | Functionality | 
| --- | --- |
| _ | (underscore) It denotes a block sequence entry | 
| ? | It denotes a mapping key | 
| : | It denotes a mapping value | 
| , | It denotes flow collection entry | 
| [ | It starts a flow sequence | 
| ] | It ends a flow sequence | 
| { | It starts a flow mapping | 
| } | It ends a flow mapping | 
| # | It denotes the comments | 
| & | It denotes node’s anchor property | 
| * | It denotes alias node | 
| ! | It denotes node’s tag | 
| &#124; | (pipe) It denotes a literal block scalar | 
| \> | It denotes a folded block scalar | 
| ' | Single quote surrounds a quoted flow scalar | 
| " | Double quote surrounds double quoted flow scalar | 
| % | It denotes the directive used |

Example 
* TODO ???
```yaml
%YAML 1.1
---
!!map {
   ? !!str "sequence"
   : !!seq [
      !!str "one", !!str "two"
   ],
   ? !!str "mapping"
   : !!map {
      ? !!str "sky" : !!str "blue",
      ? !!str "sea" : !!str "green",
   }
}

# This represents
# only comments.
---
!!map1 {
   ? !!str "anchored"
   : !local &A1 "value",
   ? !!str "alias"
   : *A1,
}
!!str "text" 
```

## Production parameters

* Each parameter has a range of allowed values
* **Indentation**: 
  * an appropriate amount of spaces
  * NOTE: no tabulator character is allowed
  * indentation introduces scopes
* **Context**: 
  * a kind of representation "style" for blocks
  * **block style**, **flow style**
* **Style**:
  * for scalar content, there are 5 styles:
    * **plain** (no indicator)
    * **single quoted flow** (`' ... '`)
    * **double quoted flow**  (`" ... "`)
    * **literal block** (`|`) 
    * **folded block** (`>`)
* **Chomping**:
  * for handling newline characters around block scalars
  * 3 possible chomping types:
    * **clip** (default)
    * **strip** (`-`)
    * **keep** (`+`)

## Indentation Spaces

* only spaces (no tab character allowed)
* the indentation spaces are not part of the node's content

## Separation Spaces

* Spaces are also used for separation between tokens. No tab character is allowed.

## Ignored Line Prefix

* An empty prefix always includes indentation depending on the scalar type.
* e.g.
  ```yaml
  %YAML 1.1
  ---
  !!map {
     ? !!str "plain"
     : !!str "text lines",
     ? !!str "quoted"
     : !!str "text lines",
     ? !!str "block"
     : !!str "text·®lines\n"
  }
  ```
  * Output:
  ```json
  {
    "plain": "text lines", 
    "quoted": "text lines", 
    "block": "text\u00b7\u00aelines\n"
  }
  ```

## Line folding

* Line folding allows breaking long lines for readability.
* e.g.
* e.g.
  ```yaml
  %YAML 1.1
  --- !!str
  "specific\L\
  trimmed\n\n\n\
  as space"
  ```
  * Output:
  ```json
  "specific\u2028trimmed\n\n\nas space"
  ```

# Structure: Block-style vs. flow-style

## Structure via indentation

* There is no amount of mandatory spaces.
* Indentation can be different for each block.
* In a block, the content can be a literal, or a collection.

## Block-style
* Block-style YAML follows a **strict indented syntax** for lists and objects. 
  * The indentation show the structure of scopes.
  * e.g.:
  ```yaml
  dev_test:
    environment:
      name: dev
    extends:
      - .env_vars
      - .test
  ```
* For literal content:
  * **Block style indicator**: indicates how newlines inside the block should behave.
    * **literal style**: indicated by the pipe symbol `|`
      * newline kept as newline
      * blank lines are interpreted as blank lines
      * spaces due to indentation are removed
      * e.g. (blank line is interpreted as an empty line)
      ```yaml
      example: |
        Several lines of text,
        with some "quotes" of various 'types',
        and also a blank line:
      
        plus another line at the end.
      ``` 
      * There is no way to escape characters inside literal scalars.
    
    * **folded style**: indicated by the right angle bracket symbol `>`
      * newlines are replaces by spaces
      * to get a newline, leave a blank line within lines
      * lines with additional indentation are not folded
      * spaces due to indentation are removed
      * e.g. (blank line is interpreted as a newline)
      ```yaml
      example: >
        Several lines of text,
        with some "quotes" of various 'types',
        and also a blank line:
      
        plus another line at the end.
      ```
  * **Block Chomping indicator**: there are different interpretations of the newline characters at the beginning and end of a scalar block. Block chomping will be indicated after the block style indicator.
    * **clip**: default behaviour, it puts a single newline at the end of the string
      * without any indicator: `|` or `>`
    * **strip**: it removes all newlines at the beginning and end
      * `|-` or `>-`
    * **keep**: it keeps all newlines at the beginning and end
      * `|+` or `>+`
  * **Indentation indicator**: Additionally to, and after the block style and block chomping indicators, optionally it is possible to give the amount of spaces used for the current indentation.
    * e.g. `|+2`, `>4`
    * valid numbers are 1 to 9

* For collection content: (sequence, mapping, node)
  * not denoted by any indicator
  * **block sequence** entries are denoted by a leading hyphen and space: `- `
  * **block mapping** entries can be written in a compact in-line style, or in a block notation 
    * If the `?` indicator is specified, the optional value node must be specified on a separate line, denoted by the `:` indicator.
  * **nodes**: embedded blocks inside block collections
## Flow-style
* The flow-style YAML uses further delimiters for showing the scope begins and ends.
  * e.g.: 
  ```yaml
  dev_test:
    environment: { name: dev }
    extends: [ .env_vars, .test ]
  ``` 
  * json-isque syntax
* Flow block contents must be indented with must be at least one space more thant the current block level.
* Flow content span multiple lines.
  * TODO ???
* It begins with `{` or `[`
  * e.g. `[PHP, Perl, Python]`
* Flow scalars have more limited escaping support.

# Documents and streams

* A "stream" is an input base for the yaml content.
  * e.g. a file, or directly loaded content in a script
  * A stream can contain one or more documents. 

* "Document": One cohesive content within a stream
  * multiple documents within a stream are separeted with 3 hyphens `---` 
  * The 3 hyphens are the signal start for the next document.
  * If there is a need of marking the end of a document, it is marked with 3 dots `...` 
    * e.g. if there are multiple documents in the stream, and not only the first document has directives
    * ```yaml
    %YAML 1.2
    %TAG !foo! !foo-types/
    ---
    myKey: myValue
    ...
    %TAG !bar! !bar-types/
    ---
    doc2
    ```
  * A document can have "directives".

# Directives: Tags and anchors

* "Directives" are instructions to the YAML processor, thus meta information, and they are not reflected in the document's representation graph.
  * tags and anchors
  * directive lines begin with a percentage sign `%`
  * apply to the following document only 
  * ```yaml
    %YAML 1.2
    %TAG !foo! !foo-types/
    ---
    myKey: myValue
    ...
    %TAG !bar! !bar-types/
    ---
    doc2
    ```
  * e.g. `%YAML `

* "Tag": Within a directive
  * `%TAG !foo! !foo-types/`
  * 
* "Anchor": within a directive
  * TODO ???

# Nodes

* YAML supports 3 kinds of nodes:
  * scalars:
    * include unicode characters
  * sequences: one type of collections
    * ordered series of zero or more nodes
  * mappings: the other type of collections
    * key-value-pairs
    * the keys have to be uniq
* 

* Nodes are labelled with one or two exclamation mark(s) `!`, `!!`; the node is a string which can be expanded into an URI/URL.
  * TODO ???
* "Repeated nodes in each file are initially denoted by an ampersand (&) and by an asterisk (*) mark later."
  * TODO ???
  


# Block 

* Each block has a scope.

```yaml
--- !clarkevans.com/^invoice
invoice: 34843
date   : 2001-01-23
bill-to: &id001
   given  : Chris
   family : Dumars
   address:
      lines: |
            458 Walkman Dr.
            Suite #292
      city    : Royal Oak
      state   : MI
      postal  : 48046
ship-to: *id001
product:
    - sku         : BL394D
      quantity    : 4
      description : Basketball
      price       : 450.00
   - sku         : BL4438H
      quantity    : 1
      description : Super Hoop
      price       : 2392.00
tax  : 251.42
total: 4443.52
comments: >
    Late afternoon is best.
    Backup contact is Nancy
    Billsmer @ 338-4338.
```

## Block collections
* Each entry begins with a new line.
* Block sequences in collections: 
  * each entry of the sequence is beginning with a dash and space on a new line `- ENTRY`
* Mappings are 


# Scalars

* two types: (see under Block styles)
  * literal scalars: indicated with `|`
  * folded scalars: indicated with `>`

* Scalar indication for flow scalars:
  * **single-quoted**: 
    * No escape sequences allowed.
    * Literal single quote within the scalar: `''`
    * Newlines can be added by a blank line.
    * It may contain tab characters.
    * e.g.
    ```yaml
    example: 'Several lines of text,\n
      containing ''single quotes''. Escapes (like \n) don''t do anything.\n
      \n
      Newlines can be added by leaving a blank line.\n
        Leading whitespace on lines is ignored.'\n
    ```
  * **double-quoted**:
    * Escape sequences are working, e.g. `\n` is interpreted as a newline -- escaping it: `\\n`
    * Escaping double quotes: `\"`
    * It may contain tab characters.
    * e.g.
    ```yaml
    example: "Several lines of text,\n
      containing \"double quotes\". Escapes (like \\n) work.\nIn addition,\n
      newlines can be esc\\n
      aped to prevent them from being converted to a space.\n
      \n
      Newlines can also be added by leaving a blank line.\n
        Leading whitespace on lines is ignored."\n
    ```
  * **plain**: 
    * No escape sequences are working.
    * Newlines can be added with a blank line.
    * Plain scalars should not contain any tab character.
    * e.g. 
    ```yaml
    example: Several lines of text,\n
      with some "quotes" of various 'types'.\n
      Escapes (like \n) don't do anything.\n
      \n
      Newlines can be added by leaving a blank line.\n
        Additional leading whitespace is ignored.\n
    ```
    * Plain flow scalars are picky about the `:` and `#` characters. They can be in the string, but `:` cannot appear before a space or newline, and `#` cannot appear after a space or newline; doing this will cause a syntax error. If you need to use these characters you are probably better off using one of the quoted styles instead.

# Anchors (variables, alias node)

* Use anchors/variables for avoiding duplicated contents.
* Define an anchor with `&NAME`
* Access to the anchor content with `<<: *NAME`

Example:
```yaml
defaults: &defaults
   adapter:  postgres
   host:     localhost

development:
   database: myapp_development
   <<: *defaults

test:
   database: myapp_test
   <<: *defaults

```
If the YAML is converted to JSON format, you see the automatically resolved variable contents:

```json
{
   "defaults": {
      "adapter": "postgres",
      "host": "localhost"
   },
   "development": {
      "database": "myapp_development",
      "adapter": "postgres",
      "host": "localhost"
   },
   "test": {
      "database": "myapp_test",
      "adapter": "postgres",
      "host": "localhost"
   }
}
```

# String

* String values are separated using double-quoted string
* Quotation can be dropped.
  * TODO in which cases?
* 

# Collection

* Two kind of collections: 
  * sequences 
  * mappings
* Collections are marked with a leading hyphen `-`
* A collection can contain all types of nodes (scalars, sequences, mappings)
* A collection has no name (aka 'key')
* e.g. collection of mappings
  ```yaml
  -
  name: Mark Joseph
  hr: 87
  avg: 0.278
  -
  name: James Stephen
  hr: 63
  avg: 0.288
  ```

# Sequence (List)

* List members are 
  * denoted by a leading hyphen `-`
  * or enclosed in square brackets, and separated by commas (and spaces)
* items: scalar values

```yaml
--- # Favorite movies
 - Casablanca
 - North by Northwest
 - The Man Who Wasn't There
```

```yaml
--- # Shopping list
   [milk, groceries, eggs, juice, fruits]
```

```yaml
men: [John Smith, Bill Jones]
```

```yaml
women:
  - Mary Smith
  - Susan Williams
```

# Mapping (Dict, Associative array)

* key and value are separated by a colon: `KEY: VALUE`
* the dict is enclosed in curly brackets: `{KEY1: VALUE1, KEY2: VALUE2}`


```yaml
- {name: John Smith, age: 33}
```

```yaml
- name: Mary Smith
  age: 27
```

## Complex mapping

* ` ? ... : ...`
  * TODO ???
* e.g. mapping between sequences
  ```yaml
  - 2001-07-23
  ? [ New York Yankees,Atlanta Braves ]
  : [ 2001-07-02, 2001-08-12, 2001-08-14]
  ```
* e.g.
  ```yaml
  %YAML 1.1
  ---
  !!map {
     ? !!str "Not indented"
     : !!map {
        ? !!str "By one space"
        : !!str "By four\n spaces\n",
        ? !!str "Flow style"
        : !!seq [
           !!str "By two",
           !!str "Still by two",
           !!str "Again by two",
        ]
     }
  }
  ```
  * The output that you can see after indentation is as follows −
  ```json
  {
     "Not indented": {
        "By one space": "By four\n spaces\n", 
        "Flow style": [
           "By two", 
           "Still by two", 
           "Again by two"
        ]
     }
  }
  ```

# Comment

* There is only single line comments, beginning with `#`.
* Comments are separated from other tokens by whitespace(s).
* e.g.
  ```yaml
  # this
  # is a multiple
  # line comment
  key: #comment 1
   - value line 1
   #comment 2
   - value line 2
   #comment 3
   - value line 3
  ```
* Comments must not appear inside scalars. 
  * YAML does not include any way to escape the hash symbol (`#`) so within multi-line string there is no way to divide the comment from the raw string value.

# Processing YAML streams

* The processing of YAML information includes three stages:
  * Representation
  * Serialization
  * Presentation and Parsing.
* **Representation**:
  * 3 kinds of nodes: scalar, sequence, mapping
  * **scalar**: strings, integers, dates, atomic data types
  * **sequence**: ordered number of entries
  * **mapping**: dictionary/hash table/associative array
  * Note that YAML also includes nodes which specify the data type structure.
    * TODO ???
* **Serialization**:
  * Result: YAML serialization tree
* **Presentation**:
  * The final output of YAML serialization: events -> characters.
  * It represents a character stream in a human friendly manner.
* **Parsing**:
  * Inverse process of presentation: characters -> events.
  * This process needs a well-formed input - otherwise, the parsing procedure will fail.
  * YAML Lint: online parser for YAML
    * http://www.yamllint.com/


# YAML with Python

* libraries:
  * PyYAML: last release 6.0 (Python 3 support >=3.08)
    * https://pyyaml.org/; https://pypi.org/project/PyYAML/
    * for YAML 1.1
    * `pip install pyyaml`
    * https://pyyaml.org/wiki/PyYAMLDocumentation
  * ruamel.yaml: last release 0.17 (Python 3.5 >=0.17)
    * https://pypi.org/project/ruamel.yaml/
    * for YAML 1.2 
    * `pip install ruamel.yaml`
    * https://yaml.readthedocs.io/en/latest/basicuse.html

## PyYAML examples

```python
yaml.load(Quick brown fox)  # -> string
yaml.load("3.14")           # -> float
yaml.load("""
    - eggs
    - ham
    - ...
    """)                    # -> list of strings
```

# Further tools

* browser-based comparison of two yaml files: https://yamldiff.com/