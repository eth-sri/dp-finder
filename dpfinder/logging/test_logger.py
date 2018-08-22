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
import warnings
import json

from dpfinder import logging
from dpfinder.utils.utils import get_file_content


class TestLogger(unittest.TestCase):
	def test_logger(self):
		# ignore warnings
		warnings.simplefilter("ignore")

		# log something
		log_file = logging.get_log_file('test_logger') + '_info'
		logging.set_logfile(log_file)
		logging.info("ABCD")
		logging.shutdown()

		# check logfile
		success = 'ABCD' in get_file_content(log_file + '_info.log')
		self.assertTrue(success)

	def test_data(self):
		log_file = logging.get_log_file('test_logger') + '_data'
		logging.set_logfile(log_file)
		logging.data('key', 2)
		logging.info('ABCD')
		logging.shutdown()

		# check
		content = get_file_content(log_file + '_data.log')
		d = json.loads(content)
		self.assertEquals(d['key'], 2)
		self.assertTrue('ABCD' not in content)


if __name__ == '__main__':
	unittest.main()
