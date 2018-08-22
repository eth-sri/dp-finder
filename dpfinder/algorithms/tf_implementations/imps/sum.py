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


class SumImpl(TensorFlowImplementation):
	def __init__(self, params):
		self.array_size = params.array_size
		super().__init__(params.name, params.array_size, 1, 2, precision_np)
		self.params = params

		self.rho = None

	def get_randomness(self, n_samples):
		epsilon = self.params.epsilon
		rho = get_laplace(1 / epsilon, n_samples)
		return {
			self.rho: rho
		}

	def estimate_internal(self, input, output):
		pr = Primitives()

		out = tf.reduce_sum(input)
		out += self.rho

		ret = pr.and_diff(pr.geq(out, output[0]), pr.geq(output[1], out))

		return ret

	def get_var_to_bounds(self, a, d, o):
		return {a: (-1.0, 1.0), d: (-1.0, 1.0)}

	def get_b(self, a, d):
		return tf.concat([a, d], axis=0)

	def prepare_randomness_placeholders(self):
		self.rho = tf.placeholder(tf.float64)
