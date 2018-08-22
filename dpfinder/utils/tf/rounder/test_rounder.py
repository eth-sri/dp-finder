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
from dpfinder.utils.tf.rounder.rounder import upward, downward, to_nearest


eps = 1 / (1 << 30)


class TestRounder(unittest.TestCase):

	def test_up(self):
		x = np.array([1.0, eps], dtype=np.float32)
		upward()
		self.assertGreater(x.sum(), 1.0)

	def test_down(self):
		x = np.array([1.0, -eps], dtype=np.float32)
		downward()
		self.assertLess(x.sum(), 1.0)

	def test_nearest(self):
		x = np.array([1.0, eps], dtype=np.float32)
		to_nearest()
		self.assertEqual(x.sum(), 1.0)


if __name__ == '__main__':
	unittest.main()
