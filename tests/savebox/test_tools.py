# -*- coding: utf-8 -*-
"""
Test script for mypybox/plotbox/tools.py

Notes
-----
Developed for Python 3.6.1
@author: d-bouvier (bouvierdamien@gmail.com)
"""

#==============================================================================
# Importations
#==============================================================================

import unittest
import os
import mypybox.savebox as savebox


#==============================================================================
# Global variables
#==============================================================================

FILE_PATH = os.path.abspath(__file__)
FILE_FOLDER = os.path.dirname(FILE_PATH)


#==============================================================================
# Test Class
#==============================================================================

class CheckPathTestCase(unittest.TestCase):

    def setUp(self):
        self.old_cwd = os.getcwd()
        os.chdir(FILE_FOLDER)
        self.cwd = os.getcwd()

        self.inputs = {self.cwd: None,
                       os.path.join(self.cwd, 'folder'): 'folder',
                       os.path.join(self.cwd, 'hierarchal_folder', 'test'):
                       ['hierarchal_folder', 'test']}
        self.folders2delete = [os.path.join(self.cwd, 'folder'),
                               os.path.join(self.cwd, 'hierarchal_folder')]

    def test_returns_a_string(self):
        for path, input_val in self.inputs.items():
            with self.subTest(i=path):
                self.assertIsInstance(savebox._check_path(input_val), str)

    def test_returned_path_is_absolute(self):
        for path, input_val in self.inputs.items():
            with self.subTest(i=path):
                self.assertTrue(os.path.isabs(savebox._check_path(input_val)))

    def test_returned_path_is_valid(self):
        for path, input_val in self.inputs.items():
            with self.subTest(i=path):
                result = savebox._check_path(input_val)
                self.assertEqual(os.path.abspath(result), path)

    def test_folder_exists(self):
        for path, input_val in self.inputs.items():
            with self.subTest(i=path):
                self.assertTrue(os.path.isdir(savebox._check_path(input_val)))

    def tearDown(self):
        for path in self.inputs.keys():
            if os.path.isdir(path) and (path != FILE_FOLDER):
                os.removedirs(path)
        os.chdir(self.old_cwd)


#==============================================================================
# Main script
#==============================================================================

if __name__ == '__main__':
    """
    Main script for testing.
    """

    unittest.main()
