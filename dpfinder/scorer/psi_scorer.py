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


import re

from dpfinder.psi.runPsi import run_on_string
from dpfinder.scorer.scorer import Scorer
from dpfinder.logging import logger
from dpfinder.utils import evaluate_math as ev

psi_flags = '--raw --mathematica --nonormalize'

regex = re.compile(r"\*DiracDelta\[[^\]]*\]")


class PSIScorer(Scorer):

	def __init__(self, alg):
		super().__init__()
		self.alg = alg

	def get_prob(self, a, o):
		psi_script = self.alg.get_psi_script(a, o)
		logger.debug(psi_script)
		res = run_on_string(psi_script, psi_flags)
		logger.debug("PSI time:%s", res.time)
		logger.data('psi-time', res.time)
		if res.error is not "":
			logger.error("PSI error:" + res.error)
			raise Exception("PSI error:" + res.error)
		logger.debug("PSI output:%s", res.output)
		if res.output == "DiracDelta[-r+1]":
			ret = 1.0
		else:
			ret = regex.sub("", res.output)
			logger.debug('Evaluating cleaned up expression: %s', ret)
			ret = ev.eval_prob(ret)
		logger.debug("PSI Scorer: Returning evaluated probability %s", ret)
		return ret
