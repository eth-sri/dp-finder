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


MYPATH = $(shell pwd)

CC = g++
FLAGS = -fopenmp -lgomp -openmp -funroll-loops 
GMP = #-lgmpxx -lgmp
DFLAGS = -g -Wall -o0 -std=c++11 $(FLAGS)
CFLAGS  = -Wall -std=c++11 -o3 $(FLAGS)

FILES = ratio_cdf.cpp

TARGET = ratio
TOMSTARGET = toms462

prog: toms462
	$(CC) $(DFLAGS) -DMYPATH="$(MYPATH)" -o $(TARGET) $(FILES) -ldl $(GMP)

run: prog
	./$(TARGET)

toms462: clean
	$(CC) $(CFLAGS) -fPIC -shared toms462.cpp -o lib$(TOMSTARGET).so

lib: clean toms462
	$(CC) $(CFLAGS) -fPIC -DMYPATH="$(MYPATH)" -shared $(FILES) -o lib$(TARGET).so $(GMP)

clean:
	rm -f *.so *.o
