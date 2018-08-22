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


FROM ubuntu:16.04

# INSTALL dependencies
RUN apt-get update && apt-get install -y \
	python3 \
	python3-pip \
	python3-tk \
	libboost-all-dev
# install virtualenv
RUN pip3 install virtualenv

# INSTALL PSI
# dependencies
RUN apt-get update && apt-get install -y \
	git \
	wget \
	unzip
# download and setup psi (fix the version of PSI by commit hash)
RUN git clone https://github.com/eth-sri/psi /opt/psi \
	&& cd /opt/psi \
	&& git reset --hard 24d07f7aeb511de5ab2cf2147890022e052b31ba \
	&& ./dependencies.sh \
	&& ./build.sh \
	&& ln -s -f "/opt/psi/psi" "/usr/local/bin"

# PREPARE
# copy (only) relevant files
COPY ./implementation/prepare.sh /implementation/prepare.sh
COPY ./implementation/dpfinder/searcher/statistics/ratio /implementation/dpfinder/searcher/statistics/ratio
COPY ./implementation/dpfinder/utils/tf/rounder /implementation/dpfinder/utils/tf/rounder
# set up the virtual environment
RUN /implementation/prepare.sh

# COPY prepared host information onto image
COPY ./implementation /implementation

# when starting the container, navigate to the correct directory
ENTRYPOINT cd /implementation && /bin/bash
