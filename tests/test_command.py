import pytest
import configparser
import os
from vim_pck import command
from vim_pck import utils


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return(tmpdir_factory)


@pytest.fixture()
def write_conf_1(temp_dir, monkeypatch):
    """ Initial setup for the test_install_cmd_1 test function

    1. Write a vimpck configuration file
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'install_cmd'
    basepath = temp_dir.mktemp(dirtest)
    confpath = basepath.join('config.ini')
    config['DEFAULT'] = {'pack_path': basepath}
    config['https://github.com/tpope/vim-commentary'] = \
        {'package': 'common',
            'type': 'start'}
    config['https://github.com/tpope/vim-dispatch'] = \
        {'package': 'common',
            'type': 'opt'}
    config['https://github.com/mustache/vim-mustache-handlebars'] = \
        {'package': 'filetype',
            'type': 'start'}
    config['https://github.com/altercation/vim-colors-solarized'] = \
        {'package': 'colors',
            'type': 'start'}
    with open(confpath, 'w') as configfile:
        config.write(configfile)
    monkeypatch.setitem(os.environ, 'VIMPCKRC', str(confpath))
    print(os.environ["VIMPCKRC"])


@pytest.fixture()
def write_conf_2(temp_dir, monkeypatch):
    """ Initial setup for the test_install_cmd_2 test function

    1. Write a vimpck configuration file
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'install_cmd'
    basepath = temp_dir.mktemp(dirtest)
    confpath = basepath.join('config.ini')
    config['DEFAULT'] = {'pack_path': basepath}
    config['https://github.com/tpope/vim-commentary'] = \
        {'package': 'common',
            'type': 'start'}
    config['https://github.com/tpope/vim-dispatch'] = \
        {'package': 'common',
            'type': 'opt'}
    config['https://github.com/mustache/vim-mustache-handlebars'] = \
        {'package': 'filetype',
            'type': 'start'}
    config['https://github.com/altercation/vim-colors-solarized'] = \
        {'package': 'colors',
            'type': 'start'}
    config['https://github.com/neomake/neomake'] = \
        {'package': 'linter'}
    with open(confpath, 'w') as configfile:
        config.write(configfile)
    monkeypatch.setitem(os.environ, 'VIMPCKRC', str(confpath))
    print(os.environ["VIMPCKRC"])


def test_install_cmd_1(write_conf_1, temp_dir):
    """Test vim_pck.command.install_cmd()

    Clone some repository from a configuration file defined by the
    write_conf_1 fixture and then check that the directory structure
    correspond to the one specified in the configuration file.
    ex: is "/common/vim-commentary" (from the configuration file) included
    somewhere where the install_cmd have cloned the repository into.
    """

    config = configparser.ConfigParser()
    config.read(os.environ["VIMPCKRC"])
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
    plug_names = [os.path.basename(i) for i in plug_urls]
    pack_path = config['DEFAULT']['pack_path']

    command.install_cmd()
    installed_plug = utils.instplug(pack_path, 3)

    if not set(installed_plug).difference(plug_names):
        assert 1
    else:
        assert 0


def test_install_cmd_2(write_conf_2, temp_dir):
    """Test vim_pck.command.install_cmd()

    Similar to test_install_cmd_1 but add an entry (neomake plugin) with
    missing key value pair and test if the directory structure for the absence
    of neomake and the presence of the remaining plugin which have a valid
    configuration entry
    """

    config = configparser.ConfigParser()
    config.read(os.environ["VIMPCKRC"])
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
    plug_names = [os.path.basename(i) for i in plug_urls]
    pack_path = config['DEFAULT']['pack_path']

    command.install_cmd()
    installed_plug = utils.instplug(pack_path, 3)

    diff = set(installed_plug).symmetric_difference(plug_names)
    if ('neomake' in diff) and (len(diff) == 1):
        assert 1
    else:
        assert 0


def test_install_cmd_3(write_conf_1, temp_dir):
    """Test vim_pck.command.install_cmd()

    Install some plugin and reinstall them. Plugin already installed should not
    be reinstalled.
    """

    config = configparser.ConfigParser()
    config.read(os.environ["VIMPCKRC"])
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
    plug_names = [os.path.basename(i) for i in plug_urls]
    pack_path = config['DEFAULT']['pack_path']

    command.install_cmd()
    installed_plug = utils.instplug(pack_path, 3)

    if not set(installed_plug).difference(plug_names):
        assert 1
    else:
        assert 0

    command.install_cmd()
    installed_plug = utils.instplug(pack_path, 3)

    if not set(installed_plug).difference(plug_names):
        assert 1
    else:
        assert 0
