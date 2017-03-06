# Vim Pck

[![Build Status](https://travis-ci.org/nicodebo/vim-pck.svg?branch=master)](https://travis-ci.org/nicodebo/vim-pck)

A command line tool to manage my vim plugin using the built-in package
feature of vim8. (see :help packages)

## Dependencies

* git
* python 3.6:
    - click
    - sh
    - tqdm

## Installation

I like to install python command line programs in their own virtual environment
to not clutter the system wide package directory and not break things. `pipsi`
make it very conveniant to do so by automatically creating the venv and
symlinking scripts to `~/.local/bin`. If you don't use `pipsi`, you're missing
out.  Here are
[installationinstructions](https://github.com/mitsuhiko/pipsi#readme).

Simply run:

`$ pipsi install git+https://github.com/nicodebo/vim-pck.git@master#egg=vimpck`

If your default python point to python2 you might have to specify the python
interpreter to use (not tested):

`$ pipsi install --python python3 git+https://github.com/nicodebo/vim-pck.git@master#egg=vimpck`

To update:

`$ pipsi upgrade vimpck`

To uninstall:

`$ pipsi uninstall vimpck`

## Usage

To use it:

    `$ vimpck --help`

## Note

* Template generated with
  [cookiecutter-python-cli](https://github.com/nvie/cookiecutter-python-cli)
