"""This module is where the main function for the subcommand of vimpck are
stored
"""

import os
import subprocess
from tqdm import tqdm
from urllib.parse import urlparse

from vim_pck import utils


def install_cmd(**kwargs):
    """Install function. This function is launched when the ``vimpck install``
    command is invoked.

    Only install plugin that are currently not present on the pack directory

    Arg:
        **kwarg (str) : an argument is present, kwargs['config'] only if the
        --congig flag of the install subcommand was specified. It used to
        specify an alternate configuration file. Used for testing purpose.
    """

    vimpckrc = utils.ConfigFile()

    try:
        os.makedirs(vimpckrc.pack_path)
    except OSError:
        pass

    vimpckrc.getplugurls()
    vimpckrc.tagplugentries()
    # get already installed plugins
    installed_plug = utils.instplug(vimpckrc.pack_path)

    # filter config entries to only get non-installed plugins
    # TODO: à mettre dans la classe qui ListPlugin
    plug_urls_fil = []
    for plug_url in vimpckrc.plugurls:
        if not any(os.path.basename(
            urlparse(vimpckrc.config[plug_url]['plug_locrepo']).path)
                in s for s in installed_plug):
            plug_urls_fil.append(plug_url)

    # install plugins
    gitcloneerror = []
    for plug_url in tqdm(plug_urls_fil):
        temperror = []
        plug_name = os.path.basename(urlparse(plug_url).path)
        plug_locrepo = vimpckrc.config[plug_url]['plug_locrepo']

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
                      (plug_name, os.path.split(plug_locrepo)[0])
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
    # get already installed plugins
    installed_plug = utils.instplug(vimpckrc.pack_path)

    plug = []
    if kwargs['start']:
        for key in installed_plug.keys():
            if installed_plug[key] == 'start':
                plug.append(key)
    elif kwargs['opt']:
        for key in installed_plug.keys():
            if installed_plug[key] == 'opt':
                plug.append(key)
    else:
        for key in installed_plug.keys():
            plug.append(key)
    return plug
