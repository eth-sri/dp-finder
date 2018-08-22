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


import numpy as np
import numpy.random as r
import os
import subprocess
import socket


def arr_of_int(a):
	for t in [np.int64]:
		if all(isinstance(item, t) for item in a):
			return True
	return False


def arr_to_str(a):
	if arr_of_int(a):
		return "[" + ", ".join([str(x) for x in a]) + "]"
	else:
		return "[" + ", ".join(["{0:.16f}".format(x) for x in a]) + "]"


def my_to_str(x):
	if isinstance(x, (list, tuple, np.ndarray)):
		return "[" + ", ".join([str(e) for e in x]) + "]"
	else:
		return str(x)


# returns an array of length array_size with n_hot "1"-entries
def n_hot(n_hot, array_size):
	assert (n_hot <= array_size)
	a = np.zeros(array_size, dtype=int)
	for n_flipped in range(n_hot):
		index = r.randint(0, array_size - n_flipped)
		i = nthWithProperty(a, index, lambda x: x == 0)
		a[i] = 1
	return a


# returns the index of the n-th (0-based) element that satisfies the property
def nthWithProperty(arr, n, prop):
	count = 0
	for i in range(len(arr)):
		if prop(arr[i]):
			if n == count:
				return i
			count += 1


def create_dir_if_not_exists(directory):
	"""Recursively creates directory (including its parents, if necessary)"""
	if not os.path.exists(directory):
		os.makedirs(directory)


def get_git_version():
	try:
		v = subprocess.check_output(["git", "describe", "--always"]).strip()
		v = v.decode("utf-8")
	except subprocess.CalledProcessError:
		v = 'no-git'
	return v


def get_hostname():
	hostname = socket.gethostname()
	return hostname


def get_file_content(file):
	with open(file) as f:
		return f.read()
