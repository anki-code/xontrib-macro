# THIS IS DRAFT WITH ISSUE - https://github.com/xonsh/xonsh/issues/5005

import types
from xonsh.contexts import Block
from textwrap import indent
from xonsh.built_ins import XSH

class Alias(Block):
    """Register alias."""

    def __init__(self, name):
       self.alias_name = name

    def __exit__(self, *a, **kw):
        fn_str = 'def _a(args):\n' + indent(self.macro_block, '    ')
        code_obj = XSH.builtins.compilex(fn_str, filename=f'<xonsh-alias-{self.alias_name}>', mode='exec', glbs=XSH.ctx)
        fn = types.FunctionType(code_obj.co_consts[0], globals())  # https://stackoverflow.com/a/57804755
        aliases[self.alias_name] = fn

# with! Alias('e1'):
#     print('e', end='')
#     echo 1
#
# e1
