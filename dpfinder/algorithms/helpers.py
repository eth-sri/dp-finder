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


import numpy as np
import tensorflow as tf
import numpy.random as r
import math


# returns logs of P[LAP<x] and P[LAP>x]
def laplacian_cdf(x,scale,loc=0):
	with tf.name_scope("laplacian-cdf"):
		condition=tf.less(x,loc)
		p_below_if=math.log(0.5)+(x-loc)/scale
		p_below_then=tf.log(-tf.expm1(math.log(0.5)+(loc-x)/scale))
		p_below=tf.where(condition,p_below_if,p_below_then)
		p_above_if=tf.log(-tf.expm1(math.log(0.5)+(x-loc)/scale))
		p_above_then=math.log(0.5)+(loc-x)/scale
		p_above=tf.where(condition,p_above_if,p_above_then)
		return p_below,p_above


# returns P[EXP>=x]
def exponential_cdf_right(x,rate):
	with tf.name_scope("exponential-cdf"):
		return tf.exp(-rate*x)


def laplacian_pdf(x,scale,loc=0):
	with tf.name_scope("laplacian-pdf"):
		return -tf.log(2.0*scale)-tf.abs(x-loc)/scale


# returns an array of length array_size with n_hot "1"-entries
def get_n_hot(n_hot, array_size):
	assert(n_hot <= array_size)
	a=np.zeros(array_size, dtype=int)
	for n_flipped in range(n_hot):
		index = r.randint(0,array_size-n_flipped)
		i=nthWithProperty(a, index, lambda x: x == 0)
		a[i] = 1
	return a


# returns the index of the n-th (0-based) element that satisfies the property
def nthWithProperty(arr, n, prop):
	count = 0
	for i in range(len(arr)):
		if prop(arr[i]):
			if n == count:
				return i
			count += 1


def get_laplace(scale, n_samples):
	ret = np.random.laplace(0, scale, n_samples)
	ret = ret.astype(np.float64)
	return ret


def get_exponential(scale, n_samples):
	ret = np.random.exponential(scale=scale, size=n_samples)
	ret = ret.astype(np.float64)
	return ret


def tf_const(c):
	return tf.constant(c,dtype=tf.float64)


