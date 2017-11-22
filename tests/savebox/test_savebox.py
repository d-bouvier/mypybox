# -*- coding: utf-8 -*-
"""
Test script for mypybox/savebox/savebox.py

Notes
-----
@author: bouvier (bouvier@ircam.fr)
         Damien Bouvier, IRCAM, Paris

Last modified on 22 Nov. 2017
Developed for Python 3.6.1
"""

#==============================================================================
# Importations
#==============================================================================

import os
import unittest
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mypybox.savebox as savebox


#==============================================================================
# Global variables
#==============================================================================

FILE_PATH = os.path.abspath(__file__)
FILE_FOLDER = os.path.dirname(FILE_PATH)


#==============================================================================
# Test Class
#==============================================================================

class SaveDataTestCase(unittest.TestCase):

    def setUp(self):
        self.old_cwd, self.cwd = global_setUp()
        a = np.zeros((3, 2))
        b = np.ones((3, 2))
        self.input_var = dict()
        for mode, ext in savebox._save_modes.items():
            self.input_var[mode] = {'name': 'test_save_' + mode, 'ext': ext}
            if mode == 'pickle':
                self.input_var[mode]['data_correct'] = {'a': a, 'b': b}
                self.input_var[mode]['data_wrong'] = a
            elif mode == 'npy':
                self.input_var[mode]['data_correct'] = a
                self.input_var[mode]['data_wrong'] = {'a': a, 'b': b}
            elif mode in {'npz', 'comp-npz'}:
                self.input_var[mode]['data_correct'] = {'a': a, 'b': b}
                self.input_var[mode]['data_wrong'] = {'a': 'a', 'b': b}

    def test_returned_path_exists(self):
        for mode, input_val in self.input_var.items():
            with self.subTest(i=mode):
                result = savebox.save_data(input_val['data_correct'],
                                           input_val['name'], mode=mode)
                self.input_var[mode]['path'] = result
                self.assertTrue(os.path.isfile(result))

    def test_returned_path_has_correct_extension(self):
        for mode, input_val in self.input_var.items():
            with self.subTest(i=mode):
                result = savebox.save_data(input_val['data_correct'],
                                           input_val['name'], mode=mode)
                _, ext = os.path.splitext(result)
                self.input_var[mode]['path'] = result
                self.assertEqual(ext, input_val['ext'])

    def test_error_raised_if_wrong_mode(self):
        for mode, input_val in self.input_var.items():
            with self.subTest(i=mode):
                self.assertRaises(TypeError, savebox.save_data,
                                  input_val['data_wrong'], input_val['name'],
                                  mode=mode)

    def tearDown(self):
        for values in self.input_var.values():
            path = values.get('path', '')
            check_and_suppress(path)
        global_tearDown(self.old_cwd)


class LoadDataTestCase(unittest.TestCase):

    def setUp(self):
        self.old_cwd, self.cwd = global_setUp()
        a = np.zeros((3, 2))
        b = np.ones((3, 2))
        self.vars = dict()
        for mode, ext in savebox._save_modes.items():
            if mode == 'pickle':
                data = {'a': a, 'b': b}
            elif mode == 'npy':
                data = a
            elif mode in {'npz', 'comp-npz'}:
                data = {'a': a, 'b': b}
            path = savebox.save_data(data, 'test_load_' + mode, mode=mode)
            self.vars[mode] = path

    def test_loaded_data_has_correct_type(self):
        for mode, path in self.vars.items():
            with self.subTest(i=mode):
                data = savebox.load_data(path)
                if mode == 'pickle':
                    self.assertIsInstance(data, dict)
                elif mode == 'npy':
                    self.assertIsInstance(data, np.ndarray)
                elif mode in {'npz', 'comp-npz'}:
                    self.assertIsInstance(data, np.lib.npyio.NpzFile)

    def tearDown(self):
        for path in self.vars.values():
            check_and_suppress(path)
        global_tearDown(self.old_cwd)


class SaveFigureTestCase(unittest.TestCase):

    def setUp(self):
        self.old_cwd, self.cwd = global_setUp()
        self.name_figs = []
        for case in ['default', 'png', 'pdf']:
            name = 'test_save_fig_' + case
            if case != 'default':
                name += '.' + case
            handle = plt.figure('Figure ' + case)
            savebox.save_figure(handle, name)
            plt.close(handle)
            if case == 'default':
                name += savebox._figure_default_extension
            self.name_figs.append(name)

    def test_file_was_created(self):
        for i, name in enumerate(self.name_figs):
            with self.subTest(i=i):
                self.assertTrue(os.path.isfile(name))

    def tearDown(self):
        for name in self.name_figs:
            path = os.path.abspath(name)
            check_and_suppress(path)
        global_tearDown(self.old_cwd)


class SaveAnimationTestCase(unittest.TestCase):

    def setUp(self):
        self.old_cwd, self.cwd = global_setUp()
        self.name_anims = []
        for case in ['default', 'mp4', 'avi']:
            name = 'test_save_fig_' + case
            if case != 'default':
                name += '.' + case
            handle_anim, handle_fig = create_anim(name)
            savebox.save_animation(handle_anim, name)
            plt.close(handle_fig)
            if case == 'default':
                name += savebox._animation_default_extension
            self.name_anims.append(name)

    def test_file_was_created(self):
        for i, name in enumerate(self.name_anims):
            with self.subTest(i=i):
                self.assertTrue(os.path.isfile(name))

    def tearDown(self):
        for name in self.name_anims:
            path = os.path.abspath(name)
            check_and_suppress(path)
        global_tearDown(self.old_cwd)


#==============================================================================
# Functions
#==============================================================================

def global_setUp():
    old_cwd = os.getcwd()
    os.chdir(FILE_FOLDER)
    return old_cwd, os.getcwd()


def check_and_suppress(path):
    if os.path.isfile(path) and (path != FILE_FOLDER):
        os.remove(path)


def global_tearDown(old_cwd):
    os.chdir(old_cwd)


def create_anim(name):
    handle_fig = plt.figure('Animation ' + name)
    ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
    line, = ax.plot([], [], lw=2)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        x = np.linspace(0, 2, 10)
        line.set_data(x, np.sin(2 * np.pi * (x - 0.01 * i)))
        return line,

    handle_anim = animation.FuncAnimation(handle_fig, animate,
                                          init_func=init, frames=20)
    return handle_anim, handle_fig


#==============================================================================
# Main script
#==============================================================================

if __name__ == '__main__':
    """
    Main script for testing.
    """

    unittest.main()
