import pytest
import configparser
import os
from urllib.parse import urlparse
from vim_pck import command
from vim_pck import utils


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return(tmpdir_factory)


@pytest.fixture()
def write_conf_1(temp_dir):
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
    return(str(confpath))


@pytest.fixture()
def write_conf_2(temp_dir):
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
    return(str(confpath))


def test_install_cmd_1(write_conf_1, temp_dir):
    """Test vim_pck.command.install_cmd()

    Clone some repository from a configuration file defined by the
    write_conf_1 fixture and then check that the directory structure
    correspond to the one specified in the configuration file.
    ex: is "/common/vim-commentary" (from the configuration file) included
    somewhere where the install_cmd have cloned the repository into.
    """

    command.install_cmd(config=write_conf_1)

    installed_plug = utils.instplug(str(temp_dir.getbasetemp()), 4)

    config = configparser.ConfigParser()
    config.read(write_conf_1)
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
    for plug_url in plug_urls:
        plug_name = os.path.basename(urlparse(plug_url).path)
        plug_locrepo = os.path.join(config[plug_url]['package'],
                                    config[plug_url]['type'], plug_name)
        assert any(plug_locrepo in s for s in installed_plug)


def test_install_cmd_2(write_conf_2, temp_dir):
    """Test vim_pck.command.install_cmd()

    Similar to test_install_cmd_1 but add an entry (neomake plugin) with
    missing key value pair and test if the directory structure for the absence
    of neomake and the presence of the remaining plugin which have a valid
    configuration entry
    """

    config = configparser.ConfigParser()
    config.read(write_conf_2)
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']

    command.install_cmd(config=write_conf_2)

    installed_plug = utils.instplug(str(temp_dir.getbasetemp()), 4)

    for plug_url in plug_urls:
        plug_name = os.path.basename(urlparse(plug_url).path)
        if 'neomake' in plug_name:
            assert not any(plug_name in s for s in installed_plug)
        else:
            plug_locrepo = os.path.join(config[plug_url]['package'],
                                        config[plug_url]['type'], plug_name)
            assert any(plug_locrepo in s for s in installed_plug)
