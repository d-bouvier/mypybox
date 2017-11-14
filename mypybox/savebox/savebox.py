# -*- coding: utf-8 -*-
"""
Tooolbox for saving data and figures.

Functions
---------
save_data :
    Save data using either pickle or one of numpy's save function.
load_data :
    Load data using either pickle or numpy's load function.
save_figure :
    Save figure using matplotlib.
save_animation :
    Save animation using matplotlib.

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
import pickle
import numpy as np
from .tools import _check_path


#==============================================================================
# Global variables
#==============================================================================

_numpy_binary_extension = '.npy'
_numpy_extension = '.npz'
_pickle_extension = ''
_save_modes = {'pickle': _pickle_extension,
               'npy': _numpy_binary_extension,
               'npz': _numpy_extension,
               'comp-npz': _numpy_extension}
_figure_default_extension = '.png'
_animation_default_extension = '.mp4'


#==============================================================================
# Functions
#==============================================================================

def save_data(data, name, path=None, mode='pickle'):
    """
    Save data using either pickle or one of numpy's save function.

    Parameters
    ----------
    data: dict(str: all_types) or numpy.ndarray
        Dictionary of data to save.
    name: str
        Name of file to create.
    path: None, str or list(str), optional (default=None)
        Absolute path or subfolder hierarchy where the file will be created.
        If None, os.getcwd() is used.
    mode: {'pickle', 'npy', 'npz', 'comp-npz'}, optional (default='pickle')
        Mode used for saving data.

    Returns
    -------
    full_path: str
        Full absolute path of the saved file.
    """

    def raise_error():
        raise TypeError("Wrong data type when using saving mode", mode,
                        "(given type is {})".format(type(data)))

    full_path = os.path.join(_check_path(path), name)

    if mode == 'pickle':
        if not isinstance(data, dict):
            raise_error()
        full_path += _pickle_extension
        with open(full_path, 'wb') as file:
            pickle.dump(data, file)

    elif mode == 'npy':
        if not isinstance(data, np.ndarray):
            raise_error()
        full_path += _numpy_binary_extension
        np.save(full_path, data)

    elif mode in {'npz', 'comp-npz'}:
        if not isinstance(data, dict):
            if not isinstance(data, np.ndarray):
                raise_error()
            else:
                data = {'arr1': data}
        elif not all([isinstance(val, np.ndarray) for val in data.values()]):
            raise_error()
        full_path += _numpy_extension
        if mode == 'npz':
            np.savez(full_path, **data)
        else:
            np.savez_compressed(full_path, **data)

    return full_path


def load_data(name, path=None):
    """
    Load data using either pickle or numpy's load function.

    Parameters
    ----------
    name: str
        Name of file to load.
    path: None, str or list(str), optional (default=None)
        Absolute path or subfolder hierarchy where the file is located.
        If None, os.getcwd() is used.

    Returns
    -------
    data:
        Stored data in file specified by ``name`` and ``path``.
    """

    basename, ext = os.path.splitext(name)
    full_path = os.path.join(_check_path(path), basename)

    is_numpy_binary = os.path.isfile(full_path + _numpy_binary_extension)
    is_numpy = os.path.isfile(full_path + _numpy_extension)
    is_pickle = os.path.isfile(full_path + _pickle_extension)
    version = [is_numpy_binary, is_numpy, is_pickle]

    if version.count(True) == 0:
        raise OSError(2, 'No such file', name)
    elif version.count(True) == 1:
        if is_numpy_binary:
            return np.load(full_path + _numpy_binary_extension)
        if is_numpy:
            return np.load(full_path + _numpy_extension)
        if is_pickle:
            with open(full_path + _pickle_extension, 'rb') as file:
                return pickle.load(file)
    else:
        list_extensions = []
        if is_numpy_binary:
            list_extensions.append(_numpy_binary_extension)
        if is_numpy:
            list_extensions.append(_numpy_extension)
        if is_pickle:
            list_extensions.append(_pickle_extension)
        message = 'Several files {} were found with different extensions ' + \
                  str(list_extensions) + ', no file was loaded.'
        warnings.warn(message.format(name), UserWarning)


def save_figure(handle_figure, name, path=None, **args):
    """
    Save figure using matplotlib.

    Parameters
    ----------
    handle_figure :
        Handle of the figure to save.
    name : str
        Name of file to load.
    path: None, str or list(str), optional (default=None)
        Absolute path or subfolder hierarchy where the figure will be created.
        If None, os.getcwd() is used.
    **args : optional
        Optional keyword arguments passed to the figure's savefig() function.
    """

    _, ext = os.path.splitext(name)
    full_path = os.path.join(_check_path(path), name)

    if ext == '':
        full_path += _figure_default_extension

    handle_figure.savefig(full_path, bbox_inches='tight', **args)


def save_animation(handle_animation, name, path=None, fps=None, **args):
    """
    Save animation using matplotlib.

    Parameters
    ----------
    handle_animation :
        Handle of the animation to save.
    name : str
        Name of file to load.
    path: None, str or list(str), optional (default=None)
        Absolute path or subfolder hierarchy where the figure will be created.
        If None, os.getcwd() is used.
    **args : optional
        Optional keyword arguments passed to the animation's save() function.
    """

    _, ext = os.path.splitext(name)
    full_path = os.path.join(_check_path(path), name)

    if ext == '':
        full_path += _animation_default_extension
    handle_animation.save(full_path, fps=fps, **args)
