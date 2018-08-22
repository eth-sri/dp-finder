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


import time
import datetime
import os

from dpfinder import logging
from dpfinder.searcher import search
from dpfinder.utils.utils import get_git_version, get_hostname

path = os.path.dirname(os.path.realpath(__file__))
timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
hostname = get_hostname()
git_version = get_git_version()
log_tag = timestamp + '_' + hostname + '_' + git_version


def get_log_dir(runner_file):
	log_label = os.path.basename(runner_file).replace(".py", "")
	log_dir = os.path.join(path, "logs", log_label, log_tag)
	return log_dir


class Runner:

	def __init__(self, args, runner_file):
		self.args = args

		# set logfile
		self.log_dir = get_log_dir(runner_file)
		summary = self.args_to_str()
		self.logfile = os.path.join(self.log_dir, summary)
		logging.set_logfile(self.logfile)

		# print content of file
		self.log_file_contents(runner_file)

	@staticmethod
	def log_file_contents(filename):
		with open(filename) as f:
			logging.info("=====" + filename + "=====:")
			logging.info(f.read())

	def args_to_str(self):
		d = self.args.__dict__
		keys = list(d.keys())
		keys.sort()
		elems = [key.replace("_", "-") + "_" + str(d[key]) for key in keys]
		return '_'.join(elems)

	def run(self):
		print("RUNNING", self.args.__dict__)
		logging.info("Running", self.args.__dict__)
		# running
		start = time.time()
		eps = search(self.args)
		end = time.time()
		total = end - start
		logging.info("Total time:%s", total)
		logging.info("Best eps:%s", eps)
		print("BEST EPS", eps)
