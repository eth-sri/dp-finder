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


import os
import datetime
import tensorflow as tf
from tensorflow.contrib.opt import ScipyOptimizerInterface

from dpfinder.utils.redirect.redirect_stdout import redirect
from dpfinder.logging import logger

# provide information on logging
path = os.path.dirname(os.path.abspath(__file__))
loading_timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
logs = os.path.join(path, "./logs/tensorflow", loading_timestamp)
logger.info("Run tensorboard using $ tensorboard --logdir=%s", logs)


class TensorFlowWrapper:

	def __init__(self, label):
		# logging
		timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
		log_dir = '{}_{}'.format(label, timestamp)
		self.log = os.path.join(logs, log_dir)

		# internal fields
		self.session = None
		self.merged = None
		self.writer = None

	def close(self):
		if hasattr(self, 'writer'):
			self.writer.close()
		if hasattr(self, 'session'):
			self.session.close()

	def build_fresh_graph(self, label, build_graph):
		"""
		build a fresh compute graph (resets the current graph)
		:param label: label of the value returned by build_network
		:param build_graph: function that builds the graph and returns a value to be monitered with tensorboard
		"""

		# cleanup
		tf.reset_default_graph()

		logger.info('Started building graph')

		# build graph
		value = build_graph()

		# tensorboard
		tf.summary.scalar(label, value)

		# prepare session
		self.session = tf.Session()
		self.merged = tf.summary.merge_all()

		# prepare logging
		self.writer = tf.summary.FileWriter(self.log + '/train', self.session.graph)

		logger.info('Finished building graph')

	def initialize(self, vars_dict, feed_dict=None):
		init = [tf.assign(var, initializer) for var, initializer in vars_dict.items()]
		self.run(init, feed_dict)

	def run(self, fetches, feed_dict=None):
		return self.session.run(fetches, feed_dict=feed_dict)

	@staticmethod
	def get_optimizer(loss, n_opt_steps, var_to_bounds, inequalities):
		options = {
			'maxiter': n_opt_steps,
			'disp': True, 'ftol': 1e-15
		}

		with tf.name_scope('optimizer'):
			optimizer = ScipyOptimizerInterface(
				loss,
				options=options,
				method='SLSQP',
				var_to_bounds=var_to_bounds,
				inequalities=inequalities
			)

		return optimizer

	def minimize(self, optimizer, feed_dict=None):
		with redirect(output=logger.debug):
			optimizer.minimize(self.session, feed_dict=feed_dict)
