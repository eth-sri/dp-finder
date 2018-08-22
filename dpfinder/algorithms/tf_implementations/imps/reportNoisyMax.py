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
from dpfinder.algorithms.tf_implementations.imps.expMech import ExpMechImpl
from dpfinder.algorithms.tf_implementations.distribution_helpers import *


class ReportNoisyMaxImpl(ExpMechImpl):

	def estimate_internal(self, input, output):
		pr = Primitives()
		best = -pr.get_inf()
		best_by_index = tf_const(0)
		for i in range(0, self.array_size):
			d = input[i] + self.noise[:, i]
			hit = pr.eq(tf_const(i), output)
			best = pr.ite(hit, best, tf.maximum(best, d))
			best_by_index = pr.ite(hit, input[i], best_by_index)

		scale = 2 / self.params.epsilon
		x = best - best_by_index
		return tf.exp(laplacian_cdf(x, scale)[1])

	def get_randomness(self, n_samples):
		scale = 2 / self.params.epsilon
		noise = get_laplace(scale, (n_samples, self.params.array_size))
		return {
			self.noise: noise
		}
