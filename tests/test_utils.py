import pytest
import configparser
import os
from vim_pck import utils


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return(tmpdir_factory)


@pytest.fixture()
def write_conf(temp_dir):
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

#TODO: This hereabove fixture is useless since I don't use configuration file

def test_inst_plug(write_conf, temp_dir):
    """Test vim_pck.utils.instplug()

    Install some plugin and retrieve the list of installed plugin. Compare the
    effectively installed plugin with the retrieved plugin from the instplug
    function. They should be equal.
    """
    bsdir = str(temp_dir.getbasetemp())
    plugins = ['vim-colors-solarized', 'vim-mustache-handlebars',
               'vim-dispatch', 'vim-commentary']

    os.makedirs(os.path.join(bsdir, 'colors', 'start', plugins[0]))
    os.makedirs(os.path.join(bsdir, 'filetype', 'start', plugins[1]))
    os.makedirs(os.path.join(bsdir, 'common', 'opt', plugins[2]))
    os.makedirs(os.path.join(bsdir, 'common', 'start', plugins[3]))

    installed_plug = utils.instplug(bsdir, 4)
    if not set(installed_plug).difference(plugins):
        assert 1
    else:
        assert 0
