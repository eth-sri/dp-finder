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


HOSTFOLDER := ./implementation
IMAGENAME := dp-finder
CONTAINERNAME := $(IMAGENAME)-container

# all commands involving docker use sudo, which is typically required to use docker commands

# build the docker image
.PHONY: image
image: clean
	rsync -a ../ $(HOSTFOLDER)/ --exclude $(HOSTFOLDER) --filter=':- .gitignore'
	sudo docker build -t $(IMAGENAME) .

# launch a docker container using the image, which will provide a shell in the container
.PHONY: launch
launch: image clean-container
	sudo docker run -it --name $(CONTAINERNAME) $(IMAGENAME)

# run the unittests in the docker image
.PHONY: test
test: image clean-container
	sudo docker run --entrypoint /implementation/test.sh $(IMAGENAME)

# find lower bounds, in the docker image
.PHONY: run
run: image clean-container
	sudo docker run --entrypoint /implementation/run.sh $(IMAGENAME)

# cleanup folders
.PHONY: clean
clean:
	rm -rf $(HOSTFOLDER)

# remove the created docker container
.PHONY: clean-container
clean-container:
	sudo docker rm $(CONTAINERNAME) || true

