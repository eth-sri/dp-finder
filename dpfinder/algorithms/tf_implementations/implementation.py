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


from abc import ABC, abstractmethod
import tensorflow as tf
import numpy as np
from typing import List

from dpfinder.utils.tf.tf_wrapper import TensorFlowWrapper
from dpfinder.logging import logger

# precision
precision_tf = tf.float64
precision_np = np.float64


class State:

	def __init__(self, a, b, d, o, est_a, est_b, pas, pbs, eps):
		self.a = a
		self.b = b
		self.d = d
		self.o = o
		self.est_a = est_a
		self.est_b = est_b
		self.pas = pas
		self.pbs = pbs
		self.eps = eps

	def __repr__(self):
		ret = "\ta:\t{}\n\tb:\t{}\n\td:\t{}\n\to:\t{}\n\teps:\t{}\n\tpa/pb:\t{}/{}".format(
			self.a, self.b, self.d, self.o, self.eps, self.est_a, self.est_b)
		return ret

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def get_list(self):
		return [self.a, self.b, self.d, self.o, self.est_a, self.est_b, self.pas, self.pbs, self.eps]


class TensorFlowImplementation(ABC):

	a_var = None; b_var = None; d_var = None; o_var = None
	randomness_placeholders = None; n_samples_placeholder = None
	est_a = None; est_b = None; pas = None; pbs = None
	eps = None; loss = None
	randomness = None; n_samples = None

	tf_wrapper = None

	def __init__(self, alg_name, input_shape, d_shape, output_shape, output_dtype):
		self.alg_name = alg_name
		self.input_shape = input_shape
		self.output_shape = output_shape
		self.d_shape = d_shape
		self.output_dtype = output_dtype

		self.o_var = None

	@abstractmethod
	def get_randomness(self, n_samples):
		pass

	@abstractmethod
	def estimate_internal(self, input, output):
		pass

	@abstractmethod
	def prepare_randomness_placeholders(self):
		pass

	@abstractmethod
	def get_var_to_bounds(self, a, d, o):
		pass

	def get_inequalities(self, a, d, o) -> List:
		return []

	@abstractmethod
	def get_b(self, a, d) -> List:
		pass

	def build_fresh_graph(self):
		# build graph
		logger.info("Started building graph for algorithm")
		self.tf_wrapper = TensorFlowWrapper(self.alg_name)
		self.tf_wrapper.build_fresh_graph('eps', self.build_graph_internal)
		logger.info("Finished building graph for algorithm")

	def build_graph_internal(self):
		"""Called internally upon construction. Do not call externally"""

		# create tensors
		self.a_var = tf.get_variable("a", shape=self.input_shape, dtype=precision_tf)
		self.d_var = tf.get_variable("d", shape=self.d_shape, dtype=precision_tf)
		self.o_var = tf.get_variable("o", shape=self.output_shape, trainable=False, dtype=self.output_dtype)

		self.b_var = self.get_b(self.a_var, self.d_var)

		# create placeholders
		self.n_samples_placeholder = tf.placeholder(precision_tf)
		self.prepare_randomness_placeholders()

		# build network
		with tf.name_scope("log-estimate-a"):
			self.est_a, self.pas = self.estimate(self.a_var, self.o_var)
			log_est_a = tf.log(self.est_a)
		with tf.name_scope("log-estimate-b"):
			self.est_b, self.pbs = self.estimate(self.b_var, self.o_var)
			log_est_b = tf.log(self.est_b)
		with tf.name_scope("eps"):
			self.eps = tf.abs(log_est_a - log_est_b)
		with tf.name_scope("loss"):
			self.loss = -self.eps

		return self.eps

	def estimate(self, input, output):
		"""
		:param input:
		:param output:
		:return: an estimate of the P[P(input)=output] averaging over the probability estimates using the entries in randomness
		"""
		p = self.estimate_internal(input, output)
		with tf.name_scope("prop-estimate"):
			ret = tf.reduce_mean(p)
		return ret, p

	def fresh_randomness(self, n_samples):
		self.n_samples = n_samples
		self.randomness = self.get_randomness(n_samples)

	def initialize(self, a_init, d_init, o_init):
		vars_dict = {self.a_var: a_init, self.d_var: d_init, self.o_var: o_init}
		vars_dict = {var: tf.constant(value) for var, value in vars_dict.items()}
		feed_dict = self.get_feed_dict()
		self.tf_wrapper.initialize(vars_dict, feed_dict)

	def get_feed_dict(self):
		return {**self.randomness, self.n_samples_placeholder: self.n_samples}

	def run(self, x):
		return self.tf_wrapper.run(x, self.get_feed_dict())

	def run_all(self):
		fetches = State(self.a_var, self.b_var, self.d_var, self.o_var,
						self.est_a, self.est_b, self.pas, self.pbs, self.eps).get_list()
		ret = self.run(fetches)
		return State(*ret)

	def close(self):
		self.tf_wrapper.close()

	def get_optimizer(self, n_opt_steps, min_p):
		var_to_bounds = self.get_var_to_bounds(self.a_var, self.d_var, self.o_var)
		inequalities = [self.est_a - min_p] + self.get_inequalities(self.a_var, self.d_var, self.o_var)
		optimizer = self.tf_wrapper.get_optimizer(self.loss, n_opt_steps, var_to_bounds, inequalities)
		return optimizer

	def minimize(self, optimizer):
		self.tf_wrapper.minimize(optimizer, self.get_feed_dict())
