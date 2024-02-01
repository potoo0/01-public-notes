# overwrite built-in function
# global: site.getsitepackages() -> sitecustomize.py
# user:   site.getsitepackages() -> usercustomize.py

_print = print


def print(*args, **kwargs):
    if 'flush' not in kwargs:
        kwargs['flush'] = True
    _print(*args, **kwargs)
