import configparser
import os
from vim_pck import utils


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


def test_PluginList(temp_dir):
    """Test the PluginList class

    Simulate the installation of plugin by creating 4 folder, then compare the
    effectively installed plugin with the retrieved plugin from the instplug
    method. They should be equal.
    Also test
    """
    dirtest = 'PluginList'
    bsdir = str(temp_dir.mktemp(dirtest))
    plugins = ['vim-colors-solarized', 'vim-mustache-handlebars',
               'vim-dispatch', 'vim-commentary']

    os.makedirs(os.path.join(bsdir, 'colors', 'start', plugins[0]))
    os.makedirs(os.path.join(bsdir, 'filetype', 'start', plugins[1]))
    os.makedirs(os.path.join(bsdir, 'common', 'opt', plugins[2]))
    os.makedirs(os.path.join(bsdir, 'common', 'start', plugins[3]))

    plugls = utils.PluginList(bsdir)
    plugls.autostart()
    plugls.optional()

    if not set(plugins).symmetric_difference(set(plugls.installed_plug.keys())):
        assert 1
    else:
        assert 0

    if not set([plugins[0], plugins[1],
               plugins[3]]).symmetric_difference(set(plugls.start_plug)):
        assert 1
    else:
        assert 0

    if not set([plugins[2]]).symmetric_difference(set(plugls.opt_plug)):
        assert 1
    else:
        assert 0


class Test_UrlFilter:
    """ Test the UrlFilter class
    """

    def test_first_install(self, temp_dir, write_conf_1):
        """ scenario_1: Test with a correct configuration file, this is the
        first time installation
        """
        vimpckrc = utils.ConfigFile()
        vimpckrc.getplugurls()
        vimpckrc.tagplugentries()
        plugls = utils.PluginList(vimpckrc.pack_path)
        plugfilt = utils.UrlFilter()
        plugfilt.install(vimpckrc.valid_plug_entries, plugls.installed_plug.keys())

        if not set(vimpckrc.valid_plug_entries).symmetric_difference(set(plugfilt.toinstall_plug)):
            assert 1
        else:
            assert 0

    def test_second_install(self, temp_dir, write_conf_2):
        """ Test with a valid configuration file, vim-commentary has already
        been installed, thus Urlfilt should return the entire list of plugin
        except vim-commentary
        """
        vimpckrc = utils.ConfigFile()
        vimpckrc.getplugurls()
        vimpckrc.tagplugentries()
        plugls = utils.PluginList(vimpckrc.pack_path)
        plugfilt = utils.UrlFilter()
        plugfilt.install(vimpckrc.valid_plug_entries, plugls.installed_plug.keys())

        if not set(vimpckrc.valid_plug_entries).symmetric_difference(set(plugfilt.toinstall_plug)):
            assert 1
        else:
            assert 0

        os.makedirs(os.path.join(vimpckrc.pack_path, 'colors', 'start', 'vim-commentary'))
        plugls = utils.PluginList(vimpckrc.pack_path)
        old_value = plugfilt.toinstall_plug
        plugfilt.install(vimpckrc.valid_plug_entries, plugls.installed_plug.keys())
        diff = set(old_value).difference(set(plugfilt.toinstall_plug))
        if ('vim-commentary' in str(diff)) and (len(diff) == 1):
            assert 1
        else:
            assert 0
