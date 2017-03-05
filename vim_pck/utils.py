import os


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
    for dirpath, dirnames, filenames in walklevel(pack_path, level):
        installed_plug.append(dirpath)
    return installed_plug
