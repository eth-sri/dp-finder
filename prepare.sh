#!/bin/bash
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


BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo """
########################
# STARTING PREPARATION #
########################
"""

echo -e "\nCOMPILING ratio\n"
cd "$BASEDIR/dpfinder/searcher/statistics/ratio"
make lib
cd -

echo -e "\nCOMPILING rounder\n"
cd "$BASEDIR/dpfinder/utils/tf/rounder"
make lib
cd -

export PYTHONPATH="$BASEDIR"
# ensure DP-Finder only occupies first GPU (if machine has a GPU)
export CUDA_VISIBLE_DEVICES=0

if [ ! -d "$BASEDIR/env" ]; then
	# to fix "unsupported locale setting"
	# export LC_ALL="en_US.UTF-8"
	# export LC_CTYPE="en_US.UTF-8"

	echo -e "\nINSTALLING virtualenv\n"
	# Alternative:
	# python3 -m venv "$BASEDIR/env"
	virtualenv -p python3 "$BASEDIR/env"
	source "$BASEDIR/env/bin/activate"

	PIP="pip3 -q"
	$PIP install numexpr # to evaluate math in the form of strings
	$PIP -q install numpy
	$PIP -q install scipy
	$PIP -q install nose
	$PIP -q install matplotlib

	if [ -x "$(command -v nvidia-smi)" ]; then
		$PIP install tensorflow-gpu==1.9.0
	else
		echo "WARNING: INSTALLING TENSORFLOW FOR CPU (not for GPU)" >&2
		$PIP install tensorflow==1.9.0
	fi
else
	source "$BASEDIR/env/bin/activate"
fi

# versions
# python3 -V; python3 -c 'import tensorflow as tf; print("tensorflow",tf.__version__); import numpy; print("numpy",numpy.version.version); import scipy; print("scipy",scipy.__version__)'

echo """
########################
# FINISHED PREPARATION #
########################
"""
