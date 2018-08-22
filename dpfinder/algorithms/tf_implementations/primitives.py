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


import tensorflow as tf


class Primitives:

	def __init__(self, const=50.0):
		self.const = const

	def geq_0(self, x):
		if isinstance(x, int) or isinstance(x, float):
			return 1.0 if x >= 0 else 0.0
		return tf.sigmoid(self.const * x)

	def geq(self, x, y):
		return self.geq_0(x - y)

	def bool_eq(self, x, y):
		both_1 = self.and_diff(x, y)
		both_0 = self.and_diff(self.not_diff(x), self.not_diff(y))
		return self.or_diff(both_0, both_1)

	def or_diff(self, x, y):
		return x + y - x * y

	def and_diff(self, x, y):
		return x * y

	def not_diff(self, x):
		return 1.0 - x

	def ite(self, b, x, y):
		return b * x + (1.0 - b) * y

	def eq_0(self, x):
		return tf.exp(-(self.const * x) ** 2)

	def eq(self, x, y):
		return self.eq_0(x - y)

	def get_inf(self):
		return tf.constant(1000, dtype=tf.float64)
