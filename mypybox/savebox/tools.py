# -*- coding: utf-8 -*-
"""
Toools for managing paths.

Functions
---------
_check_path :
    Returns the absolute path corresponding to ``path`` and creates folders.

Notes
-----
@author: bouvier (bouvier@ircam.fr)
         Damien Bouvier, IRCAM, Paris

Last modified on 13 Nov. 2017
Developed for Python 3.6.1
"""

#==============================================================================
# Importations
#==============================================================================

import os
import warnings


#==============================================================================
# Functions
#==============================================================================

def _check_path(path=None):
    """
    Returns the absolute path corresponding to ``path`` and creates folders.

    Parameters
    ----------
    path : None, str or list(str)
        Absolute path or subfolder hierarchy that will be created and returned.
        If None, os.getcwd() is used.
    """

    if path is None:
        return os.getcwd()
    if isinstance(path, str):
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
    elif isinstance(path, list):
        abs_path = ''
        for partial_path in path:
            abs_path = _check_path(os.path.join(abs_path, partial_path))
        return abs_path
    else:
        message = 'Variable ``path`` is neither a string or a list of string.'
        warnings.warn(message, UserWarning)
