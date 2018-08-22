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


import json
from enum import Enum
import numpy as np

from dpfinder.log_parser.algorithm_utils import shorten_alg_name, get_bound


class EpsType(Enum):
	ALL = 0
	OPT = 1
	RAND = 2

	@staticmethod
	def get_eps_type(l, eps_type):
		all = np.array(l)
		nans = np.isnan(all)
		all[nans] = 0

		opt = all[1::2]
		zeros = opt == 0
		all[1::2][zeros] = all[0::2][zeros]
		if eps_type == EpsType.ALL:
			return all
		elif eps_type == EpsType.RAND:
			return all[0::2]
		elif eps_type == EpsType.OPT:
			return all[1::2]
		else:
			assert False


class Parser:

	def __init__(self, logfile):
		self.logfile = logfile
		self.d = {}
		with open(self.logfile) as f:
			for line in f:
				d = json.loads(line)
				self.add_all(d)

	def add_all(self, d):
		for k, v in d.items():
			self.add(k, v)

	def add(self, key, value):
		self.ensure_key(key)
		self.d[key].append(value)

	def ensure_key(self, key):
		if key not in self.d:
			self.d[key] = []

	def get_empirical_eps(self, eps_type=EpsType.ALL):
		l = self.d['eps-empirical']
		l = np.array(l, dtype=np.float64)
		l = EpsType.get_eps_type(l, eps_type)
		return l

	def get_confirmed_eps(self, eps_type=EpsType.ALL):
		l = self.d['eps-confirmed']
		l = np.array(l, dtype=np.float64)
		return EpsType.get_eps_type(l, eps_type)

	def get_random_time(self):
		l = self.d['random']
		l = np.array(l, dtype=np.float64)
		return l

	def get_optimize_time(self):
		l = self.d['optimize']
		l = np.array(l, dtype=np.float64)
		return l

	def get_psi_time(self):
		l = self.d['scorer-time']
		l = np.array(l, dtype=np.float64)
		return l

	def get_alg_name(self):
		return self.d['algname'][0]

	def get_n_samples(self, eps_type=EpsType.ALL):
		l = self.d['n_samples']
		l = np.array(l, dtype=np.float64)
		return EpsType.get_eps_type(l, eps_type)

	def get_bound(self):
		short_name = self.get_short_alg_name()
		return get_bound(short_name)

	def get_short_alg_name(self):
		name = self.get_alg_name()
		return shorten_alg_name(name)


def get_parsed(logfile) -> Parser:
	p = Parser(logfile)
	return p
