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


class Alg5Impl(AboveThresholdImpl):
	def __init__(self, params):
		super().__init__(params)

	def get_randomness(self, n_samples):
		epsilon1 = self.params.epsilon / 2
		rho = get_laplace(self.params.delta / epsilon1, n_samples)
		return {
			self.rho: rho
		}

	def estimate_internal(self, input, output):
		pr = Primitives()
		out = []
		for i in range(self.params.array_size):
			above_threshold = pr.geq(input[i], self.params.threshold + self.rho)
			hit = above_threshold
			out.append(pr.ite(hit, 1, 0))
		ret = 1

		for i in range(self.params.array_size):
			ret = pr.and_diff(ret, pr.eq(out[i], output[i]))

		return ret
