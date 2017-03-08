# Vim Pck

[![Build Status](https://travis-ci.org/nicodebo/vim-pck.svg?branch=master)](https://travis-ci.org/nicodebo/vim-pck)

A command line tool to manage my vim plugin using the built-in package
feature of vim8. (see :help packages)

## Dependencies

* git
* python 3.6

## Installation

I like to install python command line programs in their own virtual environment
to not clutter the system wide package directory. `pipsi` make it very
conveniant to do so by automatically creating the venv and symlinking scripts
to `~/.local/bin`. If you don't use `pipsi`, you're missing out. Here are
[installation instructions](https://github.com/mitsuhiko/pipsi#readme).

Simply run:

`$ pipsi install git+https://github.com/nicodebo/vim-pck.git@master#egg=vimpck`

If your default python point to python2 you might have to specify the python
interpreter to use (not tested):

`$ pipsi install --python python3 git+https://github.com/nicodebo/vim-pck.git@master#egg=vimpck`

To update:

`$ pipsi uninstall vimpck`

`$ pipsi install git+https://github.com/nicodebo/vim-pck.git@master#egg=vimpck`

To uninstall:

`$ pipsi uninstall vimpck`

## How to use

### Configuration file

```dosini
; example vimpck configuration file
[DEFAULT]
;The built in package directory. See :help packages 
pack_path=~/.vim/pack
;pack_path= ~/.local/share/nvim/site/pack for neovim

[https://github.com/tpope/vim-commentary]
package = common
type = start

[https://github.com/tpope/vim-dispatch]
package = common
type = opt

[https://github.com/mustache/vim-mustache-handlebars]
package = filetype
type = start

[https://github.com/altercation/vim-colors-solarized]
package = colors
type = start
```
 
### Usage
 
To use it:

    `$ vimpck --help`

### File

* `config` : The main configuration file where the vim packages are
  specified. It's default location follow the [XDG specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) that is `$XDG_HOME_CONFIG/vimpck/config` or `~/.config/vimpck/config` if `XDG_HOME_CONFIG` is not set.

### Environement variable

* `VIMPCKRC`: override default configuration location (xdg standard)

   example : `export VIMPCKRC=/path/to/conf/name`

## TODO

- [x] vimpck install, install plugins from configuration file
- [ ] vimpck install -r <requirements>, restore a package directory. The
      requirements file comes from the vimpack freeze command herebelow.
- [ ] vimpck list, list installed plugins
- [ ] vimpck list --start, list autostarting plugins
- [ ] vimpck list --opt, list optional plugins
- [ ] vimpck upgrade, upgrade non freezed plugins
- [ ] vimpck upgrade <plugin>, upgrade a specific plugin
- [ ] vimpck upgrade -f, force upgrade all plugin no matter if they are
      freezed
- [ ] vimpck upgrade -f <plugin>, force upgrade a specific plugin
- [ ] use sqlite to store package info (installation date, last upgrade,
      current commit, description,…) ?
- [ ] vimpck sync, search for upgrade and display the new commits
- [ ] vimpck freeze, generate a configuration file that mirrors the current
  packages installation (directory, commit)
- [ ] vimpck clean, remove commented out/location changed plugins
- [ ] find a better way to update vimpck. (pypi repo ?)

## Note

* Project generated with
  [cookiecutter-python-cli](https://github.com/nvie/cookiecutter-python-cli)
