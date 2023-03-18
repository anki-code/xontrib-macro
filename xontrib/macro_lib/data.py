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

    filepath: str           # Path to file.
    mode: str = 'w'         # Open mode: 'w' (write), 'a' (append). Doc: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
    makedir: bool = False   # Force create missing directories in path.
    replace: bool = False   # Replace if the file exists.
    chmod: int = None       # Set file permissions. Doc: https://docs.python.org/3/library/pathlib.html#pathlib.Path.chmod
    exec: str = None        # Set execute to 'a' (all), 'u' (user), 'g' (group), 'o' (others). Can be 'uo' and the same as `chmod uo+x file`.
    user: str = None        # Set user for a file.
    group: str = None       # Set group for a file.
    verbose: bool = False   # Print info about actions.
    shebang: bool = False

    def log(self, msg):
        if self.verbose:
            print(msg, file=sys.stderr)

    def nice_st_mode(self, st_mode):
        return ' '.join(list(map(''.join, zip(*[iter(stat.filemode(st_mode)[1:])]*3))))

    def __enter__(self):
        fp = Path(self.filepath)

        if not self.replace and fp.exists():
            raise Exception(f'File exists: {fp}')

        if self.makedir and not fp.parent.exists():
            self.log(f'Make directories: {fp.parent}')
            fp.parent.mkdir(parents=True)

        self.log(f'Write to file: {fp}')
        with open(fp, self.mode) as f:
            f.write(self.macro_block.strip()+'\n')

        if self.chmod is not None:
            self.log(f'Set chmod: {self.nice_st_mode(self.chmod)}')
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
            self.log(f'Set exec:  {self.nice_st_mode(st_mode)}')
            os.chmod(self.filepath, st_mode)

        if self.user:
            self.log(f'Set user: {self.user}')
            shutil.chown(self.filepath, user=self.user)

        if self.group:
            self.log(f'Set group: {self.group}')
            shutil.chown(self.filepath, group=self.group)


    def __exit__(self, *exc):
        del self.macro_block, self.macro_globals, self.macro_locals


class JsonBlock(Block):
    """Macro block class to read json."""
    __xonsh_block__ = str

    def __enter__(self):
        return json.loads(self.macro_block)

    def __exit__(self, *exc):
        del self.macro_block, self.macro_globals, self.macro_locals
