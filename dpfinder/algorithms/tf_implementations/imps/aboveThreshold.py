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


from dpfinder.algorithms.tf_implementations.primitives import Primitives
from dpfinder.algorithms.tf_implementations.implementation import TensorFlowImplementation, precision_np
from dpfinder.algorithms.tf_implementations.distribution_helpers import *


class AboveThresholdImpl(TensorFlowImplementation):

	def __init__(self, params):
		self.array_size = params.array_size
		super().__init__(params.name, params.array_size, params.array_size, params.array_size, precision_np)
		self.params = params
		self.rho = None
		self.nu = None

	def prepare_randomness_placeholders(self):
		self.rho = tf.placeholder(tf.float64)
		self.nu = tf.placeholder(tf.float64)

	def estimate_internal(self, input, output):
		pr = Primitives()
		out = []
		for i in range(self.array_size):
			above_threshold = pr.geq(input[i] + self.nu[:, i], self.params.threshold + self.rho)
			hit = above_threshold
			out.append(pr.ite(hit, 1, 0))
		ret = 1

		for i in range(self.array_size):
			ret = pr.and_diff(ret, pr.eq(out[i], output[i]))

		return ret

	def get_randomness(self, n_samples):
		epsilon1 = self.params.epsilon / 2
		rho = get_laplace(self.params.delta / epsilon1, n_samples)
		epsilon2 = self.params.epsilon / 2
		nu = get_laplace(self.params.delta / epsilon2, (n_samples, self.array_size))
		return {
			self.rho: rho,
			self.nu: nu
		}

	def get_var_to_bounds(self, a, d, o):
		return {d: (-1.0, 1.0)}

	def get_b(self, a, d):
		return a + d
