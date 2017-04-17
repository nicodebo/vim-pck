import configparser
from itertools import compress
import os
import sys
from urllib.parse import urlparse


# http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def instplug(pack_path, level=3):
    """ Return the list of installed plugin

    Arg:
        pack_path (str) : path of the neo(vim) builtin package directory

    Return:
        installed_plug (list) : list of installed plugins
    """
    installed_plug_dir = []
    dirlen = []  # store length of the path (how deep they are)
    installed_plug = {}

    for dirpath, dirnames, filenames in walklevel(pack_path, level):
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
            installed_plug[os.path.basename(plug)] = "start"
        else:
            installed_plug[os.path.basename(plug)] = "opt"

    return installed_plug


# class PluginsList:
#     """This class define the list of plugin from which we can filter by
#     opt/autostart"""

#     def __init__(self):
#         self.list = {}

class ConfigFile:
    """This class define the configuration file and method that allows to
    manipulate it"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = ""
        self.pack_path = ""
        self.plugurls = []
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
                plug_locrepo = os.path.join(self.pack_path,
                                            self.config[plug_url]['package'],
                                            self.config[plug_url]['type'],
                                            plug_name)
            except KeyError:
                plug_locrepo = ''
            finally:
                self.config[plug_url]['plug_locrepo'] = plug_locrepo
