# ==BEGIN LICENSE==
# 
# MIT License
# 
# Copyright (c) 2018 SRI Lab, ETH Zurich
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# ==END LICENSE==


import ctypes
import os

from dpfinder.logging import logger
from dpfinder.utils.redirect import redirect_stdout

path = os.path.dirname(__file__)
lib = ctypes.cdll.LoadLibrary(path + '/libratio.so')

joint_gauss_fraction = getattr(lib, "ratio_cdf_extern", None)
joint_gauss_fraction.restype = ctypes.c_double

ratio_pdf_extern = getattr(lib, "ratio_pdf_extern", None)
ratio_pdf_extern.restype = ctypes.c_double


def cdf(lower, upper, mx, my, sx, sy, rho):
	lower = ctypes.c_double(lower)
	upper = ctypes.c_double(upper)
	mx = ctypes.c_double(mx)
	my = ctypes.c_double(my)
	sx = ctypes.c_double(sx)
	sy = ctypes.c_double(sy)
	rho = ctypes.c_double(rho)
	return joint_gauss_fraction(lower, upper, mx, my, sx, sy, rho)


def pdf(w, mx, my, sx, sy, rho):
	w = ctypes.c_double(w)
	mx = ctypes.c_double(mx)
	my = ctypes.c_double(my)
	sx = ctypes.c_double(sx)
	sy = ctypes.c_double(sy)
	rho = ctypes.c_double(rho)
	return ratio_pdf_extern(w, mx, my, sx, sy, rho)


ratio_confidence_interval_C = getattr(lib, "ratio_confidence_interval_extern", None)
ratio_confidence_interval_C.restype = ctypes.c_double


def ratio_confidence_interval(p1, p2, d1, d2, corr, center, confidence, err_goal):
	p1 = ctypes.c_double(p1)
	p2 = ctypes.c_double(p2)
	d1 = ctypes.c_double(d1)
	d2 = ctypes.c_double(d2)
	corr = ctypes.c_double(corr)
	center = ctypes.c_double(center)
	confidence = ctypes.c_double(confidence)
	err_goal = ctypes.c_double(err_goal)
	with redirect_stdout.redirect(output=logger.debug):
		ret = ratio_confidence_interval_C(p1, p2, d1, d2, corr, center, confidence, err_goal)
	return ret
