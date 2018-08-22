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

from dpfinder.algorithms.algs.alg1 import Alg1
from dpfinder.utils.utils import n_hot
from dpfinder.algorithms.algorithms import precision_np
from dpfinder.utils.utils import arr_to_str


class Alg3(Alg1):

	def get_random_output(self, a, b):
		hot = n_hot(r.randint(0, self.max_n_hot + 1), self.array_size)
		expected = -10 * np.ones(self.array_size, dtype=precision_np)
		expected[hot == 1] = a[hot == 1]
		o_init = np.empty((self.array_size, 2), dtype=precision_np)
		o_init[:, 0] = expected - 3
		o_init[:, 1] = expected + 3
		return o_init.astype(precision_np)

	def get_psi_script(self, a, o):
		psi_script = self.get_psi_base_script()
		psi_script = psi_script.replace("[$A]", arr_to_str(a))
		intervals = "[{},{}]".format(arr_to_str(o[:, 0]), arr_to_str(o[:, 1]))
		psi_script = psi_script.replace("[$O]", intervals)
		psi_script = psi_script.replace("$C", str(self.c))
		return psi_script
