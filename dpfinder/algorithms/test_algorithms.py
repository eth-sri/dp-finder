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

from dpfinder.algorithms import algorithms


class TestAboveThreshold(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestAboveThreshold, self).__init__(*args, **kwargs)
		self.a = self.get_alg()

	@staticmethod
	def get_name():
		return 'aboveThreshold'

	def get_alg(self):
		return algorithms.get_algorithm(self.get_name(), 4)

	@staticmethod
	def get_larger_dict():
		return {'array_size': 4, 'garbage': 10}

	def test_get(self):
		self.assertIsNotNone(self.a)

	def test_get_algorithm_larger_dict(self):
		a = algorithms.get_algorithm_larger_dict(
			self.get_name(), self.get_larger_dict())
		self.assertIsNotNone(self.a)
		self.assertEqual(self.a.array_size, 4)

	def test_get_psi_file(self):
		f = self.a.get_psi_filename()
		self.assertIsNotNone(f)

	def test_get_psi_base_script(self):
		script = self.a.get_psi_base_script()
		self.assertIsInstance(script, str)
		self.assertIsNotNone(script)
		self.assertNotEqual(script, '')

	def test_input_output(self):
		a, b = self.a.get_random_input()
		self.assertEqual(a.shape, (4,))
		self.assertEqual(b.shape, (4,))
		o = self.a.get_random_output(a, b)
		self.assertEqual(o.shape, (4,))

	def test_initialize_graph(self):
		imp = self.a.get_tensorflow_implementation()
		imp.build_fresh_graph()
		imp.fresh_randomness(200)
		self.a.set_random_start(imp)
		d = imp.run_all()
		self.assertIsInstance(d.eps, float)

		imp.close()


class TestAlg1(TestAboveThreshold):

	@staticmethod
	def get_name():
		return 'alg1'

	def get_alg(self):
		return algorithms.get_algorithm(self.get_name(), 4, 1)

	@staticmethod
	def get_larger_dict():
		return {'array_size': 4, 'c': 1, 'garbage': 10}


class TestAlg2(TestAlg1):

	@staticmethod
	def get_name():
		return 'alg2'


class TestAlg3(TestAlg1):

	@staticmethod
	def get_name():
		return 'alg3'

	def test_input_output(self):
		a, b = self.a.get_random_input()
		self.assertEqual(a.shape, (4,))
		self.assertEqual(b.shape, (4,))
		o = self.a.get_random_output(a, b)
		self.assertEqual(o.shape, (4, 2))


class TestAlg4(TestAlg1):

	@staticmethod
	def get_name():
		return 'alg4'


class TestAlg5(TestAboveThreshold):

	@staticmethod
	def get_name():
		return 'alg5'


class TestSum(TestAboveThreshold):

	@staticmethod
	def get_name():
		return 'sum'

	def test_input_output(self):
		a, b = self.a.get_random_input()
		self.assertEqual(a.shape, (4,))
		self.assertEqual(b.shape, (1,))
		o = self.a.get_random_output(a, b)
		self.assertEqual(o.shape, (2,))


class TestExpMech(TestAlg1):

	@staticmethod
	def get_name():
		return 'expMech'

	def test_input_output(self):
		a, b = self.a.get_random_input()
		self.assertEqual(a.shape, (4,))
		self.assertEqual(b.shape, (4,))
		o = self.a.get_random_output(a, b)
		self.assertEqual(o.shape, (1,))


class TestReportNoisyMax(TestExpMech):

	@staticmethod
	def get_name():
		return 'reportNoisyMax'


if __name__ == '__main__':
	unittest.main()
