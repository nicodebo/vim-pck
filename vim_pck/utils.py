import os
import sys
import configobj
from validate import Validator

from vim_pck.git import GetRemote
from vim_pck import const


class ConfigFile:
    """This class define the configuration file and method that allows to
    manipulate it"""

    def __init__(self):
        self.conf_path = ""  # path to the configuration file
        self.config = None  # ConfigObj object
        self._get_conf_path()
        self._read_conf()
        self._validate_conf()
        self._get_pack_path()
        self.pack_path = ""
        self.rem_urls = []  # list of remote url section
        self._get_remote_urls()
        self._get_pack_path()

    def _get_conf_path(self):
        """ Determine the configuration file path """
        # xdg directory for configuration file
        try:
            conf_path = os.environ["VIMPCKRC"]
        except KeyError:
            try:
                conf_path = os.path.join(os.environ['XDG_CONFIG_HOME'], 'vimpck', 'config')
            except KeyError:
                conf_path = os.path.join(os.environ['HOME'], '.config', 'vimpck', 'config')
        self.conf_path = conf_path

    def _read_conf(self):
        if os.path.exists(self.conf_path):
            self.config = configobj.ConfigObj(self.conf_path,
                                              configspec=os.path.join(const.ROOT_DIR,
                                                                      'configspec.ini'))
        else:
            sys.exit("No configuration file found!")

    def _validate_conf(self):
        """ Check if the configuration file is correct """
        validator = Validator()
        results = self.config.validate(validator)
        if not results:
            for entry in configobj.flatten_errors(self.config, results):
                # each entry is a tuple
                section_list, key, error = entry
                if key is not None:
                    section_list.append(key)
                else:
                    section_list.append('[missing section]')
                section_string = ', '.join(section_list)
                if not error:
                    error = 'Missing value or section.'
                print(section_string, ' = ', error)
            sys.exit(1)

    def _get_pack_path(self):
        self.pack_path = os.path.expanduser(self.config[const.SECT_1]['pack_path'])

    def _get_remote_urls(self):
        self.rem_urls = self.config[const.SECT_2].keys()

    def freeze_false(self):
        """Get the list of sections which freeze option is false
        """
        url_filt = []
        for rem_url in self.rem_urls:
            if not self.config[const.SECT_2][rem_url].as_bool(const.FRZ_NAME):
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
