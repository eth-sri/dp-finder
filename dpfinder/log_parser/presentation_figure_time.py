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
from typing import List
import numpy as np

from dpfinder.log_parser.parser import Parser
from dpfinder.log_parser.create_figures import dir_path, parse_logs
import matplotlib  # must be after the import of MyBoxPlot
from matplotlib import pyplot as plt  # must be after the import of MyBoxPlot


font_size = 12


def plot_times(ps_precise: List[Parser], ps_unprecise: List[Parser]):
	matplotlib.rcParams.update({'font.size': font_size})
	fig = plt.figure(frameon=False, figsize=(6.7, 0.7*4.8))

	times_rand_prec = [np.average(p.get_random_time()) for p in ps_precise]
	times_opt_prec = [np.average(p.get_optimize_time()) for p in ps_precise]
	times_rand_unprec = [np.average(p.get_random_time()) for p in ps_unprecise]
	times_opt_unprec = [np.average(p.get_optimize_time()) for p in ps_unprecise]
	times = [times_rand_prec, times_opt_prec, times_rand_unprec, times_opt_unprec]
	n = len(ps_precise)
	ind = np.arange(n)
	width = 1.0 / n
	bars = []
	for i in range(4):
		bar = plt.bar(ind + i * width, times[i], width, bottom=1)
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
	names = [p.get_short_alg_name() for p in ps_precise]
	ax.set_xticklabels(names, rotation=30)

	ax.legend(
		[bar[0] for bar in bars],
		('Sampling ($2 \cdot 10^{-3}$)', 'Opt ($2 \cdot 10^{-3}$)', 'Sampling ($10^{-1}$)', 'Opt ($10^{-1}$)'),
		frameon=False)

	print(fig.get_size_inches())
	plt.savefig(os.path.join(dir_path, 'figures/times-presentation.pdf'), bbox_inches='tight')
	plt.clf()


path = os.path.dirname(os.path.abspath(__file__))
default_commit = '86050a9'
default_logs = os.path.join(path, '..', 'runners', 'logs', 'tf_runner', '*' + default_commit)


def parse_logs_from_commit(commit):
	log = os.path.join(path, '..', 'runners', 'logs', 'tf_runner', '*' + commit)
	pattern = os.path.join(log, '*data.log')
	ps = parse_logs(pattern)
	return ps


def main():
	ps_precise = parse_logs_from_commit('b876ef3')
	ps_unprecise = parse_logs_from_commit('e0685d2')

	plot_times(ps_precise, ps_unprecise)


if __name__ == "__main__":
	main()
