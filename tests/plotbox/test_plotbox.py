# -*- coding: utf-8 -*-
"""
Test script for mypybox/plotbox/plotbox.py

Notes
-----
Developed for Python 3.6.1
@author: d-bouvier (bouvierdamien@gmail.com)
"""

#==============================================================================
# Importations
#==============================================================================

import unittest
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mypybox.plotbox as plotbox


#==============================================================================
# Test Class
#==============================================================================

class SigIOTestCase(unittest.TestCase):

    def setUp(self):
        N = 10
        self.vector = np.arange(N)
        self.sig_in = np.exp(2j * np.pi * self.vector/N)
        self.sig_out = self.vector * self.sig_in

    def test_works_correctly_and_returns_handle(self):
        for num_types in itertools.product(('real', 'complex'), repeat=2):
            with self.subTest(i=num_types):
                if num_types[0] == 'real':
                    temp_sig_in = np.real(self.sig_in)
                else:
                    temp_sig_in = self.sig_in
                if num_types[1] == 'real':
                    temp_sig_out = np.real(self.sig_out)
                else:
                    temp_sig_out = self.sig_out
                plotbox.sig_io(self.vector, temp_sig_in, temp_sig_out)
                value = plotbox.sig_io(self.vector, temp_sig_in, temp_sig_out)
                self.assertIsInstance(value, plt.Figure)


class TimeSigTestCase(unittest.TestCase):

    def setUp(self):
        N = 10
        K = 3
        self.vector = np.arange(N)
        self.mat = np.arange(K)[:, np.newaxis] * self.vector[np.newaxis, :]
        self.sig = np.exp(2j * np.pi * self.mat/N)

    def test_works_correctly_and_returns_handle(self):
        for num_type in ('real', 'complex'):
            with self.subTest(i=num_type):
                if num_type == 'real':
                    temp_sig = np.real(self.sig)
                else:
                    temp_sig = self.sig
                value = plotbox.time_sig(self.vector, temp_sig)
                self.assertIsInstance(value, plt.Figure)


class CollTestCase(unittest.TestCase):

    def setUp(self):
        N = 10
        K = 3
        self.vector = np.arange(N)
        self.mat = np.arange(K)[:, np.newaxis] * self.vector[np.newaxis, :]
        self.coll = (np.cos(2 * np.pi * self.mat/N),
                     np.sin(2 * np.pi * self.mat/N))

    def test_works_correctly_and_returns_handle(self):
        value = plotbox.coll(self.vector, self.coll)
        self.assertIsInstance(value, plt.Figure)


class SpectrogramTestCase(unittest.TestCase):

    def setUp(self):
        N = 512
        self.sig = np.cos(2 * np.pi * np.arange(N)/N)

    def test_works_correctly_and_returns_handle(self):
        value = plotbox.spectrogram(self.sig)
        self.assertIsInstance(value, plt.Figure)


class TimeKernelTestCase(unittest.TestCase):

    def setUp(self):
        self.M = 10
        self.vec = np.arange(self.M)

    def test_works_correctly_and_returns_handle(self):
        for n in [1, 2, 3]:
            with self.subTest(i=n):
                kernel = np.random.normal(size=(self.M,)*n)
                value = plotbox.time_kernel(self.vec, kernel)
                if n in {1, 2}:
                    handle_type = plt.Figure
                elif n == 3:
                    handle_type = animation.FuncAnimation
                self.assertIsInstance(value, handle_type)

    def test_error_raised_if_wrong_mode(self):
        n = 4
        kernel = np.random.normal(size=(self.M,)*n)
        self.assertRaises(ValueError, plotbox.time_kernel, self.vec, kernel)


class FreqKernelTestCase(unittest.TestCase):

    def setUp(self):
        self.M = 10
        self.vec = -np.fft.fftshift(np.arange(self.M))

    def test_works_correctly_and_returns_handle(self):
        for n in [1, 2]:
            with self.subTest(i=n):
                kernel = np.random.normal(size=(self.M,)*n)
                value = plotbox.freq_kernel(self.vec, kernel)
                self.assertIsInstance(value, plt.Figure)

    def test_error_raised_if_wrong_mode(self):
        n = 3
        kernel = np.random.normal(size=(self.M,)*n)
        self.assertRaises(ValueError, plotbox.freq_kernel, self.vec, kernel)


#==============================================================================
# Main script
#==============================================================================

if __name__ == '__main__':
    """
    Main script for testing.
    """

    unittest.main()
