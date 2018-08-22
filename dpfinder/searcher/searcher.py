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


from typing import Tuple
from abc import ABC, abstractmethod

from dpfinder.logging import logger
from dpfinder.algorithms.algorithms import Algorithm


class Searcher(ABC):

	def __init__(self, confirming, confirmer, alg: Algorithm):
		self.confirming = confirming
		self.confirmer = confirmer
		self.alg = alg

		# initialize internal values
		self.next_step = 0

		self.a = None
		self.b = None
		self.o = None
		self.eps = None

		self.best_a = None
		self.best_b = None
		self.best_o = None
		self.best_eps = 0

	# SEARCH

	def search(self, max_steps):
		logger.info('Starting search for %s', self.alg.name)
		logger.data('algname', self.alg.name)
		for s in range(0, max_steps):

			logger.info('Step %s start', s)
			self.a, self.b, self.o, self.eps = self.step(s)
			logger.info('Step %s end', s)

			logger.info('eps:%s', self.eps)
			logger.data('eps-empirical', self.eps)

			if self.confirming == 10:
				self.confirm(self.a, self.b, self.o)

			if self.eps > self.best_eps:
				self.best_a = self.a
				self.best_b = self.b
				self.best_o = self.o
				self.best_eps = self.eps

		logger.info('Finished search')
		logger.info('Best eps:%s', self.best_eps)

		if self.confirming == 5:
			logger.info('Confirming best eps...')
			self.confirm(self.best_a, self.best_b, self.best_o)

		return self.best_eps

	def step(self, s):
		a, b, o, eps = self.step_internal(s)
		return a, b, o, eps

	@abstractmethod
	def step_internal(self, s) -> Tuple:
		""""
		s: we are in the s-th step
		Returns next a,b,o,eps"""
		pass

	# OTHERS

	def confirm(self, a, b, o):
		eps_confirmed = self.confirmer.score(a, b, o)
		logger.info("eps according to confirmer:%s", eps_confirmed)
		logger.data('eps-confirmed', eps_confirmed)
		return eps_confirmed

	def close(self):
		# usually, no action is necessary
		return
