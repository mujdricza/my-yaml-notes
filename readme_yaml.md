TODO:
* sort information
* make script examples
* verify todos, open questions

# Notes on this documentation

Used information
* general documentation
  * YAML Specification Index: https://yaml.org/spec/
  * https://www.tutorialspoint.com/yaml/index.htm
    * (for me, the explanations there were often not clear enough :( )
  * YAML parser (usable as format validator): http://www.yamllint.com/
  * YAML to JSON converter: https://onlineyamltools.com/convert-yaml-to-json
  * https://en.wikipedia.org/wiki/YAML
* information to some details
  * https://stackoverflow.com/questions/50788277/why-3-dashes-hyphen-in-yaml-file
  * https://yaml-multiline.info/
* Documentation of PyYAML: https://pyyaml.org/wiki/PyYAMLDocumentation

# General features

* YAML = "YAML Ain’t markup language" (originally: "Yet Another Markup Language")
* There is a correspondence between YAML streams and JSON files, where YAML streams can be represented as JSON content.
* First release: 2004 by Clark Evans
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
* "character streams": a sequence of bytes which will be processed, thus a character stream is a unit for processing
  * directives
  * document boundary markers
  * documents
  * complete stream

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

## JSON schema

* see https://yaml.org/type/index.html
* Since the YAML streams are considered to be parsed to JSON objects, it is a failsafe indication of values in YAML which helps to identify JSON object types.
* NOTE that all the values can be represented also without the failsafe indicators.
* A YAML schema is a combination of set of tags
* YAML schema -> JSON type:
  * scalar types:
    * null value: `!!null` -> `null`; 
      * see https://yaml.org/type/null.html: valid Null-values in YAML1.1: `~`, `null`, `Null`, `NULL`, `` (empty)
      * can be set as value (as key, it will be represented as string)
      * full example
      ```yaml
      !!null null: value for null string key
      key with null value: !!null null
      ```
      -> JSON: 
      ```json
      {
         "null": "value for null string key", 
         "key with null value": null
      }
      ```
      * boolean value: `!!bool` -> `true` / `false`
        * see https://yaml.org/type/bool.html: valid boolean values in YAML1.1: `y|Y|yes|Yes|YES|n|N|no|No|NO
|true|True|TRUE|false|False|FALSE`
|on|On|ON|off|Off|OFF
        * NOTE that there are differences in YAML1.1 and YAML1.2 in interpreting boolean values:
          * `g: Yes` -- a boolean `True`  in YAML1.1, but a string `"Yes"` in YAML1.2
        * full example
        ```yaml
        YAML is a superset of JSON: !!bool true
        Pluto is a planet: !!bool false
        ```
        -> JSON 
        ```json
        {
           "YAML is a superset of JSON": true, 
           "Pluto is a planet": false
        }
        ```
        * TODO: if omitting "!!bool"? -- also then `true` and `True` as values will be converted to `null` in JSON ?
        * e.g.
        ```yaml
        A null: null
        Booleans: [ true, false ]
        Integers: [ 0, -0, 3, -19 ]
        Floats: [ 0., -0.0, 12e03, -2E+05 ]
        Invalid: [ True, Null, 0o7, 0x3A, +12.3 ]
        ```
        --> JSON
        ```json
        {
           "Integers": [
              0, 
              0, 
              3, 
              -19
           ], 
         
           "Booleans": [
              true, 
              false
           ], 
           "A null": null, 
      
           "Invalid": [
                 true, 
                 null, 
                 "0o7", 
                 58, 
                 12.300000000000001
           ], 
         
           "Floats": [
              0.0, 
              -0.0, 
              "12e03", 
              "-2E+05"
           ]
        }
        ```
      
    * integer: `!!int`
    * float: `!!float`
    * string: `!!str`
    * binary: `!!binary` (bytes)
      * e.g. 
      ```yaml
      picture: !!binary |
        R0lGODdhDQAIAIAAAAAAANn
        Z2SwAAAAADQAIAAACF4SDGQ
        ar3xxbJ9p0qa7R0YxwzaFME
        1IAADs= 
      ```
    * value: `!!value` (default value of a mapping)
    * yaml: `!!yaml` (keys for encoding YAML)
    * further: merge: `!!merge`, timestamp: `!!timestamp`, 
  * collection types:
    * list: `!!seq`
    * set: `!!set`
    * dictionary: `!!map` (unordered), `!!omap` (odered)
    * pair: `!!pairs` (map allowing duplicated keys)  
  * NOTE that any pickleable object can be serialized using the `!!python/object` tag (see https://pyyaml.org/wiki/PyYAMLDocumentation)
    * Many implementations of YAML can support user-defined data types for object serialization. Local data types use a single exclamation mark `!`. 
      * e.g. `myObject: !myClass { name: Joe, age: 15 }`
    * Note that the ability to construct an arbitrary Python object may be dangerous if you receive a YAML document from an untrusted source such as the Internet. The function `yaml.safe_load` limits this ability to simple Python objects like integers or lists.

### Failsafe schema

* can be used with any YAML document
* two types:
  * **generic mapping**
  * **generic sequence**
* TODO: How do they differ from normal mappings and sequences?

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

# Character streams

* character stream types
  * **directives**
  * **document boundary markers**
  * **documents**
  * **complete streams**

## Directives

* basic instructions used in YAML processor
  * types:
    * **reserved directives**
      * initialized with 3 hyphen characters
      * will be converted into specific value of JSON
      * e.g.
      ```yaml
      %YAML 1.1
      --- !!str
      "foo"
      ```
    * **YAML directive**
      * YAML documents in a stream may be preceded by 'directives' composed of a percent sign (`%`) followed by a name and space-delimited parameters. Two directives are defined in YAML 1.1:
        * The `%YAML` directive is used for identifying the version of YAML in a given document. 
        * The `%TAG` directive is used as a shortcut for URI prefixes. These shortcuts may then be used in node type tags.
      * default directives
      * "If converted in JSON, the value fetched includes forward slash character in preceding and terminating characters."
      * e.g.
      ```yaml
        %YAML 1.1
        ---
        !!str "foo"
        ```
      * TODO: e.g. for %TAG

## Document boundary markers

* A line beginning with 3 dashes `---` is used to start a new document.
* to allow more than one document in one stream.
* e.g.
  ```yaml
  %YAML 1.1
  ---
  !!str "foo"
  %YAML 1.1
  ---
  !!str "bar"
  %YAML 1.1
  ---
  !!str "baz"
  ```

## Documents

* one YAML document is representing a single root node 
* non-content parts of a document
  * directives
  * comments
  * indentation and style elements
* two types:
  * **explicit documents**
  * **implicit documents**

### Explicit Documents

* explicit documents begin with `---` and (optionally) end with `...`
* e.g.
  ```yaml
  ---
  some: yaml
  ...
  ```

### Implicit Documents

* no document begin marker
* only one document in a stream possible

## Complete Streams

* character stream: sequence of bytes
* e.g.
  ```yaml
  %YAML 1.1
  ---
  !!str "Text content\n"
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
      * newlines are replaced by spaces
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
    * **strip**: it removes all line breaks and empty lines at the beginning and end
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
* Flow block contents must be **indented** with must be at least one space more thant the current block level.
* Flow content span multiple lines.
  * TODO ???
* It begins with `{` or `[`
  * e.g. `[PHP, Perl, Python]`
* Flow scalars have more limited escaping support.
* Flow style can be represented with failsafe properties (`!!str`, `!!seq`, `!!map` for different structure elements); The only flow style that does not have any property is the plain scalar.
  * e.g. full example:
  ```yaml
  %YAML 1.2
  ---
  !!seq [
  !!seq [ !!str "a", !!str "b" ],
  !!map { ? !!str "a" : !!str "b" },
  !!str "a",
  !!str "b",
  !!str "c",]
  ```
  * --> JSON:
  ```json
  [
     [
        "a", 
        "b"
     ], 
     
     {
        "a": "b"
     }, 
     
     "a", 
     "b", 
     "c"
  ]
  ```
* Nodes with empty content are considered as empty nodes.
  * e.g.
  ```yaml
  !!map {
    ? !!str "foo" : !!str "",
    ? !!str "" : !!str "bar",
  }
  ```
  --> JSON output: 
  ```json
  {
    "": "bar", 
    "foo": ""
  }
  ```
* See also section "Scalars"

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
  * The content of a document is compiled and represented under a single root node.

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
  * **scalars**:
    * include unicode characters
  * **sequences**: one type of collections
    * ordered series of zero or more nodes
    * the items can be repeated
  * **mappings**: the other type of collections
    * key-value-pairs
    * the keys have to be uniq
* Nodes can include anchors and tags.
  * **anchor**: a node for later reference of contents
    * indicator for **referencing**: leading ampersand `&`: `&MYANCHOR`
    * indicator for **dereferencing**: leading asterisk `*`: `*MYANCHOR`
      * the content of the anchor will be inserted into the JSON representation
    * the anchor name is case-insensitive -- TODO check
    * e.g. full example:
    ```yaml
    %YAML 1.1
    ---
    !!map {
       ? &A1 !!str "foo"  <-- A1 is the anchor name
       : !!str "bar",
       ? !!str &A2 "baz"
       : *a1              <-- using the anchor value accessed via the anchor name
    }
    ``` 
    * example with block style
    ```yaml
    port: &ports
      adapter:  postgres
      host:     localhost
    development:
      database: myapp_development
      <<: *ports
    ```
    --> JSON:
    ```json
    {
       "port": {
          "adapter": "postgres",
          "host": "localhost"
       },
       "development": {
          "database": "myapp_development",
          "adapter": "postgres",
          "host": "localhost"
       }
    }
  ```
    * NOTE that only whole nodes can be referenced and dereferenced, but not parts of nodes!
  * **tag**: "The tag property represents the type of native data structure which defines a node completely."  - ???
    * indicator: leading exclamation mark: "!"
    * Tags are part of the representation graph.
    * e.g. full example
    ```yaml
    %YAML 1.1
    ---
    !!map {
       ? !<tag:yaml.org,2002:str> "foo"
       : !<!bar> "baz"
    }
    ```
    * TODO: what is the tag above in the example? TODO: embedded tags? What is the benefit of tags? How will they be converted into json? 

* Nodes are labelled with one or two exclamation mark(s) `!`, `!!`; the node is a string which can be expanded into an URI/URL.
  * TODO ???
  * e.g. `!!map { ...}` is a dictionary node
  * e.g. full example (with anchors and tags):
  ```yaml
  %YAML 1.1
  ---
  !!map {
     ? &A1 !!str "foo"
     : !!str "bar",
     ? !!str &A2 "baz"
     : *a1
  }
  ```
* "Repeated nodes in each file can be marked by an anchor (&ANCHORNAME) and dereferenced by an asterisk (*ANCHORNAME) mark later."
  * see `&A1` and `*a1` in the example above
  
* empty nodes: node with empty content, e.g. `""`
  * e.g. full example
  ```yaml
  %YAML 1.2
  ---
  !!map {
     ? !!str "foo" : !!str "",
     ? !!str "" : !!str "bar",
  }
  ```
  * -> JSON:
  ```json
  {
  "": "bar",
  "foo": ""
  }
  ```


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

* two types for block scalars: (see under Block styles)
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

* With explicit marking: e.g. `!!str "my string value"`
* e.g. 
  ```yaml
  %YAML 1.1
  ---
  !!str "as space \
  trimmed\n\
  specific\L\n\
  none"
  ```
  * --> json: "as space trimmed\nspecific\u2028\nnone"
# Anchors (variables, alias nodes)

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
* Explicit marker as property: `!!str`
* Line breaks can be given explicitely like `\n`, multiple line breaks will be simplified to one as default.
  * e.g. 
 ```yaml
  !!str "as space \
  trimmed\n\
  specific\L\n\
  none"
  ```
  -> json: `"as space trimmed\nspecific\u2028\nnone"`

# Collection

* Two kind of collections: 
  * **sequences**: ordered sequence of items
  * **mappings**: unordered sequence of key-value pairs
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
* Flow collection entries are terminated with comma (,) indicator
  * e.g. full example:
  ```yaml
  %YAML 1.2
  ---
  !!seq [
     !!seq [
        !!str "one",
        !!str "two",
     ],
     !!seq [
        !!str "three",
        !!str "four",
     ],
  ]
  ```
  * -> JSON: `[["one", "two"], ["three", "four"]]`

# Sequence (List)

* ordered list of items
* List members are 
  * denoted by a leading hyphen `-`
  * or enclosed in square brackets, and separated by commas (and spaces)
* items: scalar values
* with explicit marker `!!seq [ ... ]`

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
men names: [John Smith, Bill Jones]  <-- the value is a sequence
```

* sequence in a block: with leading hyphen and following space `- `
```yaml
women:
  - Mary Smith   <-- the value is a sequence
  - Susan Williams
```

```yaml
%YAML 1.1
---
!!seq [
   !!str "milk",
   !!str "bread",
   !!map {
      ? !!str "white"
      : !!str "black"
   }
]
```

* Nested sequence:
  * e.g. in block notation full example
  ```yaml
  -
    - HTML
    - LaTeX
    - SGML
    - VRML
    - XML
    - YAML
  -
    - BSD
    - GNU Hurd
    - Linux
  ```
  -> JSON: `[['HTML', 'LaTeX', 'SGML', 'VRML', 'XML', 'YAML'], ['BSD', 'GNU Hurd', 'Linux']]`
  * It’s not necessary to start a nested sequence with a new line:
  ```yaml
  - 1.1
  - - 2.1
    - 2.2
  - - - 3.1
      - 3.2
      - 3.3
  ```
  -> JSON: `[1.1, [2.1, 2.2], [[3.1, 3.2, 3.3]]]`

* Sequence of mappings:
  * e.g.
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
  
# Mapping (Dict, Associative array)

* unordered collection of key-value pairs
* keys are uniq within a mapping node
* key and value are separated by a colon: `KEY: VALUE`
* the dict can be enclosed in curly brackets: `{KEY1: VALUE1, KEY2: VALUE2}`, or indicated by indention
* explicitely set node structure: `!!map {...}` with key after a `?` and value after `:`
* NOTE that both key and value can contain multiple words
  * TODO check

```yaml
- {full name: John Smith, age: 33}
```

```yaml
- full name: Mary Smith
  age: 27
```

* a more complex example
```yaml
%YAML 1.1
paper:
   uuid: 8a8cbf60-e067-11e3-8b68-0800200c9a66
   name: On formally undecidable propositions of  Principia Mathematica and related systems I.
   author: Kurt Gödel.
tags:
   - tag:
      uuid: 98fb0d90-e067-11e3-8b68-0800200c9a66
      name: Mathematics
   - tag:
      uuid: 3f25f680-e068-11e3-8b68-0800200c9a66
      name: Logic
```
-> JSON:
```json
{
   "paper": {
      "author": "Kurt Gödel."
      "name": "On formally undecidable propositions of Principia Mathematica and related systems I.",
      "uuid": "8a8cbf60-e067-11e3-8b68-0800200c9a66",
   },
   "tags": [
      {
         "tag": {
            "uuid": "98fb0d90-e067-11e3-8b68-0800200c9a66",
            "name": "Mathematics"
         }
      },
      {
         "tag": {
            "uuid": "3f25f680-e068-11e3-8b68-0800200c9a66",
            "name": "Logic"
         }
      }
   ]
}
```

* Mapping of sequences:
  * e.g.
  ```yaml
  - 2001-07-23
  ? [ New York Yankees,Atlanta Braves ]  # key
  : [ 2001-07-02, 2001-08-12, 2001-08-14]  # value
  ```


* With node presentations
```yaml

%YAML 1.1
---
!!map {
   ? !!str "simple key"
   : !!map {
      ? !!str "also simple"
      : !!str "value",
      ? !!str "another a simple key"
      : !!seq [
        !!str "seq1",
        !!str "seq2"
     ]  
   }
}
```
```json
{
   "simple key": {
      "another simple key": ["seq1", "seq2"], 
      "also simple": "value"
   }
}
```

* NOTE the difference between a sequence and another mapping within a mapping node:
  * sequence within a mapping node
  ```yaml
  port: 
    - postgres adapter
    - localhost as host
  ```
  * another mapping within a mapping node
  ```yaml
  port: 
    adapter:  postgres
    host:     localhost
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
* If there is content before a comment within the line, you have to use a space before the hasthag: ` # comment`
  * e.g. `- C#    # Note that comments are denoted with ' #' (space then #).` - Here, `C#` is the content of the sequence item.
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
* Commented blocks are skipped during execution.

# Apostrophs and string content

* Scalar string content is just written without any indicator, or within quotes.
  * ??? can it be only double quotes, or also single ones?
* If quoting within a string is needed, use different quotes like
  * full example:
  ```yaml
  - The Dagger 'Narthanc'
  - The Dagger 'Nimthanc'
  - The Dagger 'Dethanc'
  ```
  --> JSON: `["The Dagger 'Narthanc'", "The Dagger 'Nimthanc'", "The Dagger 'Dethanc'"]`

# Processing YAML streams

* see the process in [pictures/yaml_processes.jpg] (from https://www.tutorialspoint.com/yaml/images/yaml_processes.jpg)

* "character streams": 
  * **directives**: basic instructions used in YAML processor
    * e.g. comments
    * types:
      * reserved directive: after 3 hyphens
        * e.g. `--- !!str` -- the following block will be converted into a string in JSON
        * full example: 
        ```yaml
          %YAML 1.1
          --- !!str
          "foo"
        ```
      * YAML directive: default directive
      * e.g. full example:
      ```yaml
      %YAML 1.1
      ---
      !!str "foo" 
      ```
      "If converted in JSON, the value fetched includes forward slash character in preceding and terminating characters." -- ???
  * **document boundary markers** allow to have more than one document within one stream
    * line starting with 3 hyphens `---` starts a new document
    * note that the document start marker can be/is preceded by directive lines. E.g.
      ```yaml
      %YAML 1.1
      %TAG !foo! !foo-types/
      ---
      !!str "Text content\n"
      ```
  * **documents**: a single native data structure with one single root node
    * explicit: starting with document start marker `---` (and optionally ending with the document end marker `...`)
    * implicit: no document boundary markers are present
  * **complete stream** 
* The processing of YAML information includes three stages:
  * Representation
  * Serialization
  * Presentation and Parsing.
* **Representation**:
  * the YAML structure will be converted into the "representation node graph" 
  * 3 kinds of nodes: scalar, sequence, mapping
  * **scalar**: strings, integers, dates, atomic data types
  * **sequence**: ordered number of entries
  * **mapping**: dictionary/hash table/associative array
  * Note that YAML also includes nodes which specify the data type structure.
    * TODO ???
* **Serialization**:
  * The Represenation Node Graph will be converted to a YAML serialization tree: stream of bytes.
* **Presentation**:
  * The final output of YAML serialization: events -> characters.
  * It represents a character stream in a human friendly manner.
* **Parsing**:
  * Inverse process of presentation: characters -> events.
  * This process needs a well-formed input - otherwise, the parsing procedure will fail.
  * YAML Lint: online parser for YAML
    * [http://www.yamllint.com/]


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
yaml.load("Quick brown fox", Loader=yaml.Loader)  # -> string
yaml.load("3.14")           # -> float
yaml.load("""
    - eggs
    - ham
    - ...
    """)                    # -> list of strings
```
* for specific Python objects, you can use the indicator `!!python/...`, e.g. `!!python/tuple`
  * e.g. full example
  ```yaml
  ? !!python/tuple [0,0]
  : The Hero
  ? !!python/tuple [0,1]
  : Treasure
  ? !!python/tuple [1,0]
  : Treasure
  ? !!python/tuple [1,1]
  : The Dragon
  ```
  -> Python: `{(0, 1): 'Treasure', (1, 0): 'Treasure', (0, 0): 'The Hero', (1, 1): 'The Dragon'}`


# Similar serialization formats

* JSON
  * YAML and JSON formats are considered to be highly compatible. 
  * YAML has many additional features lacking in JSON, including comments, extensible data types, relational anchors, strings without quotation marks, and mapping types preserving key order.
* TOML
  * TOML was designed for configuration files.
* XML
  * YAML has no notion of tag attributes as available in XML.

# Further tools

* browser-based comparison of two yaml files: https://yamldiff.com/

# Further notes

* Since there is not always an explicit terminator signal of a structure, double-check the validity of the content.