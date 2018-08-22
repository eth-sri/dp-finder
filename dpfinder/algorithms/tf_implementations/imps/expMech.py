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


class ExpMechImpl(TensorFlowImplementation):

	def __init__(self, params):
		self.array_size = params.array_size
		super().__init__(params.name, params.array_size, params.array_size, 1, precision_np)
		self.params = params
		self.noise = None

	def prepare_randomness_placeholders(self):
		self.noise = tf.placeholder(tf.float64)

	def estimate_internal(self, input, output):
		pr = Primitives()
		best = -pr.get_inf()
		best_by_index = tf_const(0)
		for i in range(0, self.array_size):
			d = input[i] + self.noise[:, i]
			hit = pr.eq(tf_const(i), output)
			best = pr.ite(hit, best, tf.maximum(best, d))
			best_by_index = pr.ite(hit, input[i], best_by_index)

		rate = self.params.epsilon / 2
		x = best - best_by_index
		return pr.ite(pr.geq(x, tf_const(0)), exponential_cdf_right(rate, x), tf_const(1))

	def get_randomness(self, n_samples):
		scale = 2 / self.params.epsilon
		noise = get_exponential(scale, (n_samples, self.params.array_size))
		return {
			self.noise: noise
		}

	def get_var_to_bounds(self, a, d, o):
		return {d: (-1.0, 1.0)}

	def get_b(self, a, d):
		return a + d
