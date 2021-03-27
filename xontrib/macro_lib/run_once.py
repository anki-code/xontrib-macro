import sys

from xonsh.contexts import Block
from hashlib import md5
from pathlib import Path

class RunOnce(Block):
    """Run xonsh codeblock only once and save the mark about it to the $XONSH_DATA_DIR."""

    def __init__(self, name='', print_done=False):
        self.name = name
        self.print_done = print_done

    def printe(self, msg):
        print(msg, file=sys.stderr)

    def __exit__(self, *a, **kw):
        data_dir = __xonsh__.env.get('XONSH_DATA_DIR')
        code_md5 =  md5(self.macro_block.encode()).hexdigest()
        filename = f'xonsh_run_once_{code_md5}.txt'
        filepath = Path(data_dir) / filename
        self.name = code_md5 if not self.name else self.name

        if filepath.exists():
            if __xonsh__.env.get('XONTRIB_RUN_ONCE_DEBUG', False):
                self.printe(f'xontrib-run-once: Skip running code block "{self.name}"')
                self.printe(f'xontrib-run-once: Already completed: {filepath}')
        else:
            if __xonsh__.env.get('XONTRIB_RUN_ONCE_DEBUG', False):
                self.printe(f'xontrib-run-once: Running code block "{self.name}"')

            __xonsh__.builtins.execx(self.macro_block, 'exec', __xonsh__.ctx, filename=filename)

            with open(filepath, 'w') as f:
                print(code_md5, file=f)

            if __xonsh__.env.get('XONTRIB_RUN_ONCE_DEBUG', False):
                self.printe(f'xontrib-run-once: Save mark to {filepath}')

            if self.print_done:
                self.printe(f"xontrib-run-once: Done '{self.name}'")