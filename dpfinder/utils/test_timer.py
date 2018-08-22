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


import unittest
import time
import json

from dpfinder.utils.timer import Timer, time_measure
from dpfinder import logging
from dpfinder.utils.utils import get_file_content


@Timer('mykey')
def sleep(n):
	time.sleep(n)


class TestTimer(unittest.TestCase):

	def test_timer_decorator(self):
		log_file = logging.get_log_file('TestTimer') + '_decorator'
		logging.set_logfile(log_file)
		sleep(0.5)
		logging.shutdown()

		content = get_file_content(log_file+'_data.log')

		d = json.loads(content)
		self.assertAlmostEqual(0.5, d['mykey'], 1)

	def test_timer_context_manager(self):
		log_file = logging.get_log_file('TestTimer') + '_context_manager'
		logging.set_logfile(log_file)
		logging.shutdown()

		with time_measure('mykey2'):
			time.sleep(0.5)

		content = get_file_content(log_file+'_data.log')
		d = json.loads(content)
		self.assertAlmostEqual(0.5, d['mykey2'], 1)


if __name__ == '__main__':
	unittest.main()
