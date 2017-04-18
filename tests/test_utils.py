import pytest
import configparser
import os
from vim_pck import utils


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return(tmpdir_factory)


@pytest.fixture()
def write_conf_class(temp_dir, monkeypatch):
    """ Initial setup for the test_install_cmd_1 test function

    1. Write a vimpck configuration file
    2. Set the VIMPCKRC env variable to the path of the created configuration
        file
    """
    config = configparser.ConfigParser()
    dirtest = 'ConfigFile'
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


def test_inst_plug(temp_dir):
    """Test vim_pck.utils.instplug()

    Install some plugin and retrieve the list of installed plugin. Compare the
    effectively installed plugin with the retrieved plugin from the instplug
    function. They should be equal.
    """
    dirtest = 'inst_plug'
    bsdir = str(temp_dir.mktemp(dirtest))
    plugins = ['vim-colors-solarized', 'vim-mustache-handlebars',
               'vim-dispatch', 'vim-commentary']

    os.makedirs(os.path.join(bsdir, 'colors', 'start', plugins[0]))
    os.makedirs(os.path.join(bsdir, 'filetype', 'start', plugins[1]))
    os.makedirs(os.path.join(bsdir, 'common', 'opt', plugins[2]))
    os.makedirs(os.path.join(bsdir, 'common', 'start', plugins[3]))

    installed_plug = utils.instplug(bsdir)

    if not set(plugins).symmetric_difference(set(installed_plug.keys())):
        assert 1
    else:
        assert 0


def test_ConfigFile(temp_dir, write_conf_class):
    vimpckrc = utils.ConfigFile()
    vimpckrc.getplugurls()

    config = configparser.ConfigParser()
    config.read(os.environ["VIMPCKRC"])
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']

    if not set(vimpckrc.plugurls).symmetric_difference(set(plug_urls)):
        assert 1
    else:
        assert 0
