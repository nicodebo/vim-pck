import configparser
from itertools import compress
import os
import sys


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
    installed_plug = []
    dirlen = []  # store length of the path (how deep they are)
    for dirpath, dirnames, filenames in walklevel(pack_path, level):
        installed_plug.append(dirpath)
    # find deepest paths
    # http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
    for plug in installed_plug:
        plug = os.path.normpath(plug)
        dirlen.append(len(plug.split(os.sep)))
    # keep only deepest path
    fil = [(i - j) == 0 for i, j in zip([max(dirlen)]*len(dirlen), dirlen)]
    installed_plug = list(compress(installed_plug, fil))
    # keep only basename
    installed_plug = [os.path.basename(i) for i in installed_plug]
    return installed_plug


def readconf():

    config = configparser.ConfigParser()

    # Read vimpck configuration file
    try:
        conf_path = os.environ['VIMPCKRC']
    except KeyError:
        conf_path = os.getenv(os.path.join(os.environ['XDG_CONFIG_HOME'],
                                           'vimpck/config'),
                              os.path.expanduser('~/.config/vimpck/config'))
    finally:
        if os.path.exists(conf_path):
            config.read(conf_path)
        else:
            sys.exit("No configuration file found!")

    return config
