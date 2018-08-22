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

from dpfinder.searcher.searcher import Searcher
from dpfinder.scorer.scorer import Scorer
from dpfinder.algorithms.algorithms import get_algorithm


class MyScorer(Scorer):

	count = 0

	def score_internal(self, a, b, o):
		self.count += 0.1
		return self.count

	def get_prob(self, input, output):
		return 0


class MySearcher(Searcher):
	def __init__(self):
		alg = get_algorithm('aboveThreshold', 4)
		super().__init__(10, MyScorer(), alg)

	count = 0

	def step_internal(self, s):
		self.count += 0.1
		return s, s, s, self.count


class TestSearcher(unittest.TestCase):
	def test_searcher(self):
		s = MySearcher()
		ret = s.search(10)
		self.assertLess(abs(ret - 1.0), 1e-10)


if __name__ == '__main__':
	unittest.main()
