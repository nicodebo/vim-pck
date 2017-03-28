import pytest
import configparser
import os
from vim_pck import utils


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return(tmpdir_factory)


def test_inst_plug(temp_dir):
    """Test vim_pck.utils.instplug()

    Install some plugin and retrieve the list of installed plugin. Compare the
    effectively installed plugin with the retrieved plugin from the instplug
    function. They should be equal.
    """
    dirtest = 'install_cmd'
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
