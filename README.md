<p align="center">
Library of the useful <a href="https://xon.sh/tutorial_macros.html">macros</a> for the <a href="https://xon.sh/">xonsh shell</a>.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/anki-code/xontrib-macro" target="_blank">tweet</a>.
</p>


## Installation

To install use pip:

```bash
xpip install xontrib-macro
# or: xpip install -U git+https://github.com/anki-code/xontrib-macro
```

## Usage

By loading the whole module - recommended for interactive usage (type `macro.<Tab>`): 
```xsh
xontrib load macro
with! macro.data.Write('/tmp/hello', replace=True):  # more macros below
    world
```

By importing certain macro - recommended for scripts:
```xsh
from xontrib.macro.data import Write
with! Write('/tmp/hello', replace=True):  # more macros below
    world
```

## Macros

### Block (xonsh builtin)
```python
from xonsh.contexts import Block

with! Block() as b:
    any
    text
    here

b.macro_block
# 'any\ntext\nhere\n\n'
b.lines
# ['any', 'text', 'here', '']
```

### data.Write

Write a file from block ([rich list of parameters](https://github.com/anki-code/xontrib-macro/blob/main/xontrib/macro/data.py#L12)):

```xsh
from xontrib.macro.data import Write

with! Write('/tmp/t/hello.xsh', chmod=0o700, replace=True, makedir=True, format={'name': 'world'}, verbose=True):
    echo {name}
    
## Make directories: /tmp/t
## Write to file: /tmp/t/hello.xsh
## Set chmod: rw- --- ---
## Set exec:  rwx --- ---

/tmp/t/hello.xsh
# world
```
There is also `data.Replace()` macro with `mode='w', replace=True, makedir=True, replace_keep='a'`.

Note! There is an upstream issue described below in "Known issues" section - the first lines that begin from `#` will be ignored in the block. As workaround to create [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) use `Write(..., shebang="#!/bin/xonsh")`.

### data.JsonBlock

Make json block and use it as dict:

```python
from xontrib.macro.data import JsonBlock

with! JsonBlock() as j:
    {"hello": "world"}

j['hello']
# 'world'
```

### data.XmlBlock

Simple XML macro context manager from [xonsh macro tutorial](https://xon.sh/tutorial_macros.html#context-manager-macros). This will return the parsed XML tree from a macro block

```xsh
from xontrib.macro.data import XmlBlock

with! XmlBlock() as tree:
    <note>
      <heading>Hello world!</heading>
      <body>
        Hello!
      </body>
    </note>

type(tree)
# xml.etree.ElementTree.Element

tree.find('body').text
# '\n    Hello!\n  '

```

### run.Once

Run the code once and save mark about it in [XONSH_DATA_DIR](https://xon.sh/envvars.html#xonsh-data-dir). 
In the next run the code will not be executed if it was not changed. If the code will be changed it will be executed again.

Example:
```python
from xontrib.macro.run import Once

with! Once('First install'):
    if $(which pacman):
        pacman -S vim htop
    elif $(which apt):
        apt update && apt install -y vim htop
```

### docker.RunInDocker

```xsh
from xontrib.macro.docker import RunInDocker as docker

with! docker():  # default: image='ubuntu', executor='bash'
    echo hello

# hello
```

### docker.RunInXonshDocker

```python
from xontrib.macro.docker import RunInXonshDocker as Doxer

with! Doxer():  # default: image='xonsh/xonsh:slim', executor='/usr/local/bin/xonsh'
   echo Installing...
   pip install -U -q pip lolcat
   echo "We are in docker container now!" | lolcat
   
# We are in docker container now! (colorized)
```

This is the same as:
```python
docker run -it --rm xonsh/xonsh:slim xonsh -c @("""
pip install -U -q pip lolcat
echo "We are in docker container now!" | lolcat
""")
```

## Known issues

Context Manager Macro picks up comments from outside the block and ignore the initial comments in the block ([4207](https://github.com/xonsh/xonsh/issues/4207)). We can fix it in the xontrib by checking the indentation in the beginning line and the end line. PR is welcome!

## Credits

This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
