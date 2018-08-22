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

from dpfinder.searcher.tf_searcher import TensorFlowSearcher
from dpfinder.scorer.psi_scorer import PSIScorer
from dpfinder.algorithms.algorithms import get_algorithm
from dpfinder.logging import logger


class TestTensorFlowSearcher(unittest.TestCase):
	def test(self):
		# prepare logger
		log_file = logger.get_log_file('tensorflow_searcher_test')
		logger.set_logfile(log_file)
		logger.info('Starting test of TensorFlowSearcher')

		# prepare arguments
		confirming = 10
		alg = get_algorithm('aboveThreshold', 4)
		confirmer = PSIScorer(alg)
		min_n_samples = 2000
		max_n_samples = 200*1000
		confidence = 0.9
		eps_err_goal = 0.01
		s = TensorFlowSearcher(confirming, confirmer, min_n_samples, max_n_samples, confidence, eps_err_goal, alg)

		# search
		eps = s.search(4)

		# check
		self.assertGreaterEqual(eps, 0)

		# finish logging
		logger.info('Finished test of TensorFlowSearcher')
		logger.shutdown()


if __name__ == '__main__':
	# unittest.main()
	s = TestTensorFlowSearcher()
	s.test()
