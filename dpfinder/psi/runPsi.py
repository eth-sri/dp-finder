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


from . import runShell
import sys
import tempfile

psi_command = 'psi'
default_psi_flags = '--noboundscheck --dp --expectation --mathematica --raw'


def run_on_string(psi_script_content, psi_flags=None, timeout=None):
	with tempfile.NamedTemporaryFile(mode='w+t', suffix='.psi') as f:
		f.write(psi_script_content)
		f.flush()
		res = run(f.name, psi_flags, timeout)
		return res


def run(psi_script, psi_flags=None, timeout=None):
	if psi_flags is None:
		psi_flags = default_psi_flags
	res = runShell.run(psi_command + ' ' + psi_flags + ' ' + psi_script, timeout)
	res.output = res.output.rstrip()  # remove trailing whitespaces from output
	return res


def main(argv):
	psi_script = argv[0]
	res = run(psi_script)
	print(res)


if __name__ == "__main__":
	main(sys.argv[1:])
