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


import subprocess
import time
import sys
import os
import signal


class Result:
	def __init__(self,output,time,error=""):
		self.output=output
		self.time=time
		self.error=error.strip() # remove whitespaces on both sides of error
		
	def __str__(self):
		ret = "[\n"
		if self.output != "":
			ret += "OUTPUT:\n" + self.output + "\n"
		if self.error != "":
			ret += "ERROR:\n" + self.error + "\n"
		ret += "ELAPSED[s]:\n" + str(self.time) + "\n]"
		return ret


class MySubProcess:
	def __init__(self, command, timeout=None):
		signal.signal(signal.SIGTERM, self.sigterm)
		self.command = command
		if timeout is None:
			timeout = float('inf')
		self.start = time.time()
		self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
		self.timeout = timeout
	
	def has_terminated(self, timeout=0):
		try:
			self.process.wait(timeout=timeout)
			return True
		except subprocess.TimeoutExpired as e:
				return False
	
	def wait_for_termination(self):
		while not self.has_terminated(1):
			if time.time()-self.start>=self.timeout:
				try:
					self.process.wait(timeout=0)
				except subprocess.TimeoutExpired as e:
						e.timeout=self.timeout
						self.kill()
						raise e
	
	def cleanup_result(self, res):
		return res
	
	def get_result(self):
		self.wait_for_termination()
		# prepare result
		output, err = self.process.communicate()
		end = time.time()
		output = output.decode("utf-8")
		err = err.decode("utf-8")
		res = Result(output, end-self.start, err)
	
		if self.process.returncode != 0:
			res.error = "runShell.py: Non-null return value (" + str(self.process.returncode) + ") for command " +\
						self.command + "\nPrevious errors from command itself:" + res.error
		return self.cleanup_result(res)
	
	def sigterm(self, signum=None, frame=None):
		self.kill()
		sys.exit(-9)
	
	def kill(self):
		if hasattr(self, 'process'):
			try:
				os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
			except ProcessLookupError:
				# process probably already terminated
				pass


# Throws a subprocess.TimeoutExpired exception after timeout seconds
def run(command, timeout=None):
	p = MySubProcess(command,timeout)
	return p.get_result()
