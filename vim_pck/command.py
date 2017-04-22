"""This module is where the main function for the subcommand of vimpck are
stored
"""

import os
import subprocess
import sys
from tqdm import tqdm
from urllib.parse import urlparse

from vim_pck import utils


def install_cmd():
    """Install function. This function is launched when the ``vimpck install``
    command is invoked.
    """

    vimpckrc = utils.ConfigFile()
    plugfilt = utils.UrlFilter()

    try:
        os.makedirs(vimpckrc.pack_path)
    except OSError:
        pass

    pluglist = utils.PluginList(vimpckrc.pack_path)
    vimpckrc.getplugurls()
    vimpckrc.tagplugentries()

    plugfilt.install(vimpckrc.valid_plug_entries, pluglist.installed_plug.keys())

    # install plugins
    gitcloneerror = []
    for plug_url in tqdm(plugfilt.toinstall_plug):
        temperror = []
        plug_name = os.path.basename(urlparse(plug_url).path)
        plug_locrepo = os.path.join(vimpckrc.pack_path,
                                    vimpckrc.config[plug_url]['package'],
                                    vimpckrc.config[plug_url]['type'],
                                    plug_name)
        try:
            subprocess.run(["git", "clone", plug_url, plug_locrepo],
                           stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            message = "Failed cloning : exit code: %s --> %s" % \
                      (e.returncode, plug_name)
            temperror.append(plug_name)
            temperror.append(plug_url)
            temperror.append(e.returncode)
            temperror.append(e.cmd)
            temperror.append(e.stderr)
            gitcloneerror.append(temperror)
        else:
            message = "Done cloning: %s --> %s" % \
                      (plug_name, plug_locrepo)
        finally:
            tqdm.write(message)

    if gitcloneerror:
        for err in gitcloneerror:
            message = "\n--> plug name: {0} \nplug url: {1} \ncmd: {2} \nerror code: {3} \nerror message: {4} \n".format(err[0], err[1], " ".join(err[3]), err[2], err[4].decode('UTF-8'))
            print(message)


def ls_cmd(**kwargs):
    """list function. This function is launched when the ``vimpck ls``
    command is invoked.

    Arg:
        **kwarg (str) : an argument is present, kwargs['start']/kwarg['opt'] to
        filter autostart/optional plugins
    """

    vimpckrc = utils.ConfigFile()
    if not os.path.isdir(vimpckrc.pack_path):
        sys.exit("{} does not exist. Use vimpck install".format(vimpckrc.pack_path))

    plugls = utils.PluginList(vimpckrc.pack_path)

    if kwargs['start']:
        plugls.autostart()
        plug = plugls.start_plug
    elif kwargs['opt']:
        plugls.optional()
        plug = plugls.opt_plug
    else:
        plug = []
        for key in plugls.installed_plug.keys():
            plug.append(key)

    return plug
