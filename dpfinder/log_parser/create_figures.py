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


import glob
import os
import sys
import argparse
from typing import List
import numpy as np

from dpfinder.log_parser.parser import get_parsed, Parser, EpsType
from dpfinder.log_parser.my_box_plot import MyBoxPlot, get_latex_formatter
import matplotlib  # must be after the import of MyBoxPlot
from matplotlib import pyplot as plt  # must be after the import of MyBoxPlot
from matplotlib import ticker


def parse_logs(file_pattern) -> List[Parser]:
	ps = []
	for filename in sorted(glob.glob(file_pattern)):
		if filename.endswith("data.log"):
			p = get_parsed(filename)
			ps.append(p)

	def get_name_for_sorting(p: Parser):
		n = p.get_short_alg_name()
		if n == 'AT':
			n = 'AT6'
		return n

	ps.sort(key=get_name_for_sorting)
	return ps


dir_path = os.path.dirname(os.path.realpath(__file__))
above_range = [0.30, 1.6]
below_range = [0.0, 0.22]
font_size = 12
default_height_ratios = [1.6, 10]


def compare_random_optimized(ps: List[Parser]):
	"""Compares the epsilon of randomly picked witnesses to optimized witnesses"""

	# prepare data
	bounds = [p.get_bound() for p in ps]
	data = [[p.get_confirmed_eps(EpsType.RAND), p.get_confirmed_eps(EpsType.OPT)] for p in ps]
	labels = [p.get_short_alg_name() for p in ps]
	sublabels = ['rand', 'opt']
	# plot
	pl = MyBoxPlot([above_range, below_range], font_size=font_size, height_ratios=default_height_ratios)
	pl.plot(data, labels, sublabels, bounds)
	plt.savefig(os.path.join(dir_path, 'figures/rand_vs_opt.pdf'), bbox_inches='tight')
	plt.clf()


def analyse_data(ps: List[Parser]):
	# analyse data
	for p in ps:
		eps_rand = p.get_confirmed_eps(EpsType.RAND)
		eps_opt = p.get_confirmed_eps(EpsType.OPT)
		name = p.get_alg_name()
		improvement = (np.median(eps_opt) - np.median(eps_rand)) / np.median(eps_rand)

		print('Algorithm:', name)

		# IMPROVEMENT

		print("\tImprovement of median:", improvement)
		if np.any(np.isinf(eps_rand)):
			print("\tRand returned inf:\t", np.sum(np.isinf(eps_rand)))
		if np.any(np.isinf(eps_opt)):
			print("\tOpt returned inf:\t", np.sum(np.isinf(eps_opt)))

		if np.any(np.isnan(eps_rand)):
			print("\tRand returned nan:\t", np.sum(np.isnan(eps_rand)))
		if np.any(np.isnan(eps_opt)):
			print("\tOpt returned nan:\t", np.sum(np.isnan(eps_opt)))

		# FINAL RESULT

		print("\tBest values:", -np.sort(-eps_opt)[:5])

		# TIMING
		time_rand = p.get_random_time()
		time_opt = p.get_optimize_time()

		median_rand = np.median(time_rand)
		median_opt = np.median(time_opt)
		median_sum = np.median(time_rand + time_opt)
		average_sum = np.average(time_rand + time_opt)
		max_sum = np.max(time_rand + time_opt)
		print("\tMedian of rand time:", median_rand)
		print("\tMedian of opt time:", median_opt)
		print("\tMedian of sum time:", median_sum / 60, 'min')
		print("\tAverage of sum time:", average_sum / 60, 'min')
		print("\tMax of sum time:", max_sum/60, 'min')

		median_time_ratio = np.median(time_opt / time_rand)
		print("\tMedian of opt time/rand time:", median_time_ratio)


def compare_empirical_confirmed(ps: List[Parser]):
	print('empirical-confirmed')
	# prepare data
	bounds = [p.get_bound() for p in ps]
	data = [[p.get_empirical_eps(EpsType.OPT), p.get_confirmed_eps(EpsType.OPT)] for p in ps]
	labels = [p.get_short_alg_name() for p in ps]
	sublabels = [r"$\hat{\epsilon}^{d}$", r"$\epsilon$"]

	# plot
	pl = MyBoxPlot(
		[above_range, below_range], rot_sub_labels=0, font_size=font_size, height_ratios=default_height_ratios)
	pl.plot(data, labels, sublabels, bounds)
	plt.savefig(os.path.join(dir_path, 'figures/est_vs_conf.pdf'), bbox_inches='tight')
	plt.clf()
	print('empirical-confirmed')


def plot_n_samples(ps: List[Parser]):
	# prepare data
	data = [[p.get_n_samples(EpsType.RAND), p.get_n_samples(EpsType.OPT)] for p in ps]
	labels = [p.get_short_alg_name() for p in ps]
	sublabels = ["rand", "opt"]

	n_samples = [v for p in ps for v in p.get_n_samples(EpsType.ALL)]

	# plot
	pl = MyBoxPlot(
		[[min(n_samples), max(n_samples)]],
		font_size=font_size,
		y_axis_formatter=get_latex_formatter(),
		y_axis_logscale=True)
	pl.plot(data, labels, sublabels, y_label='number of samples (logscale)')
	plt.savefig(os.path.join(dir_path, 'figures/n_samples.pdf'), bbox_inches='tight')
	plt.clf()


def plot_times(ps: List[Parser]):
	matplotlib.rcParams.update({'font.size': font_size})
	plt.figure(frameon=False)

	times_rand = [np.average(p.get_random_time()) for p in ps]
	times_opt = [np.average(p.get_optimize_time()) for p in ps]
	times_psi = [np.average(p.get_psi_time()) for p in ps]
	times = [times_rand, times_opt, times_psi]
	n = len(ps)
	ind = np.arange(n)
	width = 1.0 / n
	bars = []
	for i in range(3):
		bar = plt.bar(ind + i * width, times[i], width, bottom=10)
		bars.append(bar)

	ax = plt.gca()
	ax.set_yscale('log')

	ax.spines['top'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	ax.set_ylabel('time [s] (logscale)')
	ax.set_xticks(ind + width)
	ax.tick_params(bottom='off')
	names = [p.get_short_alg_name() for p in ps]
	ax.set_xticklabels(names, rotation=30)

	ax.legend([bar[0] for bar in bars], ('Sampling', 'Optimization (SLSQP)', 'Confirmation (PSI)'), frameon=False)

	plt.savefig(os.path.join(dir_path, 'figures/times.pdf'), bbox_inches='tight')
	plt.clf()


path = os.path.dirname(os.path.abspath(__file__))
default_commit = '86050a9'
default_logs = os.path.join(path, '..', 'runners', 'logs', 'tf_runner', '*' + default_commit)


def create_figures(log_dir):
	# parse logs
	pattern = os.path.join(log_dir, '*data.log')
	ps = parse_logs(pattern)

	# call all functions
	for f in [compare_random_optimized, compare_empirical_confirmed, analyse_data, plot_times, plot_n_samples]:
		f(ps)


def main(argv):
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument(
		'--logs', action="store", default=default_logs, type=str,
		help='The directory containing the logs, from which we produce figures'
	)

	args = parser.parse_args(argv)
	create_figures(args.logs)


if __name__ == "__main__":
	main(sys.argv[1:])
