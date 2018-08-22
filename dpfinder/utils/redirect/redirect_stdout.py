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


import sys, os
from contextlib import contextmanager
import threading
import select
import tempfile

self_dir = os.path.dirname(os.path.realpath(__file__))
log_dir = self_dir + "/logs"

# the pipe would fail for some reason if I didn't write to stdout at some point
# so I write a space, then backspace (will show as empty in a normal terminal)
sys.stdout.write(' \b')

# save a copy of stdout
stdout = os.dup(1)


@contextmanager
def redirect(output=print):
	with tempfile.NamedTemporaryFile(mode='r+', dir=log_dir) as logfile:
		pipe_out, pipe_in = os.pipe()

		# replace stdout with our write pipe
		os.dup2(pipe_in, 1)

		# check if we have more to read from the pipe
		def more_data():
			r, _, _ = select.select([pipe_out], [], [], 0)
			return bool(r)

		# read the pipe, writing to (former) stdout
		def write_pipe_to_stdout():
			while more_data():
				bytes = os.read(pipe_out, 1024)
				s = bytes.decode("utf-8")
				logfile.write(s)
				logfile.flush()

		done = False

		def read_loop():
			# rewrite the pipe out to stdout in a loop while the call is running
			while not done:
				write_pipe_to_stdout()
			# Finish the remnants
			write_pipe_to_stdout()
			os.close(pipe_in)
			os.close(pipe_out)

		t = threading.Thread(target=read_loop)
		t.start()

		try:
			yield
		finally:
			done = True
			t.join()  # wait for the thread to finish

			# put stdout back in place 
			os.dup2(stdout, 1)
			logfile.seek(0)
			for line in logfile:
				output(line.rstrip())
