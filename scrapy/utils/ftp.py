import posixpath
from ftplib import FTP, error_perm
from posixpath import dirname
from typing import IO

def ftp_makedirs_cwd(ftp: FTP, path: str, first_call: bool=True) -> None:
    """Set the current directory of the FTP connection given in the ``ftp``
    argument (as a ftplib.FTP object), creating all parent directories if they
    don't exist. The ftplib.FTP object must be already connected and logged in.
    """
    pass

def ftp_store_file(*, path: str, file: IO, host: str, port: int, username: str, password: str, use_active_mode: bool=False, overwrite: bool=True) -> None:
    """Opens a FTP connection with passed credentials,sets current directory
    to the directory extracted from given path, then uploads the file to server
    """
    pass