import configparser
import os
import sys
import itertools

from vim_pck.git import GetRemote
from vim_pck import const


class ConfigFile:
    """This class define the configuration file and method that allows to
    manipulate it"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = ""  # path to the configuration file
        self.pack_path = ""
        self.rem_urls = []  # list of remote url section
        self._readconf()
        self._get_remote_urls()
        self._get_pack_path()
        self._sanitize_conf()

    def _readconf(self):
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

    def _get_pack_path(self):
        self.pack_path = os.path.expanduser(self.config['DEFAULT']['pack_path'])

    def _get_remote_urls(self):
        self.rem_urls = [sect for sect in self.config.sections() if sect != 'DEFAULT']

    def _sanitize_conf(self):
        """Add default values for the different keys (package, type, freeze) if
        they are not define by the user"""
        default_val = {const.PKG_NAME: const.PACKAGE,
                       const.TYPE_NAME: const.TYPE,
                       const.FRZ_NAME: const.FREEZE}
        for url, key in itertools.product(self.rem_urls, default_val.keys()):
            if not self.config.has_option(url, key):
                self.config[url][key] = str(default_val[key])

    def freeze_false(self):
        """Get the list of sections which freeze option is false

        The sanitize_conf function must have been called before to ensure that
        a freeze option is available
        """
        url_filt = []
        for rem_url in self.rem_urls:
            if not self.config.getboolean(rem_url, const.FRZ_NAME):
               url_filt.append(rem_url)
        return url_filt


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
