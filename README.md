# DP-Finder

DP-Finder is a system that automatically derives lower bounds on the differential privacy enforced
by algorithms.

This repository contains the code used for the experiments in the paper [XX](https://www.sri.inf.ethz.ch/papers/XX).


## Setup

To install DP-Finder, you can use docker or install it locally. Before starting, clone this repository and navigate to the directory of this README file.

### Docker

For a simple (but less efficient) setup using docker, run

```shell
$ cd dp-finder/docker
$ make launch # build and run the docker image
[sudo] password for user: *************
```

### Locally

Alternatively, you can set up DP-Finder on your local machine.
The main requirements are
```shell
$ sudo apt-get install python3 python3-pip python3-tk libboost-all-dev
$ pip3 install virtualenv
```

In addition, the DP-Finder requires [PSI](https://github.com/eth-sri/psi) (to confirm found violations exactly).
Make sure that PSI can be accessed by running `psi`, by adding it to `/usr/local/bin`:

```shell
ln -s -f "/opt/psi/psi" "/usr/local/bin"
```

See the [Dockerfile](./docker/Dockerfile) for all relevant packages on for how to install PSI.
In case of issues with the setup, also see the [preparation script](./prepare.sh) (which is automatically run when you run `./test.sh` or `./run.sh`), which contains some optional commands that may fix your errors.


## Getting Started

Before running any commands, prepare the environment (sets up the PYTHONPATH, compiles dependencies, etc) by running

```shell
root@febda6ac8a18:/implementation# source ./prepare.sh
```

### Testing the build

To run the unittests of DP-Finder, run

```shell
root@febda6ac8a18:/implementation# ./test.sh
```

This should take around 10 minutes.

### Finding lower bounds

To find lower bounds for the encoded algorithms, run

```shell
root@febda6ac8a18:/implementation# ./run.sh
```

The runner generates plots, which are saved in [./dpfinder/log_parser/figures](./dpfinder/log_parser/figures).
The runtime of this script depends on your machine (XX).

### Running DP-Finder on a single algorithm

```shell
root@febda6ac8a18:/implementation# python3 dpfinder/searcher/search.py --alg aboveThreshold
```

To get a description of all parameters to dp-finder, run
````shell
root@febda6ac8a18:/implementation# python3 dpfinder/searcher/search.py --help
````


## Citing This Framework

```
@inproceedings{
  XX
}
```

## Contributors

* [Benjamin Bichsel](https://www.sri.inf.ethz.ch/beni.php) benjamin.bichsel@inf.ethz.ch
* [Timon Gehr](https://www.sri.inf.ethz.ch/tg.php) timon.gehr@inf.ethz.ch
* [Dana Drachsler Cohen](https://www.sri.inf.ethz.ch/dana.php) dana.drachsler@inf.ethz.ch
* [Petar Tsankov](http://www.ptsankov.com/) petar.tsankov@inf.ethz.ch
* [Martin Vechev](https://www.sri.inf.ethz.ch/vechev.php) martin.vechev@inf.ethz.ch


## License and Copyright

* Copyright (c) 2018 [Secure, Reliable, and Intelligent Systems Lab (SRI), ETH Zurich](https://www.sri.inf.ethz.ch/)
* Licensed under the [MIT License](https://opensource.org/licenses/MIT)

