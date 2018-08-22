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
from dpfinder.algorithms.tf_implementations.imps.aboveThreshold import AboveThresholdImpl
from dpfinder.algorithms.tf_implementations.distribution_helpers import *


class Alg2Impl(AboveThresholdImpl):
	def __init__(self, params):
		super().__init__(params)

	def get_randomness(self, n_samples):
		epsilon1 = self.params.epsilon / 2
		rho = get_laplace(self.params.c * self.params.delta / epsilon1, (n_samples, self.params.array_size))
		epsilon2 = self.params.epsilon / 2
		nu = get_laplace(2 * self.params.c * self.params.delta / epsilon2, (n_samples, self.params.array_size))
		return {
			self.rho: rho,
			self.nu: nu
		}

	def estimate_internal(self, input, output):
		pr = Primitives()
		count = tf_const(0)
		c = tf_const(self.params.c)
		out = []
		this_rho = self.rho[:, 0]
		for i in range(self.params.array_size):
			above_threshold = pr.geq(input[i] + self.nu[:, i], self.params.threshold + this_rho)
			abort = pr.eq(count, c)
			hit = pr.and_diff(above_threshold, pr.not_diff(abort))
			count = pr.ite(hit, count + 1, count)
			out.append(pr.ite(hit, 1, 0))
			if i + 1 < self.params.array_size:
				this_rho = pr.ite(hit, self.rho[:, i + 1], this_rho)
		ret = 1

		for i in range(self.params.array_size):
			ret = pr.and_diff(ret, pr.eq(out[i], output[i]))

		return ret
