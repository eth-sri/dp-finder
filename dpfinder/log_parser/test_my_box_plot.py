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
import os

from dpfinder.log_parser.my_box_plot import MyBoxPlot
from matplotlib import pyplot as plt  # must be after the import above

path = os.path.dirname(os.path.realpath(__file__))


class TestMyBoxPlot(unittest.TestCase):
	def test(self):
		bounds = [1, 2, 3]
		data = [[[0.7], [0.8]], [[1.7], [1.8]], [[2.7], [2.8]]]
		above_range = [0, 3]
		below_range = [0, 3]
		labels = ['A', 'B', 'C']
		sub_labels = ['left', 'right']
		p = MyBoxPlot([above_range, below_range], height_ratios=[1.0, 1.0])
		p.plot(bounds, data, labels, sub_labels)

		pdf = os.path.join(path, 'figures/tmp.pdf')
		plt.savefig(pdf, bbox_inches='tight')
		plt.clf()


if __name__ == '__main__':
	unittest.main()
