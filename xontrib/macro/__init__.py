"""Library of the useful macro for the xonsh shell."""

def _load_xontrib_(*args, **kwargs) -> dict:
    import xontrib.macro as macro
    import xontrib.macro.data
    import xontrib.macro.docker
    import xontrib.macro.run
    return {'macro': macro}
