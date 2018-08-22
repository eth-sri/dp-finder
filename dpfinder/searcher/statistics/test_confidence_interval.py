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


import unittest
import numpy as np

from dpfinder.searcher.statistics.confidence_interval import get_confidence_interval


class TestCorrelation(unittest.TestCase):
	size = 100 * 100
	confidence = 0.9
	eps_err_goal = 0.001

	def sample_gaussians(self, corr):
		mean = [1, 1]
		cov = [[1, corr], [corr, 1]]
		r = np.random.multivariate_normal(mean, cov, size=self.size)
		return r[:, 0], r[:, 1]

	def check_interval(self, corr):
		# compute the interval
		pas, pbs = self.sample_gaussians(corr)
		interval = get_confidence_interval(pas, pbs, self.confidence, self.eps_err_goal)

		# empirically check that the interval is correct
		n_ok = 1
		n_tests = 1000
		for _ in range(n_tests):
			pas, pbs = self.sample_gaussians(corr)
			eps = np.log(np.average(pas)) - np.log(np.average(pbs))
			if abs(eps) < interval:
				n_ok += 1
		self.assertAlmostEqual(n_ok / n_tests, self.confidence, 1)

	def test_no_correlation(self):
		self.check_interval(0)

	def test_more_correlation(self):
		self.check_interval(0.5)


if __name__ == '__main__':
	unittest.main()
