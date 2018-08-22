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
import tensorflow as tf
import numpy as np

from dpfinder.utils.tf.tf_wrapper import TensorFlowWrapper


class TestTensorFlowWrapper(unittest.TestCase):

	shape = (2,)
	x_init = np.ones(shape)

	def build_graph(self):
		self.x = tf.get_variable('x', shape=self.shape)
		self.res = tf.reduce_sum(self.x)
		return self.res

	def test_full(self):
		t = TensorFlowWrapper('test')
		t.build_fresh_graph('res', self.build_graph)
		t.initialize({self.x: self.x_init})
		res = t.run(self.res)
		self.assertEqual(res, 2.0)
		return t

	def test_optimize(self):
		t = self.test_full()
		o = t.get_optimizer(self.res, 20, {self.x: (-1.0, 1.0)}, [])
		t.minimize(o)
		best = t.run(self.res)
		self.assertAlmostEqual(best, -2)


if __name__ == '__main__':
	unittest.main()
