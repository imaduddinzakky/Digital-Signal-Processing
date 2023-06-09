# -*- coding: utf-8 -*-
"""DWT Scalogram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ikJi6wpXV-vHzJmFr9TNf_8BVXgX6atS
"""

import numpy as np
import pywt
import matplotlib.pyplot as plt
import math
from math import ceil
N=64
t_n=50

xc = np.linspace(0, t_n, num=N)
xd = np.linspace(0, t_n, num=32)
sig = np.sin(2*np.pi * 64 * xc[:32]) * (1 - xd)
composite_signal3 = np.concatenate([np.zeros(32), sig[:32], np.zeros(N-32-32)])
plt.plot(sig)
plt.plot(composite_signal3)
X=np.fft.fft(composite_signal3)
x_mag=np.abs(X)/composite_signal3.size
f = plt.figure()
f.set_figwidth(20)
f.set_figheight(5)
plt.plot(x_mag)
plt.show()
# Use the Daubechies wavelet
w = pywt.Wavelet('db1')
# Perform Wavelet transform up to log2(N) levels
lvls = ceil(math.log2(N))
coeffs = pywt.wavedec(composite_signal3, w, level=lvls)
# Each level of the WT will split the frequency band in two and apply a
# WT on the highest band. The lower band then gets split into two again,
# and a WT is applied on the higher band of that split. This repeats
# 'lvls' times.
#
# Since the amount of samples in each step decreases, we need to make
# sure that we repeat the samples 2^i times where i is the level so
# that at each level, we have the same amount of transformed samples
# as in the first level. This is only necessary because of plotting.
cc = np.abs(np.array([coeffs[-1]]))
for i in range(lvls - 1):
    cc = np.concatenate(np.abs([cc, np.array([np.repeat(coeffs[lvls - 1 - i], pow(2, i + 1))])]))

plt.figure()
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Discrete Wavelet Transform')
# X-axis has a linear scale (time)
x = np.linspace(start=0, stop=1, num=N//2)
# Y-axis has a logarithmic scale (frequency)
y = np.logspace(start=lvls-1, stop=0, num=lvls, base=2)
X, Y = np.meshgrid(x, y)
plt.pcolormesh(X, Y, cc)

use_log_scale = False

if use_log_scale:
    plt.yscale('log')
else:
    yticks = [pow(2, i) for i in range(lvls)]
    plt.yticks(yticks)

plt.tight_layout()
plt.show()