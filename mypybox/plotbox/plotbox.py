# -*- coding: utf-8 -*-
"""
Toolbox for plots.

Functions
---------
sig_io :
    Plots input and output signals of a system.
time_sig :
    Plots a signal (mono or multi-dimensional).
coll :
    Plots a collection of signals.
spectrogram :
    Plots the Short-Time Fourier Transform of a signal.
time_kernel :
    Plots a discrete time kernel of order 1 or 2.
freq_kernel :
    Plots a discrete transfer kernel of order 1 or 2.

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

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
import scipy.signal as sc_sig
from ..mathbox import safe_db


#==============================================================================
# Functions
#==============================================================================

def sig_io(vec, input_sig, output_sig, title=None, xlim=[None, None],
           ylim=[None, None]):
    """
    Plots input and output signals of a system.

    Parameters
    ----------
    vec : numpy.ndarray
        Time vector.
    input_sig : numpy.ndarray
        Input signal.
    input_sig : numpy.ndarray
        Output signal.
    title : str, optional (default=None)
        Title of the Figure. If None, will be set to a default value.
    xlim : list(float), optionall (default=[None, None])
        Set the x limits of all subplots. By default autoscaling is used.
    ylim : list(float), optionall (default=[None, None])
        Set the y limits of all subplots. By default autoscaling is used.
    """

    complex_bool = 'complex' in str(input_sig.dtype) or \
                   'complex' in str(output_sig.dtype)
    nb_col = 2 if complex_bool else 1
    if title is None:
        title = 'Input and output signal of a system'

    handle = plt.figure(title)
    handle.clf()

    plt.subplot(2, nb_col, 1)
    plt.plot(vec, input_sig.real, 'b')
    plt.title('Input - Real part' if complex_bool else 'Input')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.subplot(2, nb_col, 3 if complex_bool else 2)
    plt.plot(vec, output_sig.real, 'b')
    plt.title('Output - Real part' if complex_bool else 'Output')
    plt.xlim(xlim)
    plt.ylim(ylim)
    if complex_bool:
        plt.subplot(2, nb_col, 2)
        plt.plot(vec, input_sig.imag, 'r')
        plt.title('Input - imaginary part')
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.subplot(2, nb_col, 4)
        plt.plot(vec, output_sig.imag, 'r')
        plt.title('Output - imaginary part')
        plt.xlim(xlim)
        plt.ylim(ylim)

    return handle


def time_sig(vec, signal, title=None, title_plots=None, xlim=[None, None],
             ylim=[None, None]):
    """
    Plots a signal (mono or multi-dimensional).

    Parameters
    ----------
    vec : numpy.ndarray
        Time vector.
    sig : 1-D or 2-D numpy.ndarray
        Collection of signals to plot.
    title : str, optional (default=None)
        Title of the Figure. If None, will be set to a default value.
    title_plots : list(str), optional (default=None)
        Title of each subplots. If None, will be set to a default value.
    xlim : list(float), optionall (default=[None, None])
        Set the x limits of all subplots. By default autoscaling is used.
    ylim : list(float), optionall (default=[None, None])
        Set the y limits of all subplots. By default autoscaling is used.
    """

    complex_bool = 'complex' in str(signal.dtype)

    shape = signal.shape
    assert len(shape) <= 2, 'Signal has {} dimensions,'.format(len(shape)) + \
        ' should be less or equal than 2.'
    if len(shape) == 1: # Mono-dimensional case
        nb_sig = 1
        signal.shape = (1, shape[0])
    elif len(shape) == 2: # Multi-dimensional case
        nb_sig = shape[0]

    if title is None:
        title = 'Collection of signals'
    if title_plots is None:
        title_plots = ['Signal {}'.format(n+1) for n in range(nb_sig)]

    handle = plt.figure(title)
    handle.clf()

    if complex_bool:
        for n in range(nb_sig):
            plt.subplot(nb_sig, 2, 2*n+1)
            plt.plot(vec, signal[n].real, 'b')
            plt.title(title_plots[n] + ' - real part')
            plt.xlim(xlim)
            plt.ylim(ylim)
            plt.subplot(nb_sig, 2, 2*n+2)
            plt.plot(vec, signal[n].imag, 'r')
            plt.title(title_plots[n] + ' - imaginary part')
            plt.xlim(xlim)
            plt.ylim(ylim)
    else:
        for n in range(nb_sig):
            plt.subplot(nb_sig, 1, n+1)
            plt.plot(vec, signal[n], 'b')
            plt.title(title_plots[n])
            plt.xlim(xlim)
            plt.ylim(ylim)

    return handle


def coll(vec, sig_coll, title=None, xtitle=None, ytitle=None,
         xlim=[None, None], ylim=[None, None]):
    """
    Plots a collection of signals.

    Parameters
    ----------
    vec : numpy.ndarray
        Time vector.
    sig : tuple(numpy.ndarray)
        Collection of signals to plot.
    title : str, optional (default=None)
        Title of the Figure. If None, will be set to a default value.
    xtitle : list(str), optional (default=None)
        Title of each subplots on the left column.
    ytitle : list(str), optional (default=None)
        Title of each subplots on the upper row.
    xlim : list(float), optionall (default=[None, None])
        Set the x limits of all subplots. By default autoscaling is used.
    ylim : list(float), optionall (default=[None, None])
        Set the y limits of all subplots. By default autoscaling is used.
    """

    nb_x = len(sig_coll)
    nb_y = sig_coll[0].shape[0]

    if title is None:
        title = 'Collection of signals'

    handle = plt.figure(title)
    handle.clf()

    for nx in range(nb_x):
        for ny in range(nb_y):
            plt.subplot(nb_y, nb_x, 1 + nx + ny*nb_x)
            plt.plot(vec, sig_coll[nx][ny])
            if (nx == 0) and (xtitle is not None):
                plt.title(xtitle[nx])
            if (ny == 0) and (ytitle is not None):
                plt.ylabel(ytitle[ny])
            plt.xlim(xlim)
            plt.ylim(ylim)

    return handle


def spectrogram(signal, title=None, db=True, logscale=False, phase=False,
                unwrap_angle=True, **args):
    """
    Plots the Short-Time Fourier Transform of a signal.

    Parameters
    ----------
    signal : numpy.ndarray
        Signal data.
    title : str, optional (default=None)
        Title of the Figure. If None, will be set to a default value.
    db : boolean, optional (default=True)
        Choose wether or not magnitude is expressed in deciBel.
    logscale: boolen or int, optional (default=False)
        Choose wether or not frequency axis are on a logarithmic scale.
    phase : boolean, optional (default=False)
        Choose wether or not the phase is plotted.
    unwrap_angle : boolean, optional (default=True)
        Choose wether or not the phase is unwrapped.
    args : dict(str : value)
        Arguments that are passed to scipy.signal.stft.
    **args : optional
        Optional keyword arguments passed to scipy's stft() function.
    """

    freq_vec, time_vec, spectrogram = sc_sig.stft(signal, **args)
    if title is None:
        title = 'Short-Time Fourier Transform'

    spectrogram_amp = np.abs(spectrogram)
    spectrogram_phase = np.angle(spectrogram)
    amplabel = 'STFT Magnitude'
    if db:
        spectrogram_amp = safe_db(spectrogram_amp,
                                  np.ones(spectrogram_amp.shape))
        amplabel += ' (dB)'
    if unwrap_angle:
        spectrogram_phase = np.unwrap(spectrogram_phase, 0)

    handle = plt.figure(title + ' (amplitude)')
    handle.clf()

    plt.pcolormesh(time_vec, freq_vec, spectrogram_amp)
    plt.title(amplabel)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    if logscale:
        plt.yscale('symlog')

    if phase:
        plt.figure(title + ' (phase)')
        plt.clf()
        plt.pcolormesh(time_vec, freq_vec, spectrogram_phase)
        plt.title('Phase (radians)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        if logscale:
            plt.yscale('symlog')

    return handle


def time_kernel(vec, kernel, style='wireframe', title=None, nb_levels=20,
                set_zlim=True):
    """
    Plots a discrete time kernel of order 1, 2 or 3.

    Parameters
    ----------
    vec : numpy.ndarray
        Time vector.
    kernel : 1-D or 2-D numpy.ndarray
        Kernel to plot.
    style : {'surface', 'contour', 'wireframe'}, optional (default='wireframe')
        Plot mode if the kernel is of order 2.
    title : str, optional (default=None)
        Title of the Figure. If None, will be set to a default value.
    nb_levels : int, optional (default=20)
        Optional parameter when using 'countour'.
    set_zlim : boolean, optional (default=True)
        Choose whether setting the zlim or not when plotting kernel of order 3.
    """

    order = kernel.ndim

    if order == 1:
        if title is None:
            title = 'Volterra kernel of order 1 (linear filter)'
        handle = plt.figure(title)
        handle.clf()
        plt.plot(vec, kernel)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.xlim([vec[0], vec[-1]])

    elif order == 2:
        if title is None:
            title = 'Volterra kernel of order 2'
        time_x, time_y = np.meshgrid(vec, vec)
        handle = plt.figure(title)
        handle.clf()

        if style == 'contour':
            plt.contourf(time_x, time_y, kernel, nb_levels)
            plt.colorbar(extend='both')
            plt.xlabel('Time (s)')
            plt.ylabel('Time (s)')
        elif style == 'surface':
            ax = handle.add_subplot(111, projection='3d')
            surf = ax.plot_surface(time_x, time_y, kernel, antialiased=True,
                                   cmap='jet', rstride=1, cstride=1)
            plt.colorbar(surf, extend='both')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Time (s)')
            ax.set_zlabel('Amplitude')
            ax.set_xlim([vec[0], vec[-1]])
            ax.set_ylim([vec[0], vec[-1]])
        elif style == 'wireframe':
            ax = handle.add_subplot(111, projection='3d')
            ax.plot_wireframe(time_x, time_y, kernel, antialiased=True,
                              cmap='jet')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Time (s)')
            ax.set_zlabel('Amplitude')
            ax.set_xlim([vec[0], vec[-1]])
            ax.set_ylim([vec[0], vec[-1]])

    elif order == 3:
        if title is None:
            title = 'Volterra kernel of order 3'
        time_x, time_y = np.meshgrid(vec, vec)
        fig = plt.figure(title)
        fig.clf()
        ax = fig.add_subplot(111, projection='3d')

        z_lim = [np.min(kernel), np.max(kernel)] if set_zlim else [None, None]

        def set_axes():
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Time (s)')
            ax.set_zlabel('Amplitude')
            ax.set_xlim([vec[0], vec[-1]])
            ax.set_ylim([vec[0], vec[-1]])
            ax.set_zlim(z_lim)

        current_slice = kernel[:, :, 0]
        line = ax.plot_wireframe(time_x, time_y, current_slice,
                                 antialiased=True, cmap='jet')
        set_axes()

        def animate_frame(ind, current_slice, line):
            ax.clear()
            current_slice = kernel[:, :, ind]
            line = ax.plot_wireframe(time_x, time_y, current_slice,
                                     antialiased=True, cmap='jet')
            set_axes()
            return line,

        handle = animation.FuncAnimation(fig, animate_frame,
                                         frames=kernel.shape[2],
                                         fargs=(current_slice, line),
                                         interval=100, blit=False)

    else:
        raise ValueError('Shape mismatch: the kernel is of order ' +
                         '{0} (array has {0} dimensions), '.format(order) +
                         'should be less or equal to 3.')

    return handle


def freq_kernel(vec, kernel, style='wireframe', title=None, db=True,
                logscale=False, unwrap_angle=True, nb_levels=20):
    """
    Plots a discrete transfer kernel of order 1 or 2.

    Parameters
    ----------
    vec : numpy.ndarray
        Frequency vector.
    kernel : 1-D or 2-D numpy.ndarray
        Kernel to plot.
    style : {'surface', 'contour', 'wireframe'}, optional (default='wireframe')
        Plot mode if the kernel is of order 2.
    title : str, optional (default=None)
        Title of the Figure. If None, will be set to a default value.
    db : boolean, optional (default=True)
        Choose wether or not magnitude is expressed in deciBel.
    logscale: boolean or int, optional (default=False)
        Choose wether or not frequency axis are on a logarithmic scale.
    unwrap_angle : boolean, optional (default=True)
        Choose wether or not the phase is unwrapped.
    nb_levels : int, optional (default=20)
        Optional parameter when using 'countour'.
    """

    order = kernel.ndim
    kernel_amp = np.abs(kernel)
    kernel_phase = np.angle(kernel)
    amplabel = 'Magnitude'
    if db:
        kernel_amp = safe_db(kernel_amp, np.ones(kernel_amp.shape))
        amplabel += ' (dB)'
    if unwrap_angle:
        for n in range(order):
            kernel_phase = np.unwrap(kernel_phase, n)
    idx = slice(len(vec) // 2, len(vec))

    if order == 1:
        if title is None:
            title = 'Transfer kernel of order 1 (linear filter)'
        handle = plt.figure(title)
        handle.clf()
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        ax1.plot(vec[idx], kernel_amp[idx])
        ax2.plot(vec[idx], kernel_phase[idx])
        ax1.set_ylabel(amplabel)
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Phase (radians)')
        if logscale:
            ax1.set_xscale('log')
            ax2.set_xscale('log')
        ax1.set_xlim([0, vec[-1]])
        ax2.set_xlim([0, vec[-1]])

    elif order == 2:
        if title is None:
            title = 'Transfer kernel of order 2'
        freq_x, freq_y = np.meshgrid(vec[idx], vec, indexing='ij')
        handle = plt.figure(title)
        handle.clf()

        if style == 'contour':
            ax1 = plt.subplot(211)
            ax2 = plt.subplot(212)
            ax1.contourf(freq_x, freq_y, kernel_amp[idx, :], nb_levels)
            ax2.contourf(freq_x, freq_y, kernel_phase[idx, :], nb_levels)
        if style == 'surface':
            ax1 = handle.add_subplot(211, projection='3d')
            ax2 = handle.add_subplot(212, projection='3d')
            ax1.plot_surface(freq_x, freq_y, kernel_amp[idx, :],
                             antialiased=True, cmap='jet',
                             rstride=1, cstride=1)
            ax2.plot_surface(freq_x, freq_y, kernel_phase[idx, :],
                             antialiased=True, cmap='jet',
                             rstride=1, cstride=1)
        if style == 'wireframe':
            ax1 = handle.add_subplot(211, projection='3d')
            ax2 = handle.add_subplot(212, projection='3d')
            ax1.plot_wireframe(freq_x, freq_y, kernel_amp[idx, :],
                               antialiased=True)
            ax2.plot_wireframe(freq_x, freq_y, kernel_phase[idx, :],
                               antialiased=True)

        if style == 'contour':
            ax2.set_xlabel('Frequency (Hz)')
            ax1.set_ylabel(amplabel)
            ax2.set_ylabel('Phase (radians)')
        else:
            ax1.set_xlabel('Frequency (Hz)')
            ax1.set_ylabel('Frequency (Hz)')
            ax2.set_xlabel('Frequency (Hz)')
            ax2.set_ylabel('Frequency (Hz)')
            ax1.set_zlabel(amplabel)
            ax2.set_zlabel('Phase (radians)')
            ax1.set_xlim([vec[0], vec[-1]])
            ax1.set_ylim([vec[0], vec[-1]])
            ax2.set_xlim([vec[0], vec[-1]])
            ax2.set_ylim([vec[0], vec[-1]])
        if logscale:
            ax1.set_xscale('symlog')
            ax1.set_yscale('symlog')
            ax2.set_xscale('symlog')
            ax2.set_yscale('symlog')
        ax1.set_xlim([0, vec[-1]])
        ax2.set_xlim([0, vec[-1]])

    else:
        raise ValueError('Shape mismatch: the kernel is of order ' +
                         '{0} (array has {0} dimensions), '.format(order) +
                         'should be less or equal to 2.')

    return handle
