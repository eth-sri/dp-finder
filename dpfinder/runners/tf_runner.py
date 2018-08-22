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


import sys
import argparse

from dpfinder.runners.runner import Runner, get_log_dir
from dpfinder.searcher.search import get_args_parser
from dpfinder.log_parser.create_figures import create_figures


def run(args):
	log_dir = get_log_dir(__file__)
	for alg in [
		'aboveThreshold', 'alg1', 'alg2', 'alg3', 'alg4', 'alg5',
		'expMech', 'reportNoisyMax', 'sum']:
		args.alg = alg
		r = Runner(args, __file__)
		r.run()

	# create figures based on logs
	create_figures(log_dir)


def main(argv):
	parser = get_args_parser()
	args = parser.parse_args(argv)
	run(args)


if __name__ == "__main__":
	main(sys.argv[1:])
