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

from dpfinder.scorer.psi_scorer import PSIScorer
from dpfinder.algorithms.algs.aboveThreshold import AboveThreshold
from dpfinder.algorithms.algs.alg1 import Alg1
from dpfinder.algorithms.algs.alg2 import Alg2
from dpfinder.algorithms.algs.alg3 import Alg3
from dpfinder.algorithms.algs.alg5 import Alg5
from dpfinder.algorithms.algs.sum import Sum
from dpfinder.algorithms.algs.expMech import ExpMech
from dpfinder import logging


class TestPSIScorer(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# prepare logger
		logfile = logging.get_log_file('psi_scorer_test/' + cls.__name__)
		logging.set_logfile(logfile)

	@classmethod
	def tearDownClass(cls):
		logging.shutdown()

	@staticmethod
	def get_alg():
		return AboveThreshold(1)

	@staticmethod
	def get_inputs_output():
		return [0], [0], [0]

	@staticmethod
	def get_prob():
		return 0.5

	def test_get_prob(self):
		a = self.get_alg()
		s = PSIScorer(a)
		input, _, output = self.get_inputs_output()
		ret = s.get_prob(input, output)
		self.assertEqual(ret, self.get_prob())

	def test_psi_scorer(self):
		a = self.get_alg()
		s = PSIScorer(a)
		input1, input2, output = self.get_inputs_output()
		ret = s.score(input1, input2, output)
		self.assertEqual(ret, 0)


class TestAlg1(TestPSIScorer):

	@staticmethod
	def get_alg():
		return Alg1(1, 1)


class TestAlg2(TestPSIScorer):

	@staticmethod
	def get_alg():
		return Alg2(1, 1)


class TestAlg3(TestPSIScorer):

	@staticmethod
	def get_alg():
		return Alg3(1, 1)

	@staticmethod
	def get_inputs_output():
		return [0], [0], np.array([[0, 0], [0, 0]])

	@staticmethod
	def get_prob():
		return 0.0


class TestAlg5(TestPSIScorer):

	@staticmethod
	def get_alg():
		return Alg5(1)

	@staticmethod
	def get_inputs_output():
		return np.array([-8.4311092255497311, 7.9951193845746680, -7.6293585045750101, -3.5285106121239611]), \
			np.array([-9.0698729923760233, 8.6876466606845071, -8.3001561863281559, -3.4268547142592141]), \
			np.array([0.0000000000000000, 0.0000000000000000, 1.0000000000000000, 0.0000000000000000])

	@staticmethod
	def get_prob():
		return 0.0


class TestSum(TestPSIScorer):

	@staticmethod
	def get_alg():
		return Sum(1)

	@staticmethod
	def get_inputs_output():
		return [0], [0, 0], [0, 0]

	@staticmethod
	def get_prob():
		return 0.0


class TestExpMech(TestPSIScorer):

	@staticmethod
	def get_alg():
		return ExpMech(1, 1)

	@staticmethod
	def get_prob():
		return 1.0


if __name__ == '__main__':
	unittest.main()
