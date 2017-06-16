import configparser
import os
import sys
from urllib.parse import urlparse
from vim_pck.git import GetRemote


class ConfigFile:
    """This class define the configuration file and method that allows to
    manipulate it"""
    # TODO: Refactoring Idea: Would it be possible to make a class that inherit
    # from configparser.ConfigParser() class ?

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = ""
        self.pack_path = ""
        self.plugurls = []  # list of all url section
        self.valid_plug_entries = []  # list of url which entries are valid
        self.nonfreeze_urls = []  # list of url which are valid and non freezed
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
        plug_locrepo = plugurl, for valid entries
        An invalid plug entries is one with package or type key missing"""

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

    def nonfreezedurl(self):
        """ Get the list of plugins url that are not marked as freezed"""
        self.nonfreeze_urls = []
        freeze = False
        for url in self.valid_plug_entries:
            freeze = False
            try:
                freeze_val = self.config[url]['freeze']
            except KeyError:
                pass
            else:
                if freeze_val.lower() == 'yes' or freeze_val.lower() == 'true':
                    freeze = True
            if not freeze:
                self.nonfreeze_urls.append(url)


class DiskPlugin:
    """This class allow to access the plugins locally installed on the pack
    path.

    Attributs:
            - all_plug (dict): key = <package_name>/{start|opt}/<plugin_name>
                               value = remote_url, ex: https://path/to/repo
            - pack_path (str): package directory
    """

    def __init__(self, pack_path):
        self.all_plug = {}
        self.pack_path = pack_path
        self.git_config = [GetRemote("")]  # object container
        # Local path is not currently known so initilized at en empty string
        self._list_remote_url(self._list_plug_dir())

    @staticmethod
    def _walklevel(some_dir, level):
        """
        Get a list of directories at a specified level from <some_dir>
        http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
        """
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def _list_plug_dir(self, level=3):
        """Get the list of installed plugins with there respective remote url
        # http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
        """

        dir_list = {}  # temp dictionary key: directory, value: depth

        # Get a complete list of directory 3 level down pack path
        for dirpath, dirnames, filenames in self._walklevel(self.pack_path,
                                                            level):
            dir_list[dirpath] = 0

        # compute depth of each path
        for elem in dir_list.keys():
            elem_norm = os.path.normpath(elem)
            dir_list[elem] = len(elem_norm.split(os.sep))

        # keep only deepest paths
        max_depth = max(dir_list.values())
        dir_list = {k: v for k, v in dir_list.items() if v == max_depth}

        return dir_list.keys()

    def _list_remote_url(self, dir_list):
        """Get remote url of locally cloned repository

        Arguments:
                - dir_list (list(str)): list of directory
        """
        self.all_plug = {}

        for elem in dir_list:
            out = 1
            self.git_config[0].local_dir = elem
            out = self.git_config[0].git_cmd()
            if out == 0:
                # keep only : <package>/{<start>|<opt>}/<plugin>
                rel_plug_path = os.path.relpath(elem, self.pack_path)
                self.all_plug[rel_plug_path] = self.git_config[0].retrieve_stdout()
            else:
                # TODO: in case something went wrong, write it down to a log
                pass

    def filt_plug(self, plug_type):
        """Filter plugin

        plug_type either start or opt
        """
        plug = []
        for key in self.all_plug.keys():
            if key.split('/')[1] == plug_type:
                plug.append(key)
        return plug

    # TODO: Add an option to allow colorizing the output of the list command.
    # Maybe one color for each part of the path

    # TODO: Add the number of plugin listed at the top like the ll command
    # show the size.

# TODO: replace os.path.basename par posixpath.basename:
# http://stackoverflow.com/questions/449775/how-can-i-split-a-url-string-up-into-separate-parts-in-python

