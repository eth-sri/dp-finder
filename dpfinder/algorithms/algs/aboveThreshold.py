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

from dpfinder.algorithms.algorithms import Algorithm, precision_np, precision_tf
from dpfinder.utils.utils import n_hot


class AboveThreshold(Algorithm):

	def __init__(self, array_size):
		super().__init__()
		self.array_size = array_size
		self.threshold = 0
		self.delta = 1
		self.epsilon = 0.1
		self.max_n_hot = self.array_size

	def get_random_input(self):
		a_init = np.random.uniform(-10, 10, size=self.array_size)
		d_init = np.random.uniform(-1, 1, size=self.array_size)
		a_init = a_init.astype(precision_np)
		d_init = d_init.astype(precision_np)
		return a_init, d_init

	def get_random_output(self, a, b):
		o_init = n_hot(r.randint(0, self.max_n_hot + 1), self.array_size)
		return o_init.astype(precision_np)

