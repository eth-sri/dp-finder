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
import math

from dpfinder.logging import logger
from dpfinder.utils.redirect import redirect_stdout
from dpfinder.searcher.statistics.ratio.ratio_cdf import ratio_confidence_interval
from dpfinder.searcher.statistics.correlation import correlation


def get_confidence_interval(pas, pbs, confidence, eps_err_goal):
	"""
	:param pas:
	:param pbs:
	:return: a confidence interval for log(pa)-log(pb), as the maximum deviation from the mean.
	pa (pb) is the average of pas(pbs)
	"""

	n_samples = pas.shape[0]
	pa = np.average(pas)
	pb = np.average(pbs)
	eps = np.log(pa) - np.log(pb)

	orig_stda = np.linalg.norm(pas - pa) / np.sqrt(n_samples - 1)
	orig_stdb = np.linalg.norm(pbs - pb) / np.sqrt(n_samples - 1)
	stda = 1 / np.sqrt(n_samples) * orig_stda
	stdb = 1 / np.sqrt(n_samples) * orig_stdb
	corr = correlation(pas, pbs)

	if math.isnan(eps):
		return float('nan')

	logger.debug(
		"%s+-%s (original std: %s) and %s+-%s (original std: %s) (corr %s)",
		pa, 0.0, orig_stda,
		pb, 0.0, orig_stdb,
		corr)

	with redirect_stdout.redirect(output=logger.debug):
		d = ratio_confidence_interval(pa, pb, stda, stdb, corr, eps, confidence, eps_err_goal)

	logger.debug(
		"%s+-%s (original std: %s) and %s+-%s (original std: %s) (corr %s, eps_err %s)",
		pa, 0.0, orig_stda,
		pb, 0.0, orig_stdb,
		corr, d)

	return d
