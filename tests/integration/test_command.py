import configparser
import os
import pytest
from urllib.parse import urlparse
import subprocess
from vim_pck import command
from vim_pck import utils


@pytest.mark.skip(reason="to be reimplemented")
class Test_Install_cmd:
    """Test vim_pck.command.install_cmd()
    """
    def test_1(self, write_conf_1, temp_dir):
        """
        Clone some repository from a configuration file defined by the
        write_conf_1 fixture and then check that the directory structure
        correspond to the one specified in the configuration file.
        ex: is "/common/vim-commentary" (from the configuration file) included
        somewhere in the pack_path ?
        """

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
        plug_names = [os.path.basename(i) for i in plug_urls]
        pack_path = config['DEFAULT']['pack_path']

        command.install_cmd()

        plugls = utils.PluginList(pack_path)

        pluglist = [elem.split('/')[2] for elem in plugls.installed_plug.keys()]

        if not set(plug_names).symmetric_difference(set(pluglist)):
            assert 1
        else:
            assert 0

    def test_2(self, write_conf_2, temp_dir):
        """Test vim_pck.command.install_cmd()

        Similar to test_install_cmd_1 but add an entry (neomake plugin) with
        missing key value pair and test if the directory structure for the absence
        of neomake and the presence of the remaining plugin which have a valid
        configuration entry
        """

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        config.read(os.environ["VIMPCKRC"])
        plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
        plug_names = [os.path.basename(i) for i in plug_urls]
        pack_path = config['DEFAULT']['pack_path']

        command.install_cmd()
        plugls = utils.PluginList(pack_path)
        pluglist = [elem.split('/')[2] for elem in plugls.installed_plug.keys()]

        diff = set(pluglist).symmetric_difference(plug_names)
        if ('neomake' in str(diff)) and (len(diff) == 1):
            assert 1
        else:
            assert 0

    def test_3(self, write_conf_1, temp_dir):
        """ Test vim_pck.command.install_cmd()

        Install some plugin and reinstall them just to see if there is any
        error """

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
        plug_names = [os.path.basename(i) for i in plug_urls]
        pack_path = config['DEFAULT']['pack_path']

        command.install_cmd()
        plugls = utils.PluginList(pack_path)

        pluglist = [elem.split('/')[2] for elem in plugls.installed_plug.keys()]

        if not set(plug_names).symmetric_difference(set(pluglist)):
            assert 1
        else:
            assert 0

        command.install_cmd()
        plugls = utils.PluginList(pack_path)

        pluglist = [elem.split('/')[2] for elem in plugls.installed_plug.keys()]
        if not set(plug_names).symmetric_difference(set(pluglist)):
            assert 1
        else:
            assert 0

    def test_4(self, write_conf_3, temp_dir):
        """Test vim_pck.command.install_cmd()

        Clone some repository from a configuration file defined by the
        write_conf_3 fixture and then check that the directory structure
        correspond to the one specified in the configuration file.
        ex: is "/common/vim-commentary" (from the configuration file) included
        somewhere where the install_cmd have cloned the repository into.
        """

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        # plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
        pack_path = config['DEFAULT']['pack_path']

        command.install_cmd()

        plugls = utils.PluginList(pack_path)

        goodplugin = ["vim-commentary", "vim-dispatch", "vim-colors-solarized"]

        if not set(goodplugin).symmetric_difference(set(plugls.installed_plug.keys())):
            assert 1
        else:
            assert 0


@pytest.mark.skip(reason="to be reimplemented")
def test_ls_cmd(write_conf_1, temp_dir):
    """Test vim_pck.utils.instplug()

    Install some plugin and retrieve the list of installed plugin. Compare the
    effectively installed plugin with the retrieved plugin from the instplug
    function. They should be equal.
    """

    config = configparser.ConfigParser()
    config.read(os.environ["VIMPCKRC"])
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
    pack_path = config['DEFAULT']['pack_path']

    try:
        for i in plug_urls:
            os.makedirs(os.path.join(pack_path,
                                     config[i]['package'],
                                     config[i]['type'],
                                     os.path.basename(i)))
    except OSError:
        pass

    plug_names = [os.path.basename(i) for i in plug_urls]
    allplug = command.ls_cmd(start=False, opt=False)

    allplug = [elem.split('/')[2] for elem in allplug]

    if not set(allplug).symmetric_difference(set(plug_names)):
        assert 1
    else:
        assert 0

    plug_names_start = [os.path.basename(i) for i in plug_urls if config[i]['type'] == 'start']
    startplug = command.ls_cmd(start=True, opt=False)

    startplug = [elem.split('/')[2] for elem in startplug if elem.split('/')[1] == "start"]
    if not set(startplug).symmetric_difference(set(plug_names_start)):
        assert 1
    else:
        assert 0

    plug_names_opt = [os.path.basename(i) for i in plug_urls if config[i]['type'] == 'opt']
    optplug = command.ls_cmd(start=False, opt=True)
    optplug = [elem.split('/')[2] for elem in optplug if elem.split('/')[1] == "opt"]

    if not set(optplug).symmetric_difference(set(plug_names_opt)):
        assert 1
    else:
        assert 0


@pytest.mark.skip(reason="to be reimplemented")
def test_upgrade_cmd(write_conf_1):
    """Test vim_pck.utils.upgrade_cmd()

    Install the plugin from the configuration file but from a previous commit.
    Then upgrade all plugins and compare the previous and current commit.
    """

    config = configparser.ConfigParser()
    config.read(os.environ["VIMPCKRC"])
    plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']
    pack_path = config['DEFAULT']['pack_path']

    info = []  # Store url, later and older sha
    for url in plug_urls:
        urlinfo = []
        plug_name = os.path.basename(urlparse(url).path)
        plug_locrepo = os.path.join(pack_path,
                                    config[url]['package'],
                                    config[url]['type'],
                                    plug_name)
        subprocess.run(["git", "clone", url, plug_locrepo], check=True)

        # get the current sha
        a = subprocess.run(["git", "-C", plug_locrepo, "rev-list", "-1", "HEAD"],
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=True)

        master_sha = a.stdout.decode('UTF-8').rstrip()

        # get 4 sha below the current sha
        b = subprocess.run(["git", "-C", plug_locrepo, "rev-list", "-1", "HEAD~3"],
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=True)

        older_sha = b.stdout.decode('UTF-8').rstrip()
        urlinfo.append(url)
        urlinfo.append(plug_locrepo)
        urlinfo.append(master_sha)
        urlinfo.append(older_sha)
        info.append(urlinfo)

        subprocess.run(["git", "-C", plug_locrepo, "reset", "--hard", older_sha],
                       check=True)

    # check that the working tree has been well downgraded
    for elem in info:
        # get sha

        c = subprocess.run(["git", "-C", elem[1], "rev-list", "-1", "HEAD"],
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=True)

        master_sha = c.stdout.decode('UTF-8').rstrip()
        if master_sha == elem[3]:
            assert 1
        else:
            assert 0

    # upgrade all plugins
    command.upgrade_cmd()

    #     # TODO: if one of the repositories I'm using for tests is updated
    #     # during this particular test, then, it might fail !!

    for elem in info:
        # get sha
        c = subprocess.run(["git", "-C", elem[1], "rev-list", "-1", "HEAD"],
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                           check=True)

        master_sha = c.stdout.decode('UTF-8').rstrip()

        if master_sha == elem[2]:
            assert 1
        else:
            assert 0

