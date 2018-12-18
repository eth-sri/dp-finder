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


import importlib
from abc import ABC, abstractmethod
import os
import numpy as np
from typing import Tuple
import tensorflow as tf

from dpfinder.utils.utils import arr_to_str
from dpfinder.algorithms.tf_implementations.implementation import TensorFlowImplementation

# precisions
precision_tf = tf.float64
precision_np = np.float64


class Algorithm(ABC):

	def __init__(self):
		class_name = self.__class__.__name__
		self.name = class_name[0].lower() + class_name[1:]

	@abstractmethod
	def get_random_input(self) -> Tuple[np.ndarray, np.ndarray]:
		"""
		Return a tuple of (a,d), where a is the original database,
		and d characterizes the distance to the neighbouring database
		"""
		pass

	@abstractmethod
	def get_random_output(self, a, b):
		"""

		:param a:
		:param b:
		:return: a random output to check for (can also be multiple values that parametrize an output set)
		"""
		pass

	def get_psi_filename(self):
		"""Return the filename of the PSI code"""
		return self.name + '.psi'

	def get_psi_base_script(self):
		"""Return an implementation in PSI, as a string"""
		here = os.path.dirname(__file__)
		psi_file_location = os.path.join(here, './psi_implementations/' + self.get_psi_filename())
		with open(psi_file_location, 'r') as file:
			psi_base_script = file.read()
		return psi_base_script

	def get_psi_script(self, a, o):
		psi_script = self.get_psi_base_script()
		psi_script = psi_script.replace("[$A]", arr_to_str(a))
		psi_script = psi_script.replace("[$O]", arr_to_str(o))
		return psi_script

	def get_params(self):
		return self

	def get_tensorflow_implementation(self) -> TensorFlowImplementation:
		i = importlib.import_module('.tf_implementations.imps.' + self.name, __package__)
		class_name = self.name.capitalize()[0] + self.name[1:] + 'Impl'
		class_ = getattr(i, class_name)
		return class_(self.get_params())

	def set_random_start(self, impl: TensorFlowImplementation):
		a_init, d_init = self.get_random_input()
		o_init = self.get_random_output(a_init, a_init + d_init)
		impl.initialize(a_init, d_init, o_init)


def get_algorithm(name, *args) -> Algorithm:
	i = importlib.import_module('.algs.' + name, __package__)
	class_name = name.capitalize()[0] + name[1:]

	class_ = getattr(i, class_name)
	return class_(*args)


def get_algorithm_larger_dict(name, d) -> Algorithm:
	"""Requires d to contain at least all arguments require to construct
	the algorithm referred to by name"""

	# get constructor
	i = importlib.import_module('.algs.' + name, __package__)
	class_name = name.capitalize()[0] + name[1:]
	class_ = getattr(i, class_name)
	constructor = getattr(class_, '__init__')

	# find arguments, extract them from d
	code = constructor.__code__
	n_arguments = code.co_argcount
	args = {}
	for v in code.co_varnames[1:n_arguments]:
		args[v] = d[v]

	return class_(**args)
