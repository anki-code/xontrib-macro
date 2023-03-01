from contextlib import contextmanager

@contextmanager
def chdir(adir):
    old_dir = os.getcwd()
    os.chdir(adir)
    yield
    os.chdir(old_dir)
