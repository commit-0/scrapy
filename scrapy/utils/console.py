from functools import wraps

def _embed_ipython_shell(namespace={}, banner=''):
    """Start an IPython Shell"""
    pass

def _embed_bpython_shell(namespace={}, banner=''):
    """Start a bpython shell"""
    pass

def _embed_ptpython_shell(namespace={}, banner=''):
    """Start a ptpython shell"""
    pass

def _embed_standard_shell(namespace={}, banner=''):
    """Start a standard python shell"""
    pass
DEFAULT_PYTHON_SHELLS = {'ptpython': _embed_ptpython_shell, 'ipython': _embed_ipython_shell, 'bpython': _embed_bpython_shell, 'python': _embed_standard_shell}

def get_shell_embed_func(shells=None, known_shells=None):
    """Return the first acceptable shell-embed function
    from a given list of shell names.
    """
    pass

def start_python_console(namespace=None, banner='', shells=None):
    """Start Python console bound to the given namespace.
    Readline support and tab completion will be used on Unix, if available.
    """
    pass