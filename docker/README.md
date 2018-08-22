This explains how to set up Docker.

# Prerequisite: Install docker

To install docker, follow the instructions on https://docs.docker.com/install/linux/docker-ce/ubuntu/.
Installing docker on Ubuntu 16.04 LTS requires these steps:

```sh
# Update the apt package index
sudo apt-get update
# Install packages to allow apt to use a repository over HTTPS
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# set up the repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update the apt package index
sudo apt-get update
# Install the latest version of Docker CE
sudo apt-get -y install docker-ce
```

# Using the docker image

To simply run the docker image, use `make run`.
All relevant commands are described in the [Makefile](Makefile).
