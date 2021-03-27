from xonsh.contexts import Block

class RunInXonshDocker(Block):
    """Run xonsh codeblock in the xonsh docker container."""

    def __init__(self, image='xonsh/xonsh:slim'):
       self.docker_image = image

    def __exit__(self, *a, **kw):
        cmd = f"docker run -it --rm {self.docker_image} /usr/local/bin/xonsh -c {repr(self.macro_block)}"
        __xonsh__.builtins.execx(cmd, 'exec', __xonsh__.ctx, filename='xontrib-macro-lib-docker-run-in-xonsh-docker')


