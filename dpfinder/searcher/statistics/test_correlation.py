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

from dpfinder.searcher.statistics.correlation import correlation


class TestCorrelation(unittest.TestCase):

	@staticmethod
	def sample_gaussian(corr):
		mean = [0, 0]
		cov = [[1, corr], [corr, 1]]
		r = np.random.multivariate_normal(mean, cov, size=1000*1000)
		return r[:, 0], r[:, 1]

	def check_corr(self, corr):
		pa, pb = self.sample_gaussian(corr)
		c = correlation(pa, pb)
		self.assertAlmostEqual(c, corr, 2)

	def test_no_corr(self):
		self.check_corr(0)

	def test_full_corr(self):
		self.check_corr(1)

	def test_medium_corr(self):
		self.check_corr(0.5)


if __name__ == '__main__':
	unittest.main()
