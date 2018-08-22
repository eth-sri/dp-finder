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



def shorten_alg_name(name):
	if name is None:
		return None
	elif name == "reportNoisyMax":
		return "noisyMax"
	elif name == "alg1":
		return "AT1"
	elif name == "alg2":
		return "AT2"
	elif name == "alg3":
		return "AT3"
	elif name == "alg4":
		return "AT4"
	elif name == "alg5":
		return "AT5"
	elif name == "aboveThreshold":
		return "AT"
	else:
		return name


def get_bound(short_name):
	d = {
		"noisyMax": 0.1,
		"expMech": 0.1,
		"AT1": 0.1,
		"AT2": 0.1,
		"AT3": 0.2,
		"AT4": (1 + 6) / 4 * 0.1,
		"AT5": float('inf'),
		"AT": 0.45,
		"sum": 0.1
	}
	return d[short_name]
