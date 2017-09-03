import configparser
import os
import subprocess
import pytest

from vim_pck import utils


@pytest.mark.skip(reason="to be reimplemented")
class Test_ConfigFile():
    """ Test the ConfigFile class
    """

    def test_conf_1(self, temp_dir, write_conf_1):
        """
        scenario: use a correct configuration file and check if the
        ConfigFile.plugurls attribute contains the url defined in the
        configuration file. The url set from the configuration file should be
        equal to the attribute set of the ConfigFile class """

        vimpckrc = utils.ConfigFile()
        vimpckrc.getplugurls()

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']

        if not set(vimpckrc.plugurls).symmetric_difference(set(plug_urls)):
            assert 1
        else:
            assert 0

    def test_conf_2(self, temp_dir, write_conf_2):
        """
        scenario: use an erroneous configuration file and check if the
        ConfigFile.plugurls attribute contains the url defined in the
        configuration file. The url set from the configuration file should be
        equal to the attribute set of the ConfigFile class. Also the
        valid_plug_entries attribute should be missing the neomake entry since
        this entry is wrong (missing key)
        """

        vimpckrc = utils.ConfigFile()
        vimpckrc.getplugurls()
        vimpckrc.tagplugentries()

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']

        if not set(vimpckrc.plugurls).symmetric_difference(set(plug_urls)):
            assert 1
        else:
            assert 0

        diff = set(vimpckrc.plugurls).difference(set(vimpckrc.valid_plug_entries))

        if ('neomake' in str(diff)) and (len(diff) == 1):
            assert 1
        else:
            assert 0

    def test_nonfreezedurl(self, write_conf_4):
        """ Some plugin from the configuration file write_conf_4 are freezed
        (i.e. vim-commentary) nonfreezedurl should append all the plugin except
        vim-commentary in the nonfreeze_urls attribut
        """
        vimpckrc = utils.ConfigFile()
        vimpckrc.getplugurls()
        vimpckrc.tagplugentries()
        vimpckrc.nonfreezedurl()

        config = configparser.ConfigParser()
        config.read(os.environ["VIMPCKRC"])
        plug_urls = [sect for sect in config.sections() if sect != 'DEFAULT']

        diff = set(plug_urls).difference(set(vimpckrc.nonfreeze_urls))

        if ('vim-commentary' in str(diff)) and (len(diff) == 1):
            assert 1
        else:
            assert 0


class Test_DiskPlugin():
    """Test the DiskPlugin class"""

    def test_install_4_fake_plugin_no_problem(self, temp_dir):
        """
        Simulate installing 4 plugins by creating 4 git folder and assigning
        them a fake remote url.
        Then use the DiskPlugin to get the dictionary of plugin and make a
        comparison between what has been installed and what is retrieve
        """
        bsdir = str(temp_dir.mktemp("test_DiskPlugin_class"))
        plugins = {'colors/start/vim-colors-solarized': 'fake_url1',
                   'filetype/opt/vim-mustache-handlebars': 'fake_url2',
                   'filetype/start/vim-dispatch': 'fake_url3',
                   'common/start/vim-commentary': 'fake_url4'}

        for key in plugins:
            local_dir = os.path.join(bsdir, key)
            os.makedirs(local_dir)
            cmd = ["git", "-C", local_dir, "init"]
            subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=True)
            cmd = ["git", "-C", local_dir, "remote", "add", "origin",
                   plugins[key]]
            subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=True)

        plugls = utils.DiskPlugin(bsdir)

        if not set(plugls.all_plug.keys()).symmetric_difference(set(plugins.keys())):
            assert 1
        else:
            assert 0

        if not set(plugls.all_plug.values()).symmetric_difference(set(plugins.values())):
            assert 1
        else:
            assert 0

