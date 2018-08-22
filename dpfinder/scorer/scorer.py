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


import math
from abc import ABC, abstractmethod
import numpy as np

from dpfinder.logging import logger
from dpfinder.utils.timer import time_measure


class Scorer(ABC):

	def score(self, a, b, o):

		logger.debug("Scorer: Started")

		# sanity checks
		if np.isnan(a).any() or np.isnan(b).any() or np.isnan(o).any():
			logger.warning("Scorer: Parameters contain 'nan', will not call PSI. Returning 0.0 instead...")
			ret = 0.0
		else:
			with time_measure('scorer-time'):
				ret = self.score_internal(a, b, o)

		logger.debug("Scorer: Finished (Result:%s)", ret)

		return ret

	@abstractmethod
	def get_prob(self, input, output) -> float:
		pass

	def score_internal(self, a, b, o):
		logger.debug('Scorer: Computing probabilities')
		pa = self.get_prob(a, o)
		pb = self.get_prob(b, o)

		logger.info("Scorer: Comparing probabilities pa and pb:\t%s\t%s", pa, pb)

		eps = self.score_from_probability(pa, pb)
		return eps

	@staticmethod
	def score_from_probability(pa, pb):
		if pa <= 0 and pb <= 0:
			return 0
		if pb <= 0:
			return math.inf
		if pa <= 0:
			return 0
		eps = math.log(pa) - math.log(pb)
		return abs(eps)
