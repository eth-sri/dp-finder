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

from dpfinder.log_parser.parser import EpsType, get_parsed
from dpfinder import logging
from dpfinder.searcher.search import search, get_args_parser


class TestParser(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestParser, self).__init__(*args, **kwargs)

		# prepare logger
		logfile = logging.get_log_file('parser_test')
		logging.set_logfile(logfile)

		parser = get_args_parser(n_steps=4, confidence=0.9)
		args = parser.parse_args([])
		search(args)

		# finish logging
		logging.shutdown()

		# get generated log
		self.p = get_parsed(logfile + '_data.log')

	def test_empirical_eps(self):
		optimised_eps = self.p.get_empirical_eps(eps_type=EpsType.OPT)
		self.assertEqual(len(optimised_eps), 2)

		random_eps = self.p.get_empirical_eps(eps_type=EpsType.RAND)
		self.assertEqual(len(random_eps), 2)

	def test_confirmed_eps(self):
		empirical_eps = self.p.get_empirical_eps(eps_type=EpsType.ALL)
		confirmed_eps = self.p.get_confirmed_eps()
		for i in range(len(empirical_eps)):
			self.assertAlmostEqual(confirmed_eps[i], empirical_eps[i], 1)
			self.assertNotEqual(confirmed_eps[i], empirical_eps[i])

	def test_times(self):
		opt = self.p.get_optimize_time()
		self.assertEqual(len(opt), 2)

		rand = self.p.get_random_time()
		self.assertEqual(len(rand), 2)

	def test_alg_name(self):
		n = self.p.get_alg_name()
		self.assertEqual(n, 'aboveThreshold')

	def test_short_alg_name(self):
		n = self.p.get_short_alg_name()
		self.assertEqual(n, 'AT')

	def test_bound(self):
		b = self.p.get_bound()
		self.assertIsInstance(b, float)
		self.assertGreaterEqual(b, 0)


if __name__ == '__main__':
	unittest.main()
