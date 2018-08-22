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

from dpfinder.logging import logger
from dpfinder.searcher.tf_searcher import TensorFlowSearcher
from dpfinder.algorithms.algorithms import get_algorithm_larger_dict
from dpfinder.scorer.psi_scorer import PSIScorer


def search(args):
	alg = get_algorithm_larger_dict(args.alg, args.__dict__)
	confirmer = PSIScorer(alg)

	searcher = TensorFlowSearcher(
		args.confirming,
		confirmer,
		args.min_n_samples,
		args.max_n_samples,
		args.confidence,
		args.eps_err_goal,
		alg)

	eps = searcher.search(args.n_steps)
	searcher.close()
	return eps


def main(argv):
	logger.set_logfile(filename=None)
	parser = get_args_parser()
	args = parser.parse_args(argv)
	search(args)


def get_args_parser(**defaults):
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--alg', action="store", default="aboveThreshold",
						help="The name of the algorithm to test. \
						See directory dpfinder/algorithms/algs for a list of all implemented algorithms.")
	parser.add_argument('--c', action="store", default=1, type=int, help="Meta-parameter for some of the algorithms")
	parser.add_argument('--array_size', action="store", default=4, type=int, help="Size of arrays to test")
	parser.add_argument('--confidence', action="store", default=0.999487, type=float,
						help="DP-Finder will increase the number of samples until this confidence is reached")
	parser.add_argument('--eps_err_goal', action="store", default=0.002, type=float,
						help="Acceptable error for epsilon (will increase number of samples until this error is reached)")
	parser.add_argument('--n_steps', action="store", default=100, type=int,
						help="Number of steps to run the search for (n/2 steps for random starts, n/2 steps for optimization)")
	parser.add_argument('--confirming', action="store", default=10, type=int,
						help='How often to confirm the obtained epsilon with PSI. 0:never,5:at the end,10:after every step')
	parser.add_argument('--min_n_samples', action="store", default=2000,
						help="Minimum number of samples to use for the estimate of epsilon")
	parser.add_argument('--max_n_samples', action="store", default=12484608,
						help="Maximum number of samples to use for the estimate of epsilon")

	parser.set_defaults(**defaults)
	return parser


if __name__ == "__main__":
	main(sys.argv[1:])
