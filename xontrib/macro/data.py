import os
import sys
import stat
import json
import shutil

from dataclasses import dataclass
from pathlib import Path
from xonsh.contexts import Block

@dataclass
class Write(Block):
    """Macro block class to write a file."""

    filepath: str              # Path to file.
    mode: str = 'w'            # Open mode: 'w' (write), 'a' (append). Doc: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
    makedir: bool = False      # Force create missing directories in path.
    replace: bool = False      # Replace if the file exists.
    replace_keep: str = None   # Keep after replace: 'm' (chmod), 'u' (user), 'g' (group), 'a' (all). Allowed mix: 'mu'.
    chmod: int = None          # Set file permissions i.e `0o644`. Doc: https://docs.python.org/3/library/pathlib.html#pathlib.Path.chmod
    exec: str = None           # Set execute rights to 'u' (user), 'g' (group), 'o' (others). Can be 'uo' (user+others) and the same as `chmod uo+x file`.
    user: str = None           # Set user for a file.
    group: str = None          # Set group for a file.
    format: dict = None        # Format block text using `str.format(**format)`.
    verbose: bool = False      # Print info about actions.
    shebang: str = None        # Put here the shebang. It's workaround for https://github.com/xonsh/xonsh/issues/4207

    def log(self, msg):
        if self.verbose:
            print(msg, file=sys.stderr)

    @staticmethod
    def nice_st_mode(st_mode):
        """Return st_mode as space delimited text i.e. `nice_st_mode(0o644)` -> 'rw- r-- r--'"""
        return ' '.join(list(map(''.join, zip(*[iter(stat.filemode(st_mode)[1:])]*3))))

    def __enter__(self):
        fp = Path(self.filepath).expanduser()

        replaced, prev_st_mode, prev_user, prev_group = False, None, None, None
        if fp.exists():
            if self.replace:
                if self.replace_keep and (self.chmod or self.exec or self.user or self.group):
                    self.log('File will be replaced using `replace_keep` strategy then `chmod`, `exec`, `user` or `group` will be set as requested.')

                self.log(f'Remove file before writing: {fp}')
                replaced, prev_st_mode, prev_user, prev_group = True, fp.stat().st_mode, fp.owner(), fp.group()
                fp.unlink()
            else:
                raise Exception(f'File exists: {fp}')

        if self.makedir and not fp.parent.exists():
            self.log(f'Make directories: {fp.parent}')
            fp.parent.mkdir(parents=True)


        self.log(f'Write to file: {fp}')
        with open(fp, self.mode) as f:
            macro_block = self.macro_block.strip()
            macro_block = macro_block.format(**self.format) if self.format is not None else macro_block
            f.write((self.shebang.strip() + '\n' if self.shebang is not None else '') + macro_block + '\n')


        if self.replace_keep in ['m', 'a']:
            self.log(f'Keep mode: {self.nice_st_mode(prev_st_mode)}')
            fp.chmod(prev_st_mode)

        if self.replace_keep in ['u', 'a']:
            self.log(f'Keep user: {prev_user}')
            shutil.chown(self.filepath, user=prev_user)

        if self.replace_keep in ['g', 'a']:
            self.log(f'Keep group: {prev_group}')
            shutil.chown(self.filepath, group=prev_group)


        if self.chmod is not None:
            self.log(f'Set mode: {self.nice_st_mode(self.chmod)}')
            fp.chmod(self.chmod)

        if self.exec is not None:
            st_mode = os.stat(self.filepath).st_mode
            if self.exec == 'a':
                self.exec = 'ugo'
            if 'u' in self.exec:
                st_mode |= stat.S_IXUSR
            if 'g' in self.exec:
                st_mode |= stat.S_IXGRP
            if 'o' in self.exec:
                st_mode |= stat.S_IXOTH
            self.log(f'Set exec: {self.nice_st_mode(st_mode)}')
            os.chmod(self.filepath, st_mode)

        if self.user:
            self.log(f'Set user: {self.user}')
            shutil.chown(self.filepath, user=self.user)

        if self.group:
            self.log(f'Set group: {self.group}')
            shutil.chown(self.filepath, group=self.group)

    def __exit__(self, *exc):
        del self.macro_block, self.macro_globals, self.macro_locals

@dataclass
class Replace(Write):
    """Macro block class to force replace the file."""
    mode: str = 'w'
    replace: bool = True
    makedir: bool = True
    replace_keep: str = 'a'


class JsonBlock(Block):
    """Macro block class to read json."""
    __xonsh_block__ = str

    def __enter__(self):
        return json.loads(self.macro_block)

    def __exit__(self, *exc):
        del self.macro_block, self.macro_globals, self.macro_locals

        
# Source: https://xon.sh/tutorial_macros.html#context-manager-macros
import xml.etree.ElementTree as ET
class XmlBlock:
    """Macro block class to read XML."""
    
    # make sure the macro_block comes back as a string
    __xonsh_block__ = str

    def __enter__(self):
        # parse and return the block on entry
        root = ET.fromstring(self.macro_block)
        return root

    def __exit__(self, *exc):
        # no reason to keep these attributes around.
        del self.macro_block, self.macro_globals, self.macro_locals
        
        
