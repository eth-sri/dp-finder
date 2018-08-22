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


class Alg3Impl(TensorFlowImplementation):
	def __init__(self, params):
		self.array_size = params.array_size
		super().__init__(params.name, params.array_size, params.array_size, (params.array_size, 2), precision_np)
		self.params = params
		self.rho = None
		self.nu = None

	def get_randomness(self, n_samples):
		epsilon1 = self.params.epsilon / 2
		rho = get_laplace(self.params.delta / epsilon1, n_samples)
		epsilon2 = self.params.epsilon / 2
		nu = get_laplace(self.params.c * self.params.delta / epsilon2, (n_samples, self.params.array_size))
		return {
			self.rho: rho,
			self.nu: nu
		}

	def estimate_internal(self, input, output):
		pr = Primitives()
		count = tf_const(0)
		c = tf_const(self.params.c)
		out = []
		for i in range(self.params.array_size):
			ai = input[i] + self.nu[:, i]
			above_threshold = pr.geq(ai, self.params.threshold + self.rho)
			abort = pr.eq(count, c)
			hit = pr.and_diff(above_threshold, pr.not_diff(abort))
			count = pr.ite(hit, count + 1, count)
			out.append(pr.ite(hit, ai, -10))

		ret = 1
		for i in range(self.params.array_size):
			hit = pr.and_diff(pr.geq(out[i], output[i, 0]), pr.geq(output[i, 1], out[i]))
			ret = pr.and_diff(ret, hit)

		return ret

	def get_b(self, a, d):
		return a+d

	def get_var_to_bounds(self, a, d, o):
		return {d: (-1.0, 1.0)}

	def prepare_randomness_placeholders(self):
		self.rho = tf.placeholder(tf.float64)
		self.nu = tf.placeholder(tf.float64)