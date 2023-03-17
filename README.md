<p align="center">
Library of the useful <a href="https://xon.sh/tutorial_macros.html">macros</a> for the <a href="https://xon.sh/">xonsh shell</a>.
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Nice%20xontrib%20for%20the%20xonsh%20shell!&url=https://github.com/anki-code/xontrib-macro-lib" target="_blank">tweet</a>.
</p>


## Installation

To install use pip:

```bash
xpip install xontrib-macro-lib
# or: xpip install -U git+https://github.com/anki-code/xontrib-macro-lib
```

## Macro list

### RunOnce

Run the code once and save mark about it in [XONSH_DATA_DIR](https://xon.sh/envvars.html#xonsh-data-dir). 
In the next run the code will not be executed if it was not changed. If the code will be changed it will be executed again.

Example:
```python
from xontrib.macro_lib.run_once import RunOnce

with! RunOnce('First install'):
    if $(which pacman):
        pacman -S vim htop
    elif $(which apt):
        apt update && apt install -y vim htop
```

### RunInDocker

```xsh
from xontrib.macro_lib.docker import RunInDocker as docker

with! docker():  # default: image='ubuntu', executor='bash'
    echo hello

# hello
```

### RunInXonshDocker

```python
from xontrib.macro_lib.docker import RunInXonshDocker as Doxer

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

### JsonBlock

```python
from xontrib.macro_lib.data import JsonBlock

with! JsonBlock() as j:
    {
        "hello": "world"
    }

j['hello']
# 'world'
```

### Block (xonsh builtin)
```python
from xonsh.contexts import Block
with! Block() as b:
    qwe
    asd
    zxc

b.macro_block
# 'qwe\nasd\nzxc\n\n'
b.lines
# ['qwe', 'asd', 'zxc', '']
```

## Known issues

Context Manager Macros pick up comments from outside the block ([4207](https://github.com/xonsh/xonsh/issues/4207)). We can fix it in the xontrib by checking the indentation in the beginning line and the end line. PR is welcome!

## Credits

This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
