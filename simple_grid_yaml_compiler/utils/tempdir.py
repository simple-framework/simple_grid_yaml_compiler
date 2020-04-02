import contextlib
import shutil
import tempfile


@contextlib.contextmanager
def tempdir():
    try:
        dirpath = tempfile.mkdtemp()
        tempfile.tempdir = dirpath
        yield dirpath
    finally:
        tempfile.tempdir = None
        shutil.rmtree(dirpath)