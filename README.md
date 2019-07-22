# DP-Finder

DP-Finder is a system that automatically derives lower bounds on the differential privacy enforced
by algorithms.

This repository contains the code used for the experiments in the paper [https://www.sri.inf.ethz.ch/papers/ccs18-dpfinder.pdf](https://www.sri.inf.ethz.ch/papers/ccs18-dpfinder.pdf).

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
[...]
$ pip3 install virtualenv
[...]
$ sudo apt-get install texlive-full
[...]
```

In addition, the DP-Finder requires [PSI](https://github.com/eth-sri/psi) (to
confirm found violations exactly). Make sure that PSI can be accessed by running
`psi`, by adding it to `/usr/local/bin`. For example, assuming that `psi` was
installed to `/opt/psi/psi`, run:

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
The runtime of this script depends on your machine (expect <1day).

### Running DP-Finder on a single algorithm

```shell
root@febda6ac8a18:/implementation# python3 dpfinder/searcher/search.py --alg aboveThreshold
```

To get a description of all parameters to dp-finder, run

````shell
root@febda6ac8a18:/implementation# python3 dpfinder/searcher/search.py --help
````

## Adding more algorithms

To add a new algorithm `newAlg` for testing:

- Add `newAlg.py` to [./dpfinder/algorithms/tf_implementations/imps](./dpfinder/algorithms/tf_implementations/imps). The new file should contain a class `NewAlgImpl` that extends `TensorFlowImplementation` (see [aboveThreshold.py](./dpfinder/algorithms/tf_implementations/imps/aboveThreshold.py) for a reference).
- Add `newAlg.psi` to [./dpfinder/algorithms/psi_implementations](./dpfinder/algorithms/psi_implementations). See [aboveThreshold.psi](./dpfinder/algorithms/psi_implementations/aboveThreshold.psi) for a reference.
- Add `newAlg.py` to [./dpfinder/algorithms/algs](./dpfinder/algorithms/algs). The new file should contain a class `NewAlg` that extends `Algorithm` (see [aboveThreshold.py](./dpfinder/algorithms/algs/aboveThreshold.py) for a reference).

## Citing This Framework

```
@inproceedings{Bichsel:2018:DFD:3243734.3243863,
 author = {Bichsel, Benjamin and Gehr, Timon and Drachsler-Cohen, Dana and Tsankov, Petar and Vechev, Martin},
 title = {DP-Finder: Finding Differential Privacy Violations by Sampling and Optimization},
 booktitle = {Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security},
 series = {CCS '18},
 year = {2018},
 isbn = {978-1-4503-5693-0},
 location = {Toronto, Canada},
 pages = {508--524},
 numpages = {17},
 url = {http://doi.acm.org/10.1145/3243734.3243863},
 doi = {10.1145/3243734.3243863},
 acmid = {3243863},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {differential privacy, lower bounds, optimization, sampling},
} 
```

## Contributors

- [Benjamin Bichsel](https://www.sri.inf.ethz.ch/people/benjamin) benjamin.bichsel@inf.ethz.ch
- [Timon Gehr](https://www.sri.inf.ethz.ch/people/timon) timon.gehr@inf.ethz.ch
- [Dana Drachsler Cohen](https://www.sri.inf.ethz.ch/people/dana) dana.drachsler@inf.ethz.ch
- [Petar Tsankov](http://www.ptsankov.com/) petar.tsankov@inf.ethz.ch
- [Martin Vechev](https://www.sri.inf.ethz.ch/people/martin) martin.vechev@inf.ethz.ch

## License and Copyright

- Copyright (c) 2018 [Secure, Reliable, and Intelligent Systems Lab (SRI), ETH Zurich](https://www.sri.inf.ethz.ch/)
- Licensed under the [MIT License](https://opensource.org/licenses/MIT)
