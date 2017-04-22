import configparser
from itertools import compress
import os
import sys
from urllib.parse import urlparse


class ConfigFile:
    """This class define the configuration file and method that allows to
    manipulate it"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = ""
        self.pack_path = ""
        self.plugurls = []  # list of all url section
        self.valid_plug_entries = []  # list of url which entries are valid
        self.readconf()
        self.getpackpath()

    def readconf(self):
        # Read vimpck configuration file
        try:
            self.conf_path = os.environ['VIMPCKRC']
        except KeyError:
            self.conf_path = os.getenv(os.path.join(os.environ['XDG_CONFIG_HOME'],
                                                    'vimpck/config'),
                                       os.path.expanduser('~/.config/vimpck/config'))
        finally:
            if os.path.exists(self.conf_path):
                self.config.read(self.conf_path)
            else:
                sys.exit("No configuration file found!")

    def getpackpath(self):
        self.pack_path = os.path.expanduser(self.config['DEFAULT']['pack_path'])

    def getplugurls(self):
        self.plugurls = [sect for sect in self.config.sections() if sect != 'DEFAULT']

    def tagplugentries(self):
        """add a key/value pair, plug_locrepo, to self.config
        plug_locrepo = '', for invalid entries
        plug_locrepo = plugurl, for valid entries"""

        # get valid entries (plug_locrepo != '')
        for plug_url in self.plugurls:
            plug_name = os.path.basename(urlparse(plug_url).path)
            try:
                os.path.join(self.pack_path, self.config[plug_url]['package'],
                             self.config[plug_url]['type'], plug_name)
            except KeyError:
                pass
            else:
                self.valid_plug_entries.append(plug_url)


class PluginList:
    """This class define the list of plugin from which we can filter by
    opt/autostart. The list of plugins is directly read from the disk inside
    the pack path"""

    def __init__(self, pack_path):
        self.installed_plug = {}
        self.start_plug = []
        self.opt_plug = []
        self.pack_path = pack_path
        self.instplug()

    # http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
    def walklevel(self, some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def instplug(self, level=3):
        """ Return the list of installed plugin

        Arg:
            pack_path (str) : path of the neo(vim) builtin package directory

        Return:
            installed_plug (dictionnary) : key/value = plugin_name/{start/opt}
        """
        installed_plug_dir = []
        dirlen = []  # store length of the path (how deep they are)
        self.installed_plug = {}

        for dirpath, dirnames, filenames in self.walklevel(self.pack_path, level):
            installed_plug_dir.append(dirpath)
        # find deepest paths
        # http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
        for plug in installed_plug_dir:
            plug = os.path.normpath(plug)
            dirlen.append(len(plug.split(os.sep)))
        # keep only deepest path
        fil = [(i - j) == 0 for i, j in zip([max(dirlen)] * len(dirlen), dirlen)]
        installed_plug_dir = list(compress(installed_plug_dir, fil))

        for plug in installed_plug_dir:
            if "start" in plug:
                self.installed_plug[os.path.basename(plug)] = "start"
            else:
                self.installed_plug[os.path.basename(plug)] = "opt"

    def autostart(self):
        self.start_plug = []
        for key in self.installed_plug.keys():
            if self.installed_plug[key] == 'start':
                self.start_plug.append(key)

    def optional(self):
        self.opt_plug = []
        for key in self.installed_plug.keys():
            if self.installed_plug[key] == 'opt':
                self.opt_plug.append(key)


class UrlFilter:
    """ This class provide different urls plugins filter
    """

    def __init__(self):
        self.toinstall_plug = []

    def install(self, plugurlconf, plug_pack_path):
        """ Filter the list of plugin to be installed

        Arg:
            plugurlconf (str list): list of valid plugins url from the vimpckrc
            configuration file.
            plug_pack_path (str list): list of plugins installed on the disk on
            the pack_path

        The plugins to be installed are : (plugins from the configuration file)
        minus (plugins from the pack_path) meaning that only the plugins from
        the configuration file that are not present on the pack path of neovim
        are returned by this method. """

        self.toinstall_plug = []
        for plug_url in plugurlconf:
            if not any(os.path.basename(urlparse(plug_url).path)
                       in s for s in plug_pack_path):
                self.toinstall_plug.append(plug_url)
# TODO: inclure cette nouvelle classe dans command.py et dans test_command.py.
