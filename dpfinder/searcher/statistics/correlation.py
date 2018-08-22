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


import numpy as np

from dpfinder.utils.tf.rounder import rounder
from dpfinder.logging import logger


def correlation(pa, pb):
	n = pa.shape[0]

	rounder.downward()
	sum_lower_a = np.sum(pa)
	sum_lower_b = np.sum(pb)

	rounder.upward()
	sum_sq_upper_a = np.sum(pa ** 2)
	sum_sq_upper_b = np.sum(pb ** 2)
	v_a = sum_sq_upper_a - sum_lower_a * sum_lower_a / n
	v_b = sum_sq_upper_b - sum_lower_b * sum_lower_b / n
	den_a = np.sqrt(v_a)
	den_b = np.sqrt(v_b)
	den = den_a * den_b

	rounder.to_nearest()
	if den == 0:
		return 0
	else:
		rounder.upward()
		sum_upper_a = np.sum(pa)
		sum_upper_b = np.sum(pb)
		tmp = sum_upper_a * sum_upper_b / n

		rounder.downward()
		sum_mult_lower = np.sum(pa * pb)
		num = sum_mult_lower - tmp
		corr = num / den
		rounder.to_nearest()
		if abs(corr) > 1.0:
			logger.warning("|corr|>1.0: %s, distance from 1.0:", corr, abs(corr - 1.0))
			corr = min(corr, 1.0)
			corr = max(corr, -1.0)

		return corr