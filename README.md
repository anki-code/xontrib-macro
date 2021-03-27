<p align="center">
Library of the useful macroses for the <a href="https://xon.sh/">xonsh shell</a>.
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

## Usage

### RunOnce

Run the code once and save mark about it in [XONSH_DATA_DIR](https://xon.sh/envvars.html#xonsh-data-dir). 
In the next run the code will not be executed if it was not changed. If the code will be changed it will be executed again.

```python
from xontrib.macro_lib.run_once import RunOnce
with! RunOnce('Just echo') as _r:
    echo 123
```

### RunInXonshDocker

```python
from xontrib.macro_lib.docker import RunInXonshDocker as Doxer
with! Doxer() as _d:
   pip install lolcat
   echo "We're in docker container now!" | lolcat
```

This is the same as:
```python
docker run -it --rm xonsh/xonsh:slim xonsh -c {code}
```

## Credits

This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).