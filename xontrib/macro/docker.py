from xonsh.contexts import Block

class RunInDocker(Block):
    """Run codeblock in docker container."""
    
    def __init__(self, image='ubuntu', executor='bash'):
        """
        Parameters
        ----------
            image : str
                The docker image name. Default: ubuntu
            executor : str
                The path to executor. Default: bash 
        """        
        self.docker_image = image
        self.docker_executor = executor

    def __exit__(self, *a, **kw):
        cmd = f"docker run -it --rm {self.docker_image} {self.docker_executor} -c {repr(self.macro_block)}"
        __xonsh__.builtins.execx(cmd, 'exec', __xonsh__.ctx, filename='xontrib-macro-docker-run-in-docker')

    

class RunInXonshDocker(RunInDocker):
    """Run xonsh codeblock in the xonsh docker container."""

    def __init__(self, image='xonsh/xonsh:slim', executor='/usr/local/bin/xonsh'):
        super().__init__(image, executor)
