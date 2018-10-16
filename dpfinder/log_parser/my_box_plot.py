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


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import ticker
import math

# LATEX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def get_latex_formatter():

	def format_latex(x, pos=None):
		if x == 0:
			return '$0$'
		exponent = math.floor(math.log(x, 10))
		factor = x/10**exponent
		return '$' + str(factor) + '\cdot 10^{' + str(exponent) + '}$'

	return ticker.FuncFormatter(format_latex)


class MyBoxPlot:
	def __init__(
			self,
			ranges,
			font_size=12,
			rot_labels=30, rot_sub_labels=90,
			height_ratios=[1.0],
			y_axis_formatter=None,
			y_axis_logscale=False,
			figsize = None):

		self.ranges = ranges
		self.font_size = font_size
		self.rot_labels = rot_labels
		self.rot_sub_labels = rot_sub_labels
		self.height_ratios = height_ratios
		self.y_axis_formatter = y_axis_formatter
		self.y_axis_logscale = y_axis_logscale
		self.figsize = figsize

	def plot(self, data, labels, sublabels, bounds=None, y_label=None):
		"""

		:param bounds: list (length n) of bounds to draw as horizontal lines
		:param data: 3D list (nx2x?) of data to plot
		:return:
		"""
		n = len(labels)
		n_splits = len(self.ranges)

		matplotlib.rcParams.update({'font.size': self.font_size})
		fig, axes = plt.subplots(
			n_splits, n, sharey='row', frameon=False, gridspec_kw={'height_ratios': self.height_ratios}, figsize=self.figsize)
		fig.subplots_adjust(wspace=0, hspace=0.1)

		if n > 1 and n_splits > 1:
			axes = list(map(list, zip(*axes)))  # transpose axes
		elif n > 1:
			axes = [[ax] for ax in axes]
		else:
			axes = [axes]

		flattened_axes = [ax for axs in axes for ax in axs]

		if self.y_axis_logscale:
			for ax in flattened_axes:
				ax.set_yscale('log')

		if self.y_axis_formatter is not None:
			for ax in flattened_axes:
				ax.yaxis.set_major_formatter(self.y_axis_formatter)

		for axs, d, label in zip(axes, data, labels):
			for ax, range in zip(axs, self.ranges):
				ax.set_ylim(*range)

			for ax in axs:  # plot same data on both axes
				# ax.grid()
				ax.tick_params(bottom='off')
				ax.spines['top'].set_visible(False)
				# ax.spines['left'].set_visible(False)
				# ax.spines['right'].set_visible(False)
				ax.spines['bottom'].set_visible(False)

				ax.boxplot(d, widths=0.5, sym='+')
			# ax.yaxis.set_major_formatter(perc_formatter)

			for ax in axs:
				ax.tick_params(bottom='off', top='off', labeltop='off', labelbottom='off')

			below = axs[-1]
			below.xaxis.tick_bottom()
			below.tick_params(bottom='off', top='off', labelbottom='on')

			below.set_xticklabels(sublabels, rotation=self.rot_sub_labels)
			below.set_xlabel(label, rotation=self.rot_labels)

		if y_label is not None:
			axes[0][-1].set_ylabel(y_label)

		if bounds is not None:
			for axs, bound in zip(axes, bounds):
				for ax in axs:
					ax.axhline(bound)

		return fig