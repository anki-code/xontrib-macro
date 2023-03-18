"""Library of the useful macro for the xonsh shell."""

from xonsh.built_ins import XonshSession

def _load_xontrib_(xsh: XonshSession, **kwargs) -> dict:
    import xontrib.macrolib as macrolib
    import xontrib.macrolib.data
    import xontrib.macrolib.docker
    import xontrib.macrolib.run
    return {'macrolib': macrolib}
