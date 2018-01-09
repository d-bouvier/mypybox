# -*- coding: utf-8 -*-
"""
Test script for mypybox/utilities/log.py

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
import unittest
import mypybox.utilities as utilities


#==============================================================================
# Test Class
#==============================================================================

class LoggerTestCase(unittest.TestCase):

    def test_redirecting_stdout(self):
        utilities.duplicate_stdout_stream_to_file('file', mode='w',
                                                    record_errors=False)
        self.assertIsInstance(sys.stdout, utilities.Logger)
        self.assertNotIsInstance(sys.stderr, utilities.Logger)

        utilities.suppress_stdout_stream_to_file()
        self.assertNotIsInstance(sys.stdout, utilities.Logger)
        self.assertNotIsInstance(sys.stderr, utilities.Logger)

    def test_redirecting_stdout_and_stderr(self):

        utilities.duplicate_stdout_stream_to_file('file', mode='w')
        self.assertIsInstance(sys.stdout, utilities.Logger)
        self.assertIsInstance(sys.stderr, utilities.Logger)

        utilities.suppress_stdout_stream_to_file()
        self.assertNotIsInstance(sys.stdout, utilities.Logger)
        self.assertNotIsInstance(sys.stderr, utilities.Logger)

    def tearDown(self):
        os.remove('file.log')


class MakeHeaderTestCase(unittest.TestCase):

    def test_return_string(self):
        self.assertIsInstance(utilities.make_header(), str)


#==============================================================================
# Main script
#==============================================================================

if __name__ == '__main__':
    """
    Main script for testing.
    """

    unittest.main()
