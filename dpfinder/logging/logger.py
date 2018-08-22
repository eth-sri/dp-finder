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


import logging.config
import datetime
import os
import json
from logging import critical, error, warning, info, debug  # necessary for calls from the outside

from dpfinder.utils.utils import create_dir_if_not_exists

timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())

self_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = os.path.join(self_dir, 'logs', 'others')
log_file = None

# LOG LEVELS
# existing:
# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
DATA = 5
logging.addLevelName(DATA, "DATA")


def data(key, value):
	d = {key: value}
	return logging.log(DATA, json.dumps(d))


def shutdown(handler_list=[]):
	logging.shutdown(handler_list)


called = False


def get_log_dir(label=None):
	if label is None:
		return log_dir
	else:
		return os.path.join(log_dir, label)


def get_log_file(label=None):
	d = get_log_dir(label)
	return os.path.join(d, timestamp)


def set_logfile(filename=None, weak=False):
	global called
	global log_file
	if called and weak:
		return
	called = True

	console_loglevel = 'WARNING'
	if filename is None:
		filename = os.path.join(log_dir, timestamp)
		console_loglevel = 0

	log_file = filename
	parent = os.path.dirname(log_file)
	create_dir_if_not_exists(parent)

	print("Saving logs to", log_file)

	default_logging = {
		'version': 1,
		'formatters': {
			'standard': {
				'format': '%(asctime)s [%(levelname)s]: %(message)s',
				'datefmt': '%Y-%m-%d_%H-%M-%S'
			},
			'minimal': {
				'format': '%(message)s'
			},
		},
		'filters': {
			'onlydata': {
				'()': OnlyData
			}
		},
		'handlers': {
			'default': {
				'level': console_loglevel,
				'formatter': 'standard',
				'class': 'logging.StreamHandler',
			},
			'fileinfo': {
				'level': 'INFO',
				'formatter': 'standard',
				'filename': log_file + '_info.log',
				'mode': 'w',
				'class': 'logging.FileHandler',
			},
			'filedebug': {
				'level': 'DEBUG',
				'formatter': 'standard',
				'filename': log_file + '_debug.log',
				'mode': 'w',
				'class': 'logging.FileHandler',
			},
			'filedata': {
				'level': 'DATA',
				'formatter': 'minimal',
				'filename': log_file + '_data.log',
				'mode': 'w',
				'class': 'logging.FileHandler',
				'filters': ['onlydata']
			}
		},
		'loggers': {
			'': {
				'handlers': ['default', 'fileinfo', 'filedebug', 'filedata'],
				'level': 0
			}
		}
	}
	logging.config.dictConfig(default_logging)


class OnlyData(logging.Filter):

	def filter(self, record):
		# print(record.__dict__)
		return record.levelno == DATA
