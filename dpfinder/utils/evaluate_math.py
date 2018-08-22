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


import numexpr
import logging

import re


def process_exp(m):
	base = m.group(1)
	exp = m.group(2)
	# l = min(len(v1),len(v2))
	# v1 = v1[:-l+1] + "." + v1[-l+1:]
	# v2 = v2[:-l+1] + "." + v2[-l+1:]
	# print(v1)
	return base+"**"+"(-"+exp+")"


def eval(expr):
	try:
		logging.debug('Evaluating %s', expr)
		expr = expr.replace("E", "2.71828182845904523536028747135266249775").replace("^", "**")
		
		# avoid overflows
		exp = r"1/([\-0-9\.]*)\*\*\((-?[0-9]*/-?[0-9]*)\)"
		exp = re.compile(exp)
		expr = exp.sub(process_exp,expr)

		logging.debug('Evaluating %s using numexpr', expr)
		ret = numexpr.evaluate(expr)
		ret = float(ret)
		logging.debug('Returning evaluated expression evaluated to %s', ret)
		return ret
	except Exception as e:
		raise Exception("Exception when evaluating "+expr) from e


def eval_prob(expr):
	try:
		return eval(expr)
	except Exception as err:
		logging.warning("!!Warning!!:An exception occurred while computing the probability. Returning 'nan'...")
		logging.warning(err)
		return float('nan')
