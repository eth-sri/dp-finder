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
from dpfinder.searcher.searcher import Searcher
from dpfinder.algorithms.algorithms import Algorithm
from dpfinder.searcher.statistics.confidence_interval import get_confidence_interval
from dpfinder.utils.utils import my_to_str
from dpfinder.utils.timer import time_measure

n_opt_steps = 50
min_p = 1e-2


class TensorFlowSearcher(Searcher):

	def __init__(self, confirming, confirmer, min_n_samples, max_n_samples, confidence, eps_err_goal, alg: Algorithm):
		super().__init__(confirming, confirmer, alg)
		self.min_n_samples = min_n_samples
		self.n_samples = self.min_n_samples
		self.max_n_samples = max_n_samples
		self.confidence = confidence
		self.eps_err_goal = eps_err_goal
		self.alg = alg

		# set seed for randomness
		np.random.seed(0)

		# build graph
		with time_measure('build_graph'):
			self.imp = alg.get_tensorflow_implementation()
			self.imp.build_fresh_graph()
			self.imp.fresh_randomness(self.n_samples)
			with time_measure('init_optimizer'):
				logger.info("Started setting up optimizer")
				self.optimizer = self.imp.get_optimizer(n_opt_steps, min_p)
				logger.info("Finished setting up optimizer")

		# internal variables
		self.s = None

	def step_internal(self, s):
		if s % 2 == 0:
			with time_measure('random'):
				self.random_start(s)
		else:
			with time_measure('optimize'):
				self.optimize(s)
		return self.s.a, self.s.b, self.s.o, self.s.eps

	def random_start(self, s):
		self.alg.set_random_start(self.imp)

		self.check_error()
		logger.data('n_samples', self.n_samples)
		logger.info("Result after step (random,%s):\n%s", s, self.current_state())
		return self.s.eps

	def current_state(self):
		a_str = my_to_str(self.s.a)
		b_str = my_to_str(self.s.b)
		o_str = my_to_str(self.s.o)
		return "\ta={}\n\tb={}\n\to={}\n\teps={}".format(a_str, b_str, o_str, self.s.eps)

	def check_error(self):
		while True:
			self.imp.fresh_randomness(self.n_samples)
			self.s = self.imp.run_all()
			error = get_confidence_interval(self.s.pas, self.s.pbs, self.confidence, self.eps_err_goal)

			if error * 4 < self.eps_err_goal and self.n_samples / 1.4 >= self.min_n_samples:
				self.n_samples = int(self.n_samples / 1.4)
				logger.debug("Error too small:%s, decreasing size of network to %s...", error, self.n_samples)
			elif error > self.eps_err_goal and self.n_samples < self.max_n_samples:
				self.n_samples = self.n_samples * 2
				logger.debug("Error too large:%s, increasing size of network to %s...", error, self.n_samples)
			elif math.isnan(error):
				logger.warning("Error is nan, resetting size of network to %s...", self.n_samples)
				break
			else:
				break
		logger.info("Tensorflow: eps=%s+-%s", self.s.eps, error)

	def optimize(self, s):
		if np.isnan(self.s.a).any() or np.isnan(self.s.d).any() or np.isnan(self.s.o).any():
			logger.warning("Parameters contain 'nan', will not run gradient descent. Returning 0.0 instead...")
		elif np.isnan(self.s.eps):
			logger.warning("eps is 'nan', will not run gradient descent. Returning 0.0 instead...")
		elif np.isinf(self.s.eps):
			logger.warning("eps is already 'inf', will not run gradient descent....")
		else:
			logger.debug("Starting optimization step")
			self.imp.minimize(self.optimizer)
			logger.debug("Finished optimization step")
			self.check_error()

		logger.data('n_samples', self.n_samples)
		logger.info("Result after step (optimized,%s):\n%s", s, self.current_state())

		return self.s.eps

	def close(self):
		self.imp.close()