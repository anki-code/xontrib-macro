"""Library of the useful macro for the xonsh shell."""

def _load_xontrib_(*args, **kwargs) -> dict:
    import xontrib.macrolib as macrolib
    import xontrib.macrolib.data
    import xontrib.macrolib.docker
    import xontrib.macrolib.run
    return {'macrolib': macrolib}
