# -*- coding: utf-8 -*-
"""
Tooolbox for creating log files.

Class
-----
Logger :
    Class for redirecting print() output to both the terminal and a file.

Functions
---------
duplicate_stdout_stream_to_file :
    Add streaming of stdout to a log file (in addition of the terminal).
suppress_stdout_stream_to_file :
    Suppress streaming of stdout to a log a file.
make_header :
    Creates a normalized header.

Notes
-----
Developed for Python 3.6.1
@author: d-bouvier (bouvierdamien@gmail.com)
"""

#==============================================================================
# Importations
#==============================================================================

import os
import sys
import time
from ..savebox.tools import _check_path


#==============================================================================
# Class
#==============================================================================

class Logger(object):
    """
    Class for redirecting print() output to both the terminal and a file.

    Parameters
    ----------
    file_path : 'str'
        Path of the file where stdout will be redirected.
    mode : {'w', 'a'}, optional (default='a')
        Writing mode when writing to file.
    """

    def __init__(self, file_path, mode='a'):
        self.terminal = sys.stdout
        self.log = open(file_path, mode)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


#==============================================================================
# Functions
#==============================================================================

def duplicate_stdout_stream_to_file(name, path=None, mode='a',
                                    record_errors=True):
    """
    Add streaming of stdout to a log file (in addition of the terminal).

    Parameters
    ----------
    name : str
        Name of file to where stdout will be redirected.
    path: None, str or list(str), optional (default=None)
        Absolute path or subfolder hierarchy where the file is located.
    mode : {'w', 'a'}, optional (default='a')
        Writing mode when writing to file.
    record_errors : boolean, optional (default=True)
        If True, stderr is also redirected to file.
    """

    abs_path = _check_path(path)
    basename, ext = os.path.splitext(name)
    if ext == '':
        ext = '.log'
    file_path = os.path.join(abs_path, basename + ext)

    sys.stdout = Logger(file_path, mode=mode)
    if record_errors:
        sys.stderr = sys.stdout


def suppress_stdout_stream_to_file():
    """
    Suppress streaming of stdout to a log a file.
    """

    if type(sys.stdout) == Logger:
        sys.stdout.log.close()
        sys.stdout = sys.stdout.terminal
    if type(sys.stderr) == Logger:
        sys.stderr.log.close()
        sys.stderr = sys.stderr.terminal


def make_header(dependencies=dict()):
    """
    Creates a normalized header.

    Parameters
    ----------
    dependencies : dict{str: str}
        Dictionnary of package dependencies linking package's name to version.
    """

    header = '{:#<79}'.format('#') + '\n'
    header += '{:#<79}'.format('#') + '\n'
    header += '\n'
    header += 'Date: ' + time.strftime('%d %b %Y %H:%M') + '\n'
    header += 'Script: ' + '{}'.format(sys.argv[0]) + '\n'
    header += 'Dependencies: '
    for package_name, package_version in dependencies.items():
        header += package_name + ' v.' + package_version + ', '
    header = header[:-2] + '\n'
    header += 'Command-line arguments: {}'.format(sys.argv[1:]) + '\n'

    return header

